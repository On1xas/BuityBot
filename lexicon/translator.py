from fluentogram import TranslatorHub, FluentTranslator
from fluent_compiler.bundle import FluentBundle


translator_hub = TranslatorHub(
        {
            "ru": ("ru", "en"),
            "en": ("en",)
        },
        [
            FluentTranslator("en", translator=FluentBundle.from_string("en-US", "start-hello = Hello, { $username }")),
            FluentTranslator("ru", translator=FluentBundle.from_string("ru", "start-hello = Привет, { $username }"))
        ],
    )