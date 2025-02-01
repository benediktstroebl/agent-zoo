def send_slack_message(message: str) -> bool:
    """
    Send a request to a human via Slack.
    
    Args:
        request (Slack): The request containing message, channel, and user info
        
    Returns:
        bool: True if message was sent successfully, False otherwise
    """
    import logging
    import os
    from slack_sdk import WebClient
    from slack_sdk.errors import SlackApiError
    import time

    logger = logging.getLogger(__name__)
    # Get token from environment variables
    slack_token = os.environ.get("SLACK_BOT_TOKEN")
    if not slack_token:
        logger.error("SLACK_BOT_TOKEN not found in environment variables")
        return False

    # Initialize the Slack client
    client = WebClient(token=slack_token)

    channel = os.environ.get("SLACK_CHANNEL_ID")
    if not channel:
        logger.error("SLACK_CHANNEL_ID not found in environment variables")
        return False
    
    user = os.environ.get("SLACK_CLIENT_ID")
    if not user:
        logger.error("SLACK_CLIENT_ID not found in environment variables")
        return False

    try:
        
        # Send message to Slack
        sent_message = client.chat_postMessage(
            channel=channel,
            text=message.replace("""{"message":""", "").rstrip("}"),
            user=user
        )
        logger.info(f"Message sent successfully: {sent_message}")
        
        # Get the timestamp of the sent message
        sent_ts = sent_message["ts"]
        
        # Wait for response
        while True:
            # Get replies to our specific message
            result = client.conversations_replies(
                channel=channel,
                ts=sent_ts,  # This gets replies to our specific message
                limit=1  # We only need the most recent reply
            )
            
            # Check replies
            messages = result.get("messages", [])
            if len(messages) > 1:  # First message is our original message
                # Return the first reply
                return messages[1]["text"]
            
            # Wait 3 seconds before checking again
            time.sleep(3)

    except SlackApiError as e:
        logger.error(f"Error posting message: {e}")
        return f"Error receiving message: {e}"
