def send_slack_message(message: str) -> bool:
    """
    Send a request to a human via Slack.
    
    Args:
        request (SlackRequest): The request containing message, channel, and user info
        
    Returns:
        bool: True if message was sent successfully, False otherwise
    """
    import logging
    import os
    from slack_sdk import WebClient
    from slack_sdk.errors import SlackApiError

    logger = logging.getLogger(__name__)
    # Get token from environment variables
    slack_token = os.environ.get("SLACK_BOT_TOKEN")
    if not slack_token:
        logger.error("SLACK_BOT_TOKEN not found in environment variables")
        return False

    # Initialize the Slack client
    client = WebClient(token=slack_token)

    channel = os.environ.get("SLACK_CHANNEL")
    if not channel:
        logger.error("SLACK_CHANNEL not found in environment variables")
        return False
    
    user = os.environ.get("SLACK_USER")
    if not user:
        logger.error("SLACK_USER not found in environment variables")
        return False

    try:
        # Send message to Slack
        result = client.chat_postMessage(
            channel=channel,
            text=message,
            user=user
        )
        logger.info(f"Message sent successfully: {result}")
        return True

    except SlackApiError as e:
        logger.error(f"Error posting message: {e}")
        return False
    
    # add a listening tool to listen for a response

    try:
        response = client.chat_listen()
    except SlackApiError as e:
        logger.error(f"Error listening for response: {e}")
        return False
