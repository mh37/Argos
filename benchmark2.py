import timeit
import hashlib
from typing import Dict, Any, List, Set, Optional

class FrameHandlerBefore:
    def __init__(self):
        self.seen: List[str] = []

    def addSeen(self, info: Dict[str, Any]):
        try:
            identifier = f"{info['device']}{info['ssid']}"
            self.seen.append(hashlib.md5(identifier.encode('utf-8')).hexdigest())
        except Exception:
            pass

    def checkDuplicate(self, info: Dict[str, Any]) -> bool:
        try:
            identifier = f"{info['device']}{info['ssid']}"
            return hashlib.md5(identifier.encode('utf-8')).hexdigest() in self.seen
        except Exception:
            return True

class FrameHandlerAfter:
    def __init__(self):
        self.seen: Set[str] = set()

    def addSeen(self, info: Dict[str, Any], computed_hash: Optional[str] = None):
        try:
            if computed_hash is None:
                identifier = f"{info['device']}{info['ssid']}"
                computed_hash = hashlib.md5(identifier.encode('utf-8')).hexdigest()
            self.seen.add(computed_hash)
        except Exception:
            pass

    def checkDuplicate(self, info: Dict[str, Any], computed_hash: Optional[str] = None) -> bool:
        try:
            if computed_hash is None:
                identifier = f"{info['device']}{info['ssid']}"
                computed_hash = hashlib.md5(identifier.encode('utf-8')).hexdigest()
            return computed_hash in self.seen
        except Exception:
            return True

def run_bench():
    infos = [{"device": f"00:11:22:33:44:{i%100:02x}", "ssid": f"Network_{i%100}"} for i in range(1000)]

    def test_before():
        handler = FrameHandlerBefore()
        for info in infos:
            if not handler.checkDuplicate(info):
                handler.addSeen(info)

    def test_after():
        handler = FrameHandlerAfter()
        for info in infos:
            identifier = f"{info['device']}{info['ssid']}"
            computed_hash = hashlib.md5(identifier.encode('utf-8')).hexdigest()
            if not handler.checkDuplicate(info, computed_hash):
                handler.addSeen(info, computed_hash)

    import time

    t0 = time.time()
    for _ in range(100):
        test_before()
    t1 = time.time()

    t2 = time.time()
    for _ in range(100):
        test_after()
    t3 = time.time()

    print(f"Before: {t1-t0:.4f}s")
    print(f"After: {t3-t2:.4f}s")
    print(f"Improvement: {((t1-t0)-(t3-t2))/(t1-t0)*100:.2f}%")

if __name__ == '__main__':
    run_bench()
