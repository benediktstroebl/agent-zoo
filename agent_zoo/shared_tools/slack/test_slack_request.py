import logging
import os
# Import WebClient from Python SDK (github.com/slackapi/python-slack-sdk)
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from dotenv import load_dotenv

load_dotenv()

# WebClient instantiates a client that can call API methods
# When using Bolt, you can use either `app.client` or the `client` passed to listeners.
client = WebClient(token=os.environ.get('SLACK_BOT_TOKEN'))
logger = logging.getLogger(__name__)

# ID of the channel you want to send the message to
channel_id = os.environ.get('SLACK_CHANNEL_ID')

try:
    # Call the chat.postMessage method using the WebClient
    result = client.chat_postMessage(
        channel=channel_id, 
        text="@stroebl test"
    )
    
    # Get conversation history after our message
    result = client.conversations_history(
        channel=channel_id,
        limit=1  # We only need the most recent messages
    )
    
    
    print(result)
    logger.info(result)

except SlackApiError as e:
    logger.error(f"Error posting message: {e}")