from django import forms
from django.core.exceptions import ValidationError

from blogs.models import Article, Comment, Authors
from modeltranslation.forms import TranslationModelForm
from django.utils.translation import gettext_lazy as _


class ArticleCreateForm(TranslationModelForm):
    error_css_class = "alert alert-danger"

    def __init__(self, *args, **kwargs):
        profile = kwargs.pop('profile', None)
        super(ArticleCreateForm, self).__init__(*args, **kwargs)
        self.fields['authors'].queryset = Authors.objects.filter(linked_profile=profile)

    class Meta:
        model = Article
        fields = [
            "title",
            "annotation",
            "for_quoting",
            "doi",
            "file",
            "authors",
            "tags_text",
            "is_draft",
        ]
        widgets = {
            'title': forms.TextInput(attrs={"class": "form-control"}),
            'for_quoting': forms.Textarea(attrs={"class": "form-control", 'rows': 3}),
            'doi': forms.TextInput(attrs={"class": "form-control", }),
            'file': forms.FileInput(attrs={"class": "form-control", }),
            'linked_volume': forms.Select(attrs={"class": "form-control", }),
            'type': forms.Select(attrs={"class": "form-control", }),
            'authors': forms.SelectMultiple(attrs={"class": "select-1 form-control", "multiple": "multiple"}),
            'profile_author': forms.Select(attrs={"class": "form-control", }),
            'tags_text': forms.TextInput(attrs={"class": "form-control"}),
        }
        labels = {
            'authors': "Соавтроры",
            'tags_text': "Ключевые слова"
        }

    def clean_tags_text(self):
        tags_text = self.cleaned_data['tags_text']
        tags = str(tags_text).replace(" ", "").replace(";", ",").split(",")
        if len(tags) < 5:
            raise ValidationError(_("В статье должно быть более 5 ключевых слов"))
        return tags_text

    def clean_annotation(self):
        annotation = self.cleaned_data['annotation']
        if len(annotation.split()) < 200:
            raise ValidationError(_("Аннотация статьи должна содержать более 200 слов"))
        return annotation


class CommentCreateForm(TranslationModelForm):
    class Meta:
        model = Comment
        fields = [
            "response_file",
            "is_recommended",
        ]
        labels = {
            "response_file": _("Файл рецензии"),
            "is_recommended": _("Рекомендовать статью для публикации?")
        }

    def clean_response_file(self):
        response_file = self.cleaned_data['response_file']
        if str(response_file).endswith(".pdf"):
            return response_file

        raise ValidationError(_("Файл рецензии должен быть в формате pdf!"))


class AuthorCreateForm(TranslationModelForm):
    error_css_class = "alert alert-danger"

    class Meta:
        model = Authors
        fields = [
            "first_name",
            "last_name",
            "middle_name",
            "country",
            "city",
            "institution",
            "department",
            "post",
            "degree",
            "rank",
            "orcid",
            "scopus_id",
            "wos_id",
            "spin_code_e_library",
        ]

        widgets = {
            'first_name': forms.TextInput(attrs={"class": "form-control"}),
            'last_name': forms.TextInput(attrs={"class": "form-control"}),
            'middle_name': forms.TextInput(attrs={"class": "form-control"}),
            'country': forms.Select(attrs={"class": "form-control", }),
            'city': forms.TextInput(attrs={"class": "form-control"}),
            'institution': forms.TextInput(attrs={"class": "form-control"}),
            'department': forms.TextInput(attrs={"class": "form-control"}),
            'post': forms.TextInput(attrs={"class": "form-control"}),
            'degree': forms.Select(attrs={"class": "form-control", }),
            'rank': forms.Select(attrs={"class": "form-control", }),
            'orcid': forms.TextInput(attrs={"class": "form-control"}),
            'scopus_id': forms.TextInput(attrs={"class": "form-control"}),
            'wos_id': forms.TextInput(attrs={"class": "form-control"}),
            'spin_code_e_library': forms.TextInput(attrs={"class": "form-control"}),
        }
