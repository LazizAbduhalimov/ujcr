from modeltranslation.translator import register, TranslationOptions
from .models import Volume, Article, Authors, ArticleSection, Tags


@register(Volume)
class VolumeTranslationOptions(TranslationOptions):
    fields = ("title", "file")


@register(Article)
class ArticleTranslationOptions(TranslationOptions):
    fields = ("title", "annotation", "file", "for_quoting", "literature",)


@register(Authors)
class AuthorsTranslationOptions(TranslationOptions):
    fields = ("first_name", "last_name", "middle_name")


@register(ArticleSection)
class AuthorsTranslationOptions(TranslationOptions):
    fields = ("title",)


@register(Tags)
class AuthorsTranslationOptions(TranslationOptions):
    fields = ("title",)
