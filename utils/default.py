import json

def config(filename: str = "config"):
    try:
        with open(f"{filename}.json", encoding='utf8') as data:
            return json.load(data)
    except FileNotFoundError:
        raise FileNotFoundError("JSON file wasn't found")

def responsible(target, reason):
    responsible = f"[{target}]"
    if not reason:
        return f"{responsible} no reason given..."
    return f"{responsible} {reason}"
