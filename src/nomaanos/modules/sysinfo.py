import os, platform, time, json

def main():
    info = {
        "os": platform.system(),
        "release": platform.release(),
        "python": platform.python_version(),
        "machine": platform.machine(),
        "uptime_sec": time.time() - ps_boot_time(),
        "cwd": os.getcwd()
    }
    print(json.dumps(info, indent=4))

def ps_boot_time():
    try:
        with open("/proc/stat") as f:
            for line in f:
                if line.startswith("btime"):
                    return float(line.split()[1])
    except:
        return time.time()
