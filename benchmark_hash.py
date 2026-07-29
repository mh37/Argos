import timeit
import hashlib

def current_hash(device, ssid):
    identifier = f"{device}{ssid}"
    return hashlib.sha256(identifier.encode('utf-8')).hexdigest()

def optimized_hash(device, ssid):
    return f"{device}{ssid}"

def benchmark():
    setup = "from __main__ import current_hash, optimized_hash; device='00:11:22:33:44:55'; ssid='MyWiFiNetwork'"

    current_time = timeit.timeit("current_hash(device, ssid)", setup=setup, number=1000000)
    optimized_time = timeit.timeit("optimized_hash(device, ssid)", setup=setup, number=1000000)

    print(f"Current Hash Time: {current_time:.4f} seconds")
    print(f"Optimized Hash Time: {optimized_time:.4f} seconds")
    print(f"Improvement: {current_time / optimized_time:.2f}x faster")

benchmark()
