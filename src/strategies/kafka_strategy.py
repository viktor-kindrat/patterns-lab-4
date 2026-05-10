import json
from .base import OutputStrategy


class KafkaOutputStrategy(OutputStrategy):
    def __init__(self, kafka_config: dict) -> None:
        from confluent_kafka import Producer

        self._topic = kafka_config["topic"]
        self._producer = Producer(
            {"bootstrap.servers": kafka_config["bootstrap_servers"]}
        )

    def output(self, records: list[dict]) -> None:
        print(f"[Kafka] Sending {len(records)} records to topic '{self._topic}'")
        for record in records:
            self._producer.produce(
                self._topic,
                value=json.dumps(record, ensure_ascii=False).encode("utf-8"),
            )
        self._producer.flush()
        print(f"[Kafka] Done. {len(records)} messages delivered.")
