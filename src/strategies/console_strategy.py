from .base import OutputStrategy


class ConsoleOutputStrategy(OutputStrategy):
    def __init__(self) -> None:
        self._last_records: list[dict] = []

    def output(self, records: list[dict]) -> None:
        self._last_records = records
        self._print_records(records)

    def view(self) -> None:
        if not self._last_records:
            print("[Console] No records in memory. Run without --view first.")
            return
        print(f"[Console] Showing {len(self._last_records)} records from last output\n" + "-" * 60)
        self._print_records(self._last_records)

    def _print_records(self, records: list[dict]) -> None:
        print(f"[Console] Outputting {len(records)} records\n" + "-" * 60)
        for i, record in enumerate(records, 1):
            print(f"Record #{i}")
            for key, value in record.items():
                print(f"  {key}: {value}")
            print()
