from .base import OutputStrategy


class ConsoleOutputStrategy(OutputStrategy):
    def output(self, records: list[dict]) -> None:
        print(f"[Console] Outputting {len(records)} records\n" + "-" * 60)
        for i, record in enumerate(records, 1):
            print(f"Record #{i}")
            for key, value in record.items():
                print(f"  {key}: {value}")
            print()
