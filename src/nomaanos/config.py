import json, os

CONFIG_FILE = "/root/nomaanos_config.json"

default_config = {
    "username": "Nomaan",
    "mode": "developer",
    "auto_backup": True
}

def load():
    if not os.path.exists(CONFIG_FILE):
        save(default_config)
    return json.load(open(CONFIG_FILE))

def save(cfg):
    json.dump(cfg, open(CONFIG_FILE, "w"), indent=4)
    return True
