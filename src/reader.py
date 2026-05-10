import csv


class DataReader:
    def __init__(self, file_path: str) -> None:
        self._file_path = file_path

    def read(self, limit: int | None = None) -> list[dict]:
        with open(self._file_path, encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            records = []
            for i, row in enumerate(reader):
                if limit is not None and i >= limit:
                    break
                records.append(dict(row))
        return records
