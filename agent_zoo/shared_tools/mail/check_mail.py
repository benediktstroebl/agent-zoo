import os 

def check_mail(): 
    """
    check the mail for the agent. 
    """
    workspace_dir = os.getenv('WORKSPACE_DIR')
    agent_name = os.getenv('AGENT_NAME')
    mail_dir = os.getenv('MAIL_DIR')
    mail_path = os.path.join(workspace_dir, mail_dir, 'mail')
    with open(mail_path, 'r') as f:
        mail = f.read()
    return mail 