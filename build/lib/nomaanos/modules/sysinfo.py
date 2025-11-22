import platform, time, json

def run():
    info = {
        "project": "NomaanOS",
        "time": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "user": "unknown",
        "python": platform.python_version(),
        "platform": platform.platform(),
    }

    return json.dumps(info)
