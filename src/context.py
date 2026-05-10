from .strategies.base import OutputStrategy


class DataOutputContext:
    def __init__(self, strategy: OutputStrategy) -> None:
        self._strategy = strategy

    def set_strategy(self, strategy: OutputStrategy) -> None:
        self._strategy = strategy

    def execute_output(self, records: list[dict]) -> None:
        self._strategy.output(records)

    def execute_view(self) -> None:
        self._strategy.view()
