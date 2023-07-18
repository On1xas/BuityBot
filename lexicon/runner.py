from typing import TYPE_CHECKING

from fluentogram import AttribTracer


class StubsTranslatorRunner(AttribTracer):
    def __init__(self, separator: str = '-'):
        super().__init__()
        self.separator = separator
        self.kwargs = {}

    def __call__(self, **kwargs) -> tuple[str, dict]:
        out = self._get_request_line()[:-1], kwargs
        self.request_line = ''
        return out


runner: StubsTranslatorRunner = StubsTranslatorRunner()

# if TYPE_CHECKING:
#     from stub import TranslatorRunner
#     runner: TranslatorRunner