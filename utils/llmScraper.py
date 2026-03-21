from google import genai
import json
import asyncio
import logging

logger = logging.getLogger(__name__)

def removeFirstAndLastLines(text):
    textSplit = text.split("\n")

    response = '\n'.join(textSplit[1:-1])

    return response


async def summarizer(client, text):
    ASK_GEMINI = """
Ignore any casual conversation, jokes, or vague messsages.

If the message is NOT a valid event, return:
{
  "name": null,
  "description": null,
  "location": null,
  "start": null,
  "duration": null,
  "food": null
}

Otherwise, if a valid event:
Extract information matching this schema.
Return ONLY valid JSON.
Do NOT include explanations.
Do NOT wrap in markdown.
If missing, use null.
If you believe the message is not an event, simply use null for all fields.

Schema:
{
  "is_event": boolean, // true ONLY if the email is announcing a specific upcoming event, workshop, or gathering. false for newsletters, receipts, account creations, etc.
  "name": string,
  "description": string,
  "location": string,
  "start": string (STRICT ISO 8601 format: YYYY-MM-DDTHH:MM:SS),
  "duration": string,
  "food": boolean or null
}
"""

    prompt = ASK_GEMINI + text

    response = await client.aio.models.generate_content(
        model="gemini-2.0-flash-lite-preview-02-05", contents=prompt # chose the model here
    )

    try:

        response_json = json.loads(response.text)

        # https://www.w3schools.com/python/ref_func_isinstance.asp
        if not isinstance(response_json, dict):
            logger.warning(f"response_json is not isInstance of dictionary")
            return None
        
        #if response_json["name"] is None and response_json["description"] is None and response_json["location"] is None and response_json["start"] is None and response_json["duration"] is None and response_json["food"] is None:
        #    logger.debug(f"response_json only has None values")
        #    return None
        
        # If value is None -> True, and if all values are None -> True, then all() returns true
        if all(value is None for value in response_json.values()):
            print("Made it here llm scraper no significant values")
            logger.debug("response_json only has None values")
            return None
        
        return response_json
    except json.JSONDecodeError as e:
        # response_json = {}
        logger.warning(f"Failed to decode Gemini response: {e}")
        return None
