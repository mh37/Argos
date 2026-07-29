import time
import os
import json

class FrameHandlerBefore:
    def __init__(self, out):
        self.outFile = out

    def process_probe(self, message):
        if self.outFile is not None:
            with open(self.outFile, 'a') as file:
                file.write(message + "\n")

class FrameHandlerAfter:
    def __init__(self, out):
        self.outFile = out
        self.file = None
        if self.outFile:
            self.file = open(self.outFile, 'a')

    def process_probe(self, message):
        if self.file is not None:
            self.file.write(message + "\n")
            self.file.flush()

    def __del__(self):
        if self.file is not None:
            self.file.close()

def run_bench():
    messages = [json.dumps({"device": "00:11:22:33:44:55", "ssid": "TestNetwork", "location": [{"lat": 0.0, "lng": 0.0}]}) for _ in range(1000)]

    # Test Before
    if os.path.exists("test_out_before.txt"):
        os.remove("test_out_before.txt")
    handler_before = FrameHandlerBefore("test_out_before.txt")

    t0 = time.time()
    for msg in messages:
        handler_before.process_probe(msg)
    t1 = time.time()

    # Test After
    if os.path.exists("test_out_after.txt"):
        os.remove("test_out_after.txt")
    handler_after = FrameHandlerAfter("test_out_after.txt")

    t2 = time.time()
    for msg in messages:
        handler_after.process_probe(msg)
    t3 = time.time()

    print(f"Before: {t1-t0:.4f}s")
    print(f"After: {t3-t2:.4f}s")

    if os.path.exists("test_out_before.txt"): os.remove("test_out_before.txt")
    if os.path.exists("test_out_after.txt"): os.remove("test_out_after.txt")

if __name__ == '__main__':
    run_bench()
