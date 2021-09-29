import sys
import time


def get_local_time():
    t = time.localtime()
    return f"{t.tm_hour}:{t.tm_min}:{t.tm_sec}"


def log(message):
    print(f"[{get_local_time()}] [Bot/Info] {message}")


def errlog(message):
    print(f"[{get_local_time()}] [Bot/Error] {message}", file=sys.stderr)
