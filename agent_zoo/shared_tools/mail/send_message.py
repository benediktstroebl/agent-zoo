import os 

msg_template = """
Sender: {sender_name}

Message: {msg}
"""

def send_message(recipient_name, msg): 
    """
    send a message to the agent. 
    """
    sender_name = os.getenv('AGENT_NAME')
    mail_path = os.path.join('/scratch/gpfs/vv7118/projects/testing/', recipient_name + '.mail')
    with open(mail_path, 'w') as f:
        msg_template.format(sender_name=sender_name, msg=msg)
    return mail_path