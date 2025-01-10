def check_mail(mail_path): 
    """
    check the mail for the agent. 
    """
    with open(mail_path, 'r') as f:
        mail = f.read()
    return mail 