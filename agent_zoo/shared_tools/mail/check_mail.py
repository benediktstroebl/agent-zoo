def check_mail(): 
    """
    check the mail for the agent. 
    """
<<<<<<< HEAD
    workspace_dir = os.getenv('WORKSPACE_DIR')
    agent_name = os.getenv('AGENT_NAME')
    mail_dir = os.getenv('MAIL_DIRECTORY')
    mail_path = os.path.join(workspace_dir, agent_name, mail_dir, 'mail.txt')
    with open(mail_path, 'r') as f:
=======
    import os 
    workspace_dir = os.getenv("WORKSPACE_DIR")
    agent_name = os.getenv("AGENT_NAME")
    mail_dir = os.getenv("MAIL_DIRECTORY")
    mail_path = os.path.join(workspace_dir, agent_name, mail_dir, "mail")
    with open(mail_path, "r") as f:
>>>>>>> 333827d90f406c2e5a42617b100a4afd47a9f621
        mail = f.read()
    return mail 