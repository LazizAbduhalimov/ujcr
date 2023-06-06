from django.contrib import admin

from .models import *
from modeltranslation.admin import TabbedTranslationAdmin


@admin.register(State)
class AdminState(admin.ModelAdmin):
    list_display = [
        "title",
    ]
    list_per_page = 15


@admin.register(Authors)
class AdminAuthors(TabbedTranslationAdmin):
    list_display = [
        "first_name",
        "last_name",
        "middle_name",
        "slug",
    ]
    readonly_fields = ["slug"]
    list_per_page = 50


@admin.register(Volume)
class AdminVolume(TabbedTranslationAdmin):
    list_display = [
        "title",
        "get_doi_color",
        "admin_image",
        "slug",
        "get_status_color",
    ]

    readonly_fields = ["status_str", "slug"]

    def get_doi_color(self, object):
        return mark_safe(f"<span style='color: DarkGray;'><italic>{object.doi}</italic></span>")

    def get_status_color(self, object):
        if str(object.status) == "Неактивный":
            print("!")
            return mark_safe(f"<span style='color: red'><strong>{object.status}</strong></span>")
        elif str(object.status) == "Активный":
            return mark_safe(f"<span style='color: Lime'><strong>{object.status}</strong></span>")
        elif str(object.status) == "Архивный":
            return mark_safe(f"<span style='color: DodgerBlue'><strong>{object.status}</strong></span>")
        elif str(object.status) == "Следующий":
            return mark_safe(f"<span style='color: DarkOrange'><strong>{object.status}</strong></span>")
        else:
            return object.status

    get_doi_color.short_description = "DOI"
    get_status_color.short_description = "Статус"

    list_per_page = 15


@admin.register(Tags)
class AdminTags(TabbedTranslationAdmin):
    list_display = [
        "title",
        "related_articles_number"
    ]
    readonly_fields = ["related_articles_number"]
    list_per_page = 50


@admin.register(ArticleSection)
class AdminArticleSection(TabbedTranslationAdmin):
    list_display = ["title", "position"]
    list_editable = ["position"]
    list_per_page = 50


@admin.register(Article)
class AdminArticle(TabbedTranslationAdmin):
    list_display = [
        "cut_title",
        "doi",
        "published_date",
        "slug"
    ]
    # filter_horizontal = ["authors",]
    prepopulated_fields = {"slug": ("title",)}
    exclude = ["viewers"]
    actions = ["publish"]

    list_filter = ["linked_volume", "type"]
    list_per_page = 15

    def publish(self, request, queryset):
        row_update = queryset.update(status=ArticleStatusEnum.published.value)
        if row_update == "1":
            msg = "1 запись была обновлена"
        else:
            msg = f"{row_update} записей были обновлены"

        self.message_user(request, f"{msg}")

    publish.short_description = "Опубликовать"
    publish.allowed_permissions = ("change",)


@admin.register(UniqueViewers)
class AdminPartner(admin.ModelAdmin):
    list_display = [
        "user_id",
    ]
    list_per_page = 50


@admin.register(Comment)
class AdminPartner(admin.ModelAdmin):
    list_display = [
        "reviewer",
        "article",
    ]
    list_per_page = 50