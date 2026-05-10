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

    def view(self) -> None:
        pattern = f"{self._prefix}:*"
        keys = sorted(
            self._client.keys(pattern),
            key=lambda k: int(k.split(":")[-1]),
        )
        if not keys:
            print(f"[Redis] No records found for prefix '{self._prefix}'.")
            return

        print(f"[Redis] Reading {len(keys)} records with prefix '{self._prefix}'\n" + "-" * 60)
        for i, key in enumerate(keys, 1):
            record = self._client.hgetall(key)
            print(f"Record #{i}  (key: {key})")
            for field, value in record.items():
                print(f"  {field}: {value}")
            print()
        print(f"[Redis] Total records read: {len(keys)}")
