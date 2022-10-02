from blogs.models import *
from main_app.models import *
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import six

class MenuMixin:
    def get_user_context(self, **kwargs):
        context = kwargs
        context["links"] = Page.objects.filter(linklocation__title="About us")
        context["menu_links"] = Page.objects.filter(linklocation__title="Menu")

        context["side_bar_links"] = Page.objects.filter(linklocation__title="Side bar")
        try:
            context["next_volume"] = Volume.objects.filter(status_str="Следующий")[0]
        except:
            context["next_volume"] = None

        return context


class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return(
            six.text_type(user.pk) + six.text_type(timestamp) +
            six.text_type(user.is_active)
        )
account_activation_token = TokenGenerator()