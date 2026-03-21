import discord
from discord.ext import commands
from utils.bot import UPLBot
import sqlite3
from config import CHANNEL_ID, BACKEND_URL, BACKEND_PORT, BACKEND_ROUTE_ADDCHANNEL, BACKEND_ROUTE_DELCHANNEL, BACKEND_ROUTE_CURCHANNEL
import logging
import aiohttp
import json

logger = logging.getLogger(__name__)

class Utility(commands.Cog):
    def __init__(self, bot: UPLBot):
        self.bot = bot
        self.scrape_channels = set()

    @commands.command(
        help="!ping - Utility to help test bot responsiveness"
    )
    @commands.has_permissions(administrator=True)
    async def ping(self, ctx):
        await ctx.message.delete()
        await ctx.send("Pong!", delete_after=2)

    @commands.command(
        help="!addChannel [channelId] - Adds a channel to be scrapped from"
    )
    @commands.has_permissions(administrator=True)
    async def addChannel(self, ctx, channelId: int):
        await ctx.message.delete()

        channel = self.bot.get_channel(channelId)

        if channel is None:
            await ctx.send('Could not find that channel.', delete_after=2)
            return

        # Check for duplicates before adding
        if channelId in CHANNEL_ID:
            await ctx.send('You are already scrapping from that channel')
            return
        
        json_addChannel = {'server_id': ctx.guild.id, 'channel_id': channelId}
        # json_addChannel = json.dumps(json_addChannel)

        try:
            # Write to DB/send to Flask backend
            async with aiohttp.ClientSession() as session:
                BASE_URL = f"http://{BACKEND_URL}:{BACKEND_PORT}"
                FULL_URL = f"{BASE_URL}/{BACKEND_ROUTE_ADDCHANNEL}"

                async with session.post(FULL_URL, json=json_addChannel) as response:
                    if response.status == 201:
                        # Now add it to memory
                        CHANNEL_ID.add(channelId)
                        await ctx.send('Successfully added channel to scrapping list.', delete_after=2)
                    else:
                        text = await response.text()
                        logger.warning(f"Backend error: {text}") 
        except aiohttp.ClientError as e:
            logger.warning(f"Failed to connect to backend addChannel: {e}") 
        except Exception as e:
            logger.warning(f"on_message error addChannel: {e}")
            
        


    @commands.command(
        help="!removeChannel [channelId] - Removes a channel to be scrapped from"
    )
    @commands.has_permissions(administrator=True)
    async def removeChannel(self, ctx, channelId: int):
        await ctx.message.delete()

        channel = self.bot.get_channel(channelId)

        if channel is None:
            await ctx.send('Could not find that channel.', delete_after=2)
            return
        
        if channelId not in CHANNEL_ID:
            await ctx.send('That channel was not being scrapped.', delete_after=2)
            return
        
        json_delChannel = {'server_id': ctx.guild.id, 'channel_id': channelId}
        # json_delChannel = json.dumps(json_delChannel)

        try:
            # Write to DB/send to Flask backend
            async with aiohttp.ClientSession() as session:
                BASE_URL = f"http://{BACKEND_URL}:{BACKEND_PORT}"
                FULL_URL = f"{BASE_URL}/{BACKEND_ROUTE_DELCHANNEL}"

                # async with session.post(FULL_URL, json=json_delChannel) as response:
                async with session.request("DELETE", FULL_URL, json=json_delChannel) as response:
                    if response.status == 200:
                        CHANNEL_ID.discard(channelId)
                        await ctx.send('Successfully discarded channel from scrapping list.')
                    else:
                        text = await response.text()
                        logger.warning(f"Backend error: {text}") 
        except aiohttp.ClientError as e:
            logger.warning(f"Failed to connect to backend addChannel: {e}") 
        except Exception as e:
            logger.warning(f"on_message error addChannel: {e}")
        
        
        
    @commands.command(
        help="!currentChannels - Lists all the channels that are currently being scrapped"
    )
    @commands.has_permissions(administrator=True)
    async def currentChannels(self, ctx):
        await ctx.message.delete()

        if not CHANNEL_ID:
            await ctx.send('Currently no channels being scrapped', delete_after=2)
            return
                    
        # We shouldn't delete msg
        await ctx.send(f"Channel IDs: {", ".join([str(channel) for channel in CHANNEL_ID])}")


    # https://fallendeity.github.io/discord.py-masterclass/error-handling/#what-library-does-with-the-errors
    @addChannel.error
    async def addChannel_error(self, ctx, error):
        await ctx.message.delete()

        if isinstance(error, commands.BadArgument):
            await ctx.send("Invalid channel ID. Please provide a valid integer.", delete_after=5)
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send("You do not have permission to add channels.", delete_after=5)

    @removeChannel.error
    async def removeChannel_error(self, ctx, error):
        await ctx.message.delete()
        if isinstance(error, commands.BadArgument):
            await ctx.send("Invalid channel ID. Please provide a valid integer.", delete_after=5)
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send("You do not have permission to add channels.", delete_after=5)

    @currentChannels.error
    async def currentChannels_error(self, ctx, error):
        await ctx.message.delete()
        if isinstance(error, commands.BadArgument):
            await ctx.send("Invalid channel ID. Please provide a valid integer.", delete_after=5)
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send("You do not have permission to add channels.", delete_after=5)


# We must add this line for every cog file we have
async def setup(UPLBot):
    await UPLBot.add_cog(Utility(UPLBot))

