import time
import timeit

def test_str_slice(data):
    return str(data)[2:-1]

def test_decode(data):
    return data.decode('utf-8')

# Mock data simulating a response body
mock_data = b'{"success": "True", "results": [{"trilat": 40.7128, "trilong": -74.0060}]}'

def run_bench():
    # Verify correctness
    assert test_str_slice(mock_data) == test_decode(mock_data)

    n = 1000000

    t0 = time.time()
    for _ in range(n):
        test_str_slice(mock_data)
    t1 = time.time()
    time_str = t1 - t0

    t0 = time.time()
    for _ in range(n):
        test_decode(mock_data)
    t1 = time.time()
    time_decode = t1 - t0

    print(f"str(data)[2:-1] time: {time_str:.4f}s")
    print(f"data.decode('utf-8') time: {time_decode:.4f}s")
    if time_decode < time_str:
        print(f"Improvement: {(time_str - time_decode) / time_str * 100:.2f}% faster")
    else:
        print(f"Improvement: {(time_decode - time_str) / time_str * 100:.2f}% slower")

if __name__ == '__main__':
    run_bench()
