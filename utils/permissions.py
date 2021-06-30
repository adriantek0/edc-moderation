from utils import default
config = default.config()

def check_mod(member):
    auth = False
    for role in member.roles:
        if role.id in config['mods']:
            auth = True

    if member.id in config['owners']:
        auth = True
    
    return auth

def check_roblox(member):
    auth = False
    for role in member.roles:
        if role.id in config['mods_roblox']:
            auth = True

    if member.id in config['owners']:
        auth = True
    
    return auth