import json
from .base import OutputStrategy


class RedisOutputStrategy(OutputStrategy):
    def __init__(self, redis_config: dict) -> None:
        import redis

        self._prefix = redis_config["key_prefix"]
        self._client = redis.Redis(
            host=redis_config["host"],
            port=redis_config["port"],
            decode_responses=True,
        )

    def output(self, records: list[dict]) -> None:
        print(f"[Redis] Storing {len(records)} records with prefix '{self._prefix}'")
        for i, record in enumerate(records):
            key = f"{self._prefix}:{i}"
            self._client.hset(key, mapping=record)
        print(f"[Redis] Done. {len(records)} hashes stored.")
