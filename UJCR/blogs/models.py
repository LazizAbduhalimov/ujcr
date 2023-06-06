from enum import Enum

import qrcode
from io import BytesIO
from django.core.files import File
from PIL import Image, ImageDraw

from ckeditor.fields import RichTextField
from django.db import models
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils.timezone import now
from django_countries.fields import CountryField
from pytils.templatetags.pytils_translit import slugify

from profiles.models import AuthorsProfile, ReviewersProfile
from ujcr.settings import MEDIA_ROOT


class ArticleStatusEnum(str, Enum):
    draft = "черновик"
    reviewing = "рецензируется"
    rejected = "отклонено"
    accepted = "принят"
    published = "опубликован"


article_status_choices = [
    (ArticleStatusEnum.draft.value, 'Черновик'),
    (ArticleStatusEnum.reviewing.value, 'Рецензируется'),
    (ArticleStatusEnum.rejected.value, 'Отклонено'),
    (ArticleStatusEnum.accepted.value, 'Принят'),
    (ArticleStatusEnum.published.value, 'Опубликован'),
]


class DegreeEnum(str, Enum):
    no_degree = "Нет степени"


degree_choices = [
    (DegreeEnum.no_degree.value, 'Нет степени'),
]


class RankEnum(str, Enum):
    no_rank = "Нет звания"


rank_choices = [
    (RankEnum.no_rank.value, 'Активный'),
]


class State(models.Model):
    title = models.CharField("Название статуса", max_length=150)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Статус"
        verbose_name_plural = "Статусы"


class Tags(models.Model):
    title = models.CharField("Ключевое слово", max_length=150)
    related_articles_number = models.IntegerField("Количество связанных статей", default=0)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Ключевое слово"
        verbose_name_plural = "Ключевые слова"

        ordering = ["title"]


class Authors(models.Model):
    linked_profile = models.ForeignKey(AuthorsProfile, verbose_name="Профиль регистрации", on_delete=models.DO_NOTHING,
                                       related_name="profile", null=True)
    first_name = models.CharField("Имя", max_length=70, default="")
    last_name = models.CharField("Фамилия", max_length=70, default="")
    middle_name = models.CharField("Отчество", max_length=70, default="")
    country = CountryField(verbose_name="Страна", default="UZ")
    city = models.CharField("Город", max_length=100, default="")
    institution = models.CharField("Учреждение", max_length=255, default="")
    department = models.CharField("Кафедра. отделение", max_length=255, default="")
    post = models.CharField("Должность", max_length=255, default="")
    degree = models.CharField("Степень", max_length=30, default="", choices=degree_choices)
    rank = models.CharField("Звание", max_length=30, default="", choices=rank_choices)

    orcid = models.CharField("ORCID", max_length=100, default="")
    scopus_id = models.CharField("Scopus id", max_length=100, default="")
    wos_id = models.CharField("Wos id", max_length=100, default="")
    spin_code_e_library = models.CharField("Spin code e-library", max_length=100, default="")

    slug = models.SlugField("Slug автора", max_length=200, null=True, unique=True)

    def get_absolute_url(self):
        return reverse('author-detail', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('author-update', kwargs={'slug': self.slug})

    def get_full_name(self):
        return "{} {} {}".format(self.last_name, self.first_name, self.middle_name)

    def get_initials(self):
        return "{}.{}. {}".format(self.last_name[0], self.first_name[0], self.middle_name)

    def save(self, *args, **kwargs):
        if self.pk is None:
            try:
                self.pk = Authors.objects.order_by("pk").last().pk + 1
            except AttributeError:
                self.pk = 1

        self.slug = slugify("{}-{}-{}-{}".format(self.last_name, self.first_name, self.middle_name, self.pk))
        super(Authors, self).save(*args, **kwargs)

    def __str__(self):
        return self.get_full_name()

    class Meta:
        verbose_name = "Автора"
        verbose_name_plural = "Авторы"

        ordering = ["last_name"]


def create_qrcode(model):
    url = MEDIA_ROOT.replace("\\", "/") + "/" + str(model.file)
    qrcode_image = qrcode.make(url)
    canvas = Image.new("RGB", (qrcode_image.pixel_size, qrcode_image.pixel_size), "white")
    canvas.paste(qrcode_image)
    file_name = f"qrcode-{model.slug}.png"
    buffer = BytesIO()
    canvas.save(buffer, "PNG")
    model.qr.save(file_name, File(buffer), save=False)
    canvas.close()


class Volume(models.Model):
    title = models.CharField("Название тома", max_length=255, default="Том")
    doi = models.CharField("DOI ссылка", max_length=255, default="")
    file = models.FileField("Файл (PDF)", upload_to="files/Volume/", blank=True, null=True)
    published_date = models.DateField("Дата публикации", default=now, editable=True)
    qr = models.ImageField("QR-код", upload_to="images/volumes/QR/", blank=True)

    slug = models.SlugField("Slug тома", max_length=200, blank=True, null=True)
    status = models.ForeignKey(State, verbose_name="Статус", on_delete=models.DO_NOTHING)
    status_str = models.CharField("Строка статуса", blank=True, max_length=100)

    def get_absolute_url(self):
        return reverse('issue-detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        self.status_str = str(self.status)
        self.slug = slugify(self.title)

        # Создание и сохранение qr-code
        if not self.qr:
            create_qrcode(self)

        # При статусе Неактивынй отключаем все связанные Статьи, а иначе включаем их
        if self.status_str == "Неактивный" or self.status_str == "Следующий":
            if self.status_str == "Следующий":
                for i in Volume.objects.exclude(title=self.title).filter(status_str="Следующий"):
                    i.status = State.objects.get(title="Активный")
                    i.save()

            for i in Article.objects.filter(linked_volume=self):
                i.is_active = False
                i.save()
        else:
            for i in Article.objects.filter(linked_volume=self):
                i.is_active = True
                i.save()

        # Если модель получит статус Активный то другая модель с таким же статусом станет Архивной
        if self.status_str == "Активный":

            for i in Volume.objects.exclude(title=self.title).filter(status_str="Активный"):
                i.status = State.objects.get(title="Архивный")
                i.save()

        super(Volume, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    def admin_image(self):

        if self.qr:
            return mark_safe(
                u'<a href="{0}" target="_blank"><img src="{0}" width="100" /></a>'.format(self.qr.url))
        else:
            return 'Image Not Found'

    admin_image.short_description = 'QR-код'
    admin_image.allow_tags = True

    class Meta:
        verbose_name = "Том"
        verbose_name_plural = "Тома"
        ordering = ["-published_date"]


class ArticleSection(models.Model):
    position = models.IntegerField(default=0)
    title = models.CharField("Название раздела", max_length=255, default="")

    class Meta:
        verbose_name = "Раздел"
        verbose_name_plural = "Разделы статьи"

        ordering = ["position"]

    def __str__(self):
        return  self.title


class UniqueViewers(models.Model):
    user_id = models.CharField("ID", max_length=255)

    def __str__(self):
        return str(self.user_id)

    class Meta:
        verbose_name = "Уникального пользователя"
        verbose_name_plural = "Уникальные пользователи"


class Article(models.Model):
    position = models.IntegerField(default=0)
    slug = models.SlugField("Slug статьи", max_length=200, blank=True)

    udk = models.CharField("УДК", max_length=255, default="")
    specialization = models.CharField("Специальность", max_length=70, default="")
    title = models.CharField("Заголовок статьи", max_length=255, default="")
    annotation = RichTextField("Аннотация", default="")
    for_quoting = RichTextField("Для цитирования", default="", blank=True, null=True)
    literature = RichTextField("Литература", default="", blank=True, null=True)

    doi = models.CharField("DOI ссылка", max_length=255, default="", null=True)
    file = models.FileField("Файл (PDF)", upload_to="files/Article/", null=True)

    linked_volume = models.ForeignKey(Volume, verbose_name="Связанный том", null=True, on_delete=models.DO_NOTHING)
    type = models.ForeignKey(ArticleSection, verbose_name="Раздел", null=True, on_delete=models.DO_NOTHING)
    profile_author = models.ForeignKey(AuthorsProfile, verbose_name="Связанные Авторы", related_name='authors',
                                       blank=True, null=True, on_delete=models.DO_NOTHING)
    authors = models.ManyToManyField(Authors, verbose_name="Связанные Авторы", related_name='authors', blank=True)
    tags = models.ManyToManyField(Tags, verbose_name="Ключевые слова", related_name='tags')
    tags_text = models.CharField("Ключевые слова", max_length=255, default="")

    created_date = models.DateTimeField("Дата создания", auto_now_add=True)
    updated_date = models.DateTimeField("Дата последнего изменения", auto_now=True)
    upload_to_review_date = models.DateTimeField("Дата отправки на рассмотрение", auto_now=True)
    published_date = models.DateField("Дата публикации", default=now, editable=True)
    status = models.CharField("Статус", max_length=100, default=ArticleStatusEnum.draft,
                              choices=article_status_choices)
    is_draft = models.BooleanField("Черновик", default=True)

    viewers = models.ManyToManyField(UniqueViewers, verbose_name="Просмотры", related_name="viewers")

    def get_absolute_url(self):
        return reverse('article', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('article-update', kwargs={'slug': self.slug})

    def get_review_url(self):
        return reverse('article-review', kwargs={'int': self.pk})

    def cut_title(self):

        if self.title:
            from django.utils.safestring import mark_safe
            return mark_safe(
                f'{self.title[:50]}...'
            )
        else:
            return 'Text Not Found'

    title.short_description = 'Аннотация'

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Статью"
        verbose_name_plural = "Статьи"

        ordering = ["published_date", "title"]


class Comment(models.Model):
    reviewer = models.ForeignKey(
        ReviewersProfile,
        verbose_name="Рецензент",
        on_delete=models.CASCADE,
        related_name='user_comment',
        null=True
    )
    article = models.ForeignKey(Article, verbose_name="Статья", on_delete=models.CASCADE, related_name="comment_article")
    response_file = models.FileField("Файл рецензии", upload_to="files/Article/response/", null=True)
    published_date = models.DateTimeField("Время комментирования", editable=False, auto_now=True)
    is_recommended = models.BooleanField("Принять в публикацию", default=False)

    # def save(self, *args, **kwargs):
    #     super(Comment, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('article-update-review', kwargs={'pk': self.pk})

    def __str__(self):
        return f'{self.reviewer}-{self.article_id}'

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
        ordering = ['-published_date']
