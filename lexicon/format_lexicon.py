from typing import Any, Dict, Protocol

from aiogram_dialog.api.protocols import DialogManager
from aiogram_dialog.widgets.common import WhenCondition
from aiogram_dialog.widgets.text import Text

from fluentogram import TranslatorRunner

I18N_FORMAT_KEY = "i18n"


class Values(Protocol):
    def __getitem__(self, item: Any) -> Any:
        raise NotImplementedError


def default_format_text(text: str, data: Values) -> str:
    return text.format_map(data)


class I18NFormat(Text):
    def __init__(self, text: str, when: WhenCondition = None):
        super().__init__(when)
        self.text = text

    async def _render_text(self, data: Dict, manager: DialogManager) -> str:
        format_text = manager.middleware_data.get(
            I18N_FORMAT_KEY, default_format_text,
        )
        return format_text(self.text, data)

class FluentKey:
    def __init__(self, key: str):
        self.key = key

    async def __call__(self, manager: DialogManager):
        translator: TranslatorRunner = manager.middleware_data.get("i18n")
        return translator.get(key=self.key)

