from src.strategies.base import OutputStrategy
from src.strategies.console_strategy import ConsoleOutputStrategy
from src.strategies.kafka_strategy import KafkaOutputStrategy
from src.strategies.redis_strategy import RedisOutputStrategy


def create_strategy(config: dict) -> OutputStrategy:
    name = config["output"]["strategy"]
    match name:
        case "console":
            return ConsoleOutputStrategy()
        case "kafka":
            return KafkaOutputStrategy(config["kafka"])
        case "redis":
            return RedisOutputStrategy(config["redis"])
        case _:
            raise ValueError(f"Unknown output strategy: '{name}'. Valid options: console, kafka, redis")
