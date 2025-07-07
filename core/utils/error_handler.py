# 5. Error Handling Wrapper
import time

def retry(func, retries=3, delay=2):
    for i in range(retries):
        try:
            return func()
        except Exception as e:
            print(f"Retry {i+1}/{retries} failed: {e}")
            time.sleep(delay)
    raise Exception("All retries failed")
