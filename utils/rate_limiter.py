import time

last_call = 0

def limit_requests(delay=1):
    global last_call
    now = time.time()
    
    if now - last_call < delay:
        time.sleep(delay - (now - last_call))
    
    last_call = time.time()