
from aiogram import F
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.common import WhenCondition
from aiogram_dialog.widgets.text import Text
from fluentogram import TranslatorRunner


class FluentText(Text):
    def __init__(self, key: str | tuple[str, dict[str, F]], when: WhenCondition = None):
        super().__init__(when=when)
        self.key: str = key[0]
        self.kwargs: dict[str, F] = key[-1]  # type: ignore

    def _resolve_kwargs(self, data: dict) -> dict:
        if not self.kwargs:
            return data
        out: dict = data.copy()
        in_: dict[str, F] = self.kwargs.copy()
        for key, value in in_.items():
            out[key] = value.resolve(data)
        return out

    async def _render_text(
            self, data: dict, manager: DialogManager,
    ) -> str:
        runner: TranslatorRunner = manager.middleware_data['i18n']
        return runner.get(self.key, **self._resolve_kwargs(data))
