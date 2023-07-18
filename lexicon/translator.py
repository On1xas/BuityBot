from fluentogram import TranslatorHub, FluentTranslator
from fluent_compiler.bundle import FluentBundle


translator_hub = TranslatorHub(
        {
            "ru": ("ru", "en"),
            "en": ("en", "ru")
        },
        [
            FluentTranslator("en", translator=FluentBundle.from_files(locale="en-US", filenames=[r"lexicon/en/en.ftl"])),
            FluentTranslator("ru", translator=FluentBundle.from_files(locale="ru", filenames=[r"lexicon/ru/ru.ftl"]))
        ],
    )