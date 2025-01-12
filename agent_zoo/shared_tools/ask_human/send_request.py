def send_slack_message(message: str) -> str:
    """
    Send a request to a human via Slack and wait for their response.
    
    Returns:
        str: The response message from the human, or empty string if no response received or error occurred
    """
    import logging
    import os
    import time
    from slack_sdk import WebClient
    from slack_sdk.errors import SlackApiError

    logger = logging.getLogger(__name__)
    # Get token from environment variables
    slack_token = os.environ.get("SLACK_BOT_TOKEN")
    if not slack_token:
        logger.error("SLACK_BOT_TOKEN not found in environment variables")
        return ""

    # Initialize the Slack client
    client = WebClient(token=slack_token)

    channel = os.environ.get("SLACK_CHANNEL")
    if not channel:
        logger.error("SLACK_CHANNEL not found in environment variables")
        return ""
    
    user = os.environ.get("SLACK_USER")
    if not user:
        logger.error("SLACK_USER not found in environment variables")
        return ""

    try:
        # Send message to Slack
        sent_message = client.chat_postMessage(
            channel=channel,
            text=message,
            user=user
        )
        logger.info(f"Message sent successfully: {sent_message}")
        
        # Get the timestamp of the sent message
        sent_ts = sent_message['ts']
        
        # Wait for response
        while True:
            # Get conversation history after our message
            result = client.conversations_history(
                channel=channel,
                oldest=sent_ts,
                limit=5  # We only need the most recent messages
            )
            
            # Check messages
            messages = result.get('messages', [])
            for msg in messages:
                # Skip our own message
                if msg['ts'] == sent_ts:
                    continue
                    
                # Return the first message that's not our original message
                return msg['text']
                
            # Wait 5 seconds before checking again
            time.sleep(5)

    except SlackApiError as e:
        logger.error(f"Error with Slack API: {e}")
        return ""
