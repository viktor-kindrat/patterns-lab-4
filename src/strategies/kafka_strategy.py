import json
from .base import OutputStrategy


class KafkaOutputStrategy(OutputStrategy):
    def __init__(self, kafka_config: dict) -> None:
        from confluent_kafka import Producer

        self._config = kafka_config
        self._topic = kafka_config["topic"]
        self._bootstrap_servers = kafka_config["bootstrap_servers"]
        self._producer = Producer({
            "bootstrap.servers": self._bootstrap_servers,
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

    def view(self) -> None:
        from confluent_kafka import Consumer, KafkaError

        consumer = Consumer({
            "bootstrap.servers": self._bootstrap_servers,
            "group.id": "strategy-viewer",
            "auto.offset.reset": "earliest",
            "enable.auto.commit": False,
        })
        consumer.subscribe([self._topic])

        print(f"[Kafka] Reading messages from topic '{self._topic}'\n" + "-" * 60)
        count = 0
        empty_polls = 0
        while empty_polls < 3:
            msg = consumer.poll(timeout=2.0)
            if msg is None:
                empty_polls += 1
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    break
                print(f"[Kafka] Error: {msg.error()}")
                break
            empty_polls = 0
            count += 1
            record = json.loads(msg.value().decode("utf-8"))
            print(f"Record #{count}")
            for key, value in record.items():
                print(f"  {key}: {value}")
            print()

        consumer.close()
        print(f"[Kafka] Total records read: {count}")
