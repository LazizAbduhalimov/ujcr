from blogs.models import *
from main_app.models import *
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import six

from profiles.models import AuthorsProfile, ReviewersProfile


def get_or_none(class_model, **kwargs):
    try:
        return class_model.objects.get(**kwargs)
    except class_model.DoesNotExist:
        return None


class MenuMixin:

    def get_user_context(self, **kwargs):
        context = kwargs
        all_pages = Page.objects.all()
        context["links"] = all_pages.filter(linklocation__title="About us").select_related("linklocation")
        context["menu_links"] = all_pages.filter(linklocation__title="Menu").select_related("linklocation")
        context["side_bar_links"] = all_pages.filter(linklocation__title="Side bar").select_related("linklocation")

        context["next_volume"] = get_or_none(Volume, status_str="Следующий")
        context["current_volume"] = get_or_none(Volume, status_str="Активный")
        context["current_path"] = str(self.request.path)[3:]

        if self.request.user.is_authenticated:
            context["author_profile"] = get_or_none(AuthorsProfile, user=self.request.user)
            context["is_author"] = bool(context["author_profile"])

            context["reviewer_profile"] = get_or_none(ReviewersProfile, user=self.request.user)
            context["is_reviewer"] = bool(context["reviewer_profile"])

        return context


class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return(
            six.text_type(user.pk) + six.text_type(timestamp) +
            six.text_type(user.is_active)
        )


account_activation_token = TokenGenerator()
