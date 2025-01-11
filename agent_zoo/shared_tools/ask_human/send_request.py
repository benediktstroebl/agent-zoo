import logging
import os
from pydantic import BaseModel
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

logger = logging.getLogger(__name__)

class SlackRequest(BaseModel):
    message: str
    channel: str
    user: str

def send_slack_message(request: SlackRequest) -> bool:
    """
    Send a request to a human via Slack.
    
    Args:
        request (SlackRequest): The request containing message, channel, and user info
        
    Returns:
        bool: True if message was sent successfully, False otherwise
    """
    # Get token from environment variables
    slack_token = os.environ.get('SLACK_BOT_TOKEN')
    if not slack_token:
        logger.error("SLACK_BOT_TOKEN not found in environment variables")
        return False

    # Initialize the Slack client
    client = WebClient(token=slack_token)

    try:
        # Send message to Slack
        result = client.chat_postMessage(
            channel=request.channel,
            text=request.message,
            user=request.user
        )
        logger.info(f"Message sent successfully: {result}")
        return True

    except SlackApiError as e:
        logger.error(f"Error posting message: {e}")
        return False