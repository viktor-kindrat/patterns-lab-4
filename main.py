import yaml

from src.downloader import DataDownloader
from src.reader import DataReader
from src.context import DataOutputContext
from strategy_factory import create_strategy


def load_config(path: str = "config/config.yaml") -> dict:
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def main() -> None:
    config = load_config()

    downloader = DataDownloader(config["data"])
    downloader.ensure_downloaded()

    reader = DataReader(config["data"]["file"])
    records = reader.read(limit=config["output"]["limit"])

    strategy = create_strategy(config)
    context = DataOutputContext(strategy)
    context.execute_output(records)


if __name__ == "__main__":
    main()
