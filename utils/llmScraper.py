from google import genai
import json
import asyncio

def removeFirstAndLastLines(text):
    textSplit = text.split("\n")

    response = '\n'.join(textSplit[1:-1])

    return response


async def summarizer(client, text):
    ASK_GEMINI = """
Extract information matching this schema.
Return ONLY valid JSON.
Do NOT include explanations.
Do NOT wrap in markdown.
If missing, use null.

Schema:
{
  "is_event": boolean, // true ONLY if the email is announcing a specific upcoming event, workshop, or gathering. false for newsletters, receipts, account creations, etc.
  "name": string,
  "description": string,
  "location": string,
  "start_date_time": string,
  "duration": string,
  "food": string
}
"""

    prompt = ASK_GEMINI + text

    response = await client.aio.models.generate_content(
        model="gemini-2.0-flash-lite-preview-02-05", contents=prompt # chose the model here
    )

    response_json = json.loads(response.text)

    return response_json
