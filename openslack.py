import os
from slack_sdk import WebClient
import openai

slack_token_user = "xoxp-5417079717520-5390435807605-5379016664439-aa5c73e0aa5691fa2a980937c503bb4a"  # Set your Slack OAuth access token here
slack_token_bot = "xoxb-5417079717520-5393356374355-T3AM05zT63f5pInOvfPEfXeW"

channel_id = "C05BK7F8UUT"  # Set the desired Slack channel ID here

foundUserClient = WebClient(token=slack_token_user)
botUserClient = WebClient(token=slack_token_bot)

response = foundUserClient.users_identity()
user_id = response["user"]["id"]

channel_info = foundUserClient.conversations_info(channel=channel_id)
channel_name = channel_info["channel"]["name"]

response2 = botUserClient.conversations_history(channel=channel_id)
messages = response2["messages"]

content = "\n".join([message["text"] for message in messages])
print(channel_name)
prompt = "Please provide a very short summary of the following channel of slack:\n\n" + content + "\n\n" + "I want the summary to have the title of the channel: " + channel_name

openai.api_key = "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"  # Set your OpenAI API key here

response = openai.Completion.create(
    engine="text-davinci-003",
    prompt=prompt,
    max_tokens=100,
    temperature=0.5
)

summary = response.choices[0].text.strip()

botUserClient.chat_postMessage(channel=user_id, text=summary)
