from typing import Any, Optional
from collections import OrderedDict
from datetime import datetime, timedelta
import threading

class MemoryCache:
    def __init__(self, max_size: int = 1000, ttl_seconds: int = 3600):
        self.max_size = max_size
        self.ttl_seconds = ttl_seconds
        self.cache = OrderedDict()
        self.timestamps = {}
        self.lock = threading.Lock()
    
    def get(self, key: str) -> Optional[Any]:
        with self.lock:
            if key not in self.cache:
                return None
            
            if self._is_expired(key):
                del self.cache[key]
                del self.timestamps[key]
                return None
            
            self.cache.move_to_end(key)
            return self.cache[key]
    
    def set(self, key: str, value: Any):
        with self.lock:
            if key in self.cache:
                self.cache.move_to_end(key)
                self.cache[key] = value
                self.timestamps[key] = datetime.now()
                return
            
            if len(self.cache) >= self.max_size:
                oldest_key = next(iter(self.cache))
                del self.cache[oldest_key]
                del self.timestamps[oldest_key]
            
            self.cache[key] = value
            self.timestamps[key] = datetime.now()
    
    def _is_expired(self, key: str):
        if key not in self.timestamps:
            return True
        age = datetime.now() - self.timestamps[key]
        return age > timedelta(seconds=self.ttl_seconds)