import discord
from discord.ext import commands
from config import OWNERS, PREFIX, CHANNEL_ID, BACKEND_URL, BACKEND_PORT, BACKEND_ROUTE, GEMINI_API_KEY
import os, sys
from pathlib import Path
import logging
import aiohttp
from google import genai
import datetime

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import llmScraper

#import DiscordBot.utils.llmScraper


logger = logging.getLogger(__name__)

class UPLBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.members = True
        intents.message_content = True
        

        super().__init__(
            owner_ids=OWNERS,
            command_prefix=PREFIX,
            intents=intents,
        )

        self.cogs_loaded = False
        self.geminiClient = genai.Client(api_key=GEMINI_API_KEY)    

    async def setup_hook(self):
        await self.load_extensions('./cogs')
        
        # await self.addChannelsUponStartup()

        self.cogs_loaded = True

    # Test this method
    async def addChannelsUponStartup(self):
        await self.wait_until_ready()

        async with aiohttp.ClientSession() as session:
            BASE_URL = f"http://{BACKEND_URL}:{BACKEND_PORT}"
            
            # For all the servers we are in...
            for guild in self.guilds:
                print(f"Guild count: {len(self.guilds)}")
                try:
                    url = f"{BASE_URL}/channels/{guild.id}"

                    async with session.get(url) as response:
                        if response.status == 200:
                            data = await response.json()


                            channel_ids = set(map(int, data))

                            CHANNEL_ID.update(channel_ids)

                            print(f"Loaded {len(channel_ids)} channels for guild {guild.id}")
                        else:
                            text = await response.text()
                            logger.warning(f"Failed to load channels: {text}")
                            await self.close()
                            return

                except Exception as e:
                    logger.warning(f"Error loading channels for guild {guild.id}: {e}")
                    await self.close()
                    return 

    async def on_ready(self):
        print(f"Ready! {self.user.name} ID: {self.user.id}")

        if not hasattr(self, "channels_loaded"):
            await self.addChannelsUponStartup()
            self.channels_loaded = True


    def validate_ISO8601(self, date):
        try:
            datetime.datetime.fromisoformat(date)
            return True
        except ValueError:
            return False

    async def on_message(self, message: discord.Message):
        if message.author == self.user:
            return
        
        await self.process_commands(message)
         
        if message.channel.id not in CHANNEL_ID:
            return
        
        if message.content.startswith(self.command_prefix):
            # print("DEBUG: Made it here to on_message while using a command prefix")
            return

        try:

            # Will be an empty list if no attachments
            media = {"media": [attachment.url for attachment in message.attachments]}

            response_json = await llmScraper.summarizer(self.geminiClient, message.content)

            if not response_json:
                return

            # Verify that results are in correct format

            # Foot has to be a 0 or a 1 due to integer wanted from db
            food_val = response_json.get("food")

            if food_val is None:
                response_json["food"] = 0
            else:
                response_json["food"] = 1 if bool(food_val) else 0

            # Verify date matches standard format
            start_val = response_json.get("start")

            if start_val and self.validate_ISO8601(start_val):
                    response_json["start"] = start_val
            else:
                response_json["start"] = None


            response_json.update(media)

            json_payload = response_json

            async with aiohttp.ClientSession() as session:
                BASE_URL = f"http://{BACKEND_URL}:{BACKEND_PORT}"
                FULL_URL = f"{BASE_URL}/{BACKEND_ROUTE}"

                async with session.post(FULL_URL, json=json_payload) as response:
                    if response.status == 201:
                        pass
                    else:
                        text = await response.text()
                        logger.warning(f"Backend error: {text}") 


                        # await message.channel.send(f"Backend error: {text}")

            print(json_payload)
            
        except aiohttp.ClientError as e:
            #await message.channel.send(f"Failed to connect to backend: {e}")
            logger.warning(f"Failed to connect to backend: {e}") 
        except Exception as e:
            logger.warning(f"on_message error: {e}") 
        
    async def load_extensions(self, filename_):
        loaded = []
        not_loaded = {}
        i = 0
        total = 0

        for filename in Path(filename_).iterdir():
            if filename.suffix == '.py' and filename != "__init__.py":
                total += 1
                
                handle = f'{Path(filename_).name}.{filename.stem}'
                
                try:
                    await self.load_extension(handle)
                    loaded.append(handle)
                    i += 1
                except Exception as e:
                    not_loaded.update({handle: e})

        print(f"Loaded {i}/{total} extensions from {filename_}")
        return loaded, not_loaded
    
    