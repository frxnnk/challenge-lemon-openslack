import os
from dotenv import load_dotenv
from slack_sdk import WebClient
import openai

# Cargar las variables del archivo .env
load_dotenv()

TOKEN_USER = os.environ.get('TOKEN_USER')
TOKEN_BOT = os.environ.get('TOKEN_BOT')
KEY_OPENAI = os.environ.get('KEY_OPENAI')
CHANNEL_ID = os.environ.get('CHANNEL_ID')

userClient = WebClient(TOKEN_USER)
botClient = WebClient(TOKEN_BOT)

# Get user ID
response = userClient.users_identity()
user_id = response["user"]["id"]

# Set the desired Slack channel ID and get channel name
channel_id = CHANNEL_ID
channel_info = botClient.conversations_info(channel=channel_id)
channel_name = channel_info["channel"]["name"]

# Get channel messages
response = botClient.conversations_history(channel=channel_id)
messages = response["messages"]

# Create the content to summarize
content = "\n".join([message["text"] for message in messages])

# Create the prompt to resume the summary
prompt = f"Please provide a very short summary. Max 150 characters. The summary starts with the title: {channel_name}\n\nThe content to summarize is a channel slack conversation:\n\n{content}"

openai.api_key = KEY_OPENAI # Set your OpenAI API key here

response = openai.Completion.create(
    engine="text-davinci-003",
    prompt=prompt,
    max_tokens=100,
    temperature=0.5
)

# Resume the summary
summary = response.choices[0].text.strip()

# Send the summary to the private message channel of the user
botClient.chat_postMessage(channel=user_id, text=summary)
