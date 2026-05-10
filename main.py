import argparse
import yaml

from src.downloader import DataDownloader
from src.reader import DataReader
from src.context import DataOutputContext
from src.strategies.console_strategy import ConsoleOutputStrategy
from strategy_factory import create_strategy


def load_config(path: str = "config/config.yaml") -> dict:
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def main() -> None:
    parser = argparse.ArgumentParser(description="GoF Strategy pattern — police cases output")
    parser.add_argument("--view", action="store_true", help="Read and display data from the configured storage")
    args = parser.parse_args()

    config = load_config()
    strategy = create_strategy(config)
    context = DataOutputContext(strategy)

    if args.view and not isinstance(strategy, ConsoleOutputStrategy):
        context.execute_view()
    else:
        downloader = DataDownloader(config["data"])
        downloader.ensure_downloaded()

        reader = DataReader(config["data"]["file"])
        records = reader.read(limit=config["output"]["limit"])

        context.execute_output(records)


if __name__ == "__main__":
    main()
