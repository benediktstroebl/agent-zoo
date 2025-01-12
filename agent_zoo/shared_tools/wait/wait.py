def wait(minutes: int):
    """
    Wait for a given number of minutes. 
    """
    import time
    time.sleep(minutes * 60)
    return "Waited for " + str(minutes) + " minutes"