import json
from database import config

def config(filename: str = "config"):
    """ Fetch default config file """
    try:
        with open(f"{filename}.json", encoding='utf8') as data:
            return json.load(data)
    except FileNotFoundError:
        raise FileNotFoundError("JSON file wasn't found")

def responsible(target, reason):
    """ Default responsible maker targeted to find user in AuditLogs """

    responsible = f"[{target}]"
    if not reason:
        return f"{responsible} no reason given..."
    return f"{responsible} {reason}"
