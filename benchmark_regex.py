import timeit
import json
import re

class LazyDecoderBefore(json.JSONDecoder):
    def decode(self, s, **kwargs):
        regex_replacements = [
            (re.compile(r'([^\\])\\([^\\])'), r'\1\\\\\2'),
            (re.compile(r',(\s*])'), r'\1'),
        ]
        for regex, replacement in regex_replacements:
            s = regex.sub(replacement, s)
        return super().decode(s, **kwargs)

class LazyDecoderAfter(json.JSONDecoder):
    REGEX_REPLACEMENTS = [
        (re.compile(r'([^\\])\\([^\\])'), r'\1\\\\\2'),
        (re.compile(r',(\s*])'), r'\1'),
    ]
    def decode(self, s, **kwargs):
        for regex, replacement in self.REGEX_REPLACEMENTS:
            s = regex.sub(replacement, s)
        return super().decode(s, **kwargs)

def run_bench():
    # Example JSON string with things to replace
    s = '{"key1": "value1 \\ value2", "key2": [1, 2, ], "key3": "regular string"}'

    decoder_before = LazyDecoderBefore()
    decoder_after = LazyDecoderAfter()

    import time

    t0 = time.time()
    for _ in range(100000):
        decoder_before.decode(s)
    t1 = time.time()

    t2 = time.time()
    for _ in range(100000):
        decoder_after.decode(s)
    t3 = time.time()

    print(f"Before: {t1-t0:.4f}s")
    print(f"After: {t3-t2:.4f}s")
    print(f"Improvement: {((t1-t0)-(t3-t2))/(t1-t0)*100:.2f}%")

if __name__ == '__main__':
    run_bench()
