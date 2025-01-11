import os 

msg_template = """
=========================
Sender: {sender_name}

Message: {msg}

"""

def send_message(recipient_name, msg): 
    """
    send a message to the agent. 
    """
    sender_name = os.getenv('AGENT_NAME')
    workspace_dir = os.getenv('WORKSPACE_DIR')
    mail_dir = os.getenv('MAIL_DIR')
    mail_path = os.path.join(workspace_dir, mail_dir, 'mail')
    with open(mail_path, 'a') as f:
        msg_template = msg_template.format(sender_name=sender_name, msg=msg)
        f.write(msg_template)
    return mail_path