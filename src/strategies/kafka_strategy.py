import json
from .base import OutputStrategy


class KafkaOutputStrategy(OutputStrategy):
    def __init__(self, kafka_config: dict) -> None:
        from confluent_kafka import Producer

        self._topic = kafka_config["topic"]
        self._producer = Producer({
            "bootstrap.servers": kafka_config["bootstrap_servers"],
            "socket.timeout.ms": 5000,
            "message.timeout.ms": 10000,
        })

    def output(self, records: list[dict]) -> None:
        delivered = 0
        failed = 0

        def _on_delivery(err, _msg):
            nonlocal delivered, failed
            if err:
                failed += 1
            else:
                delivered += 1

        print(f"[Kafka] Sending {len(records)} records to topic '{self._topic}'")
        for record in records:
            self._producer.produce(
                self._topic,
                value=json.dumps(record, ensure_ascii=False).encode("utf-8"),
                on_delivery=_on_delivery,
            )

        remaining = self._producer.flush(timeout=15)
        if remaining:
            print(f"[Kafka] Warning: {remaining} message(s) not delivered (broker unreachable?).")
        print(f"[Kafka] Done. delivered={delivered}, failed={failed}.")
