from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect, FileResponse, HttpRequest
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.generic import ListView, DetailView
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse_lazy
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from .utils import account_activation_token

from blogs.models import Volume, Article, Tags, Authors, ArticleSection, ArticleStatusEnum
from main_app.forms import RegisterUserForm
from main_app.models import *
from main_app.utils import MenuMixin

from django.conf import settings
from django.views.decorators.cache import cache_control
from django.views.decorators.http import require_GET


@require_GET
@cache_control(max_age=60 * 60 * 24, immutable=True, public=True)
def favicon(request: HttpRequest):
    file = (settings.BASE_DIR / "static" / "favicon.ico").open("rb")
    return FileResponse(file)


def index(request):
    return HttpResponseRedirect("ru/home/")


class SamePages(MenuMixin, DetailView):
    model = Page
    template_name = "main_app/same_pages.html"
    slug_field = 'slug'

    def get_context_data(self, **kwargs):
        context = super(SamePages, self).get_context_data(**kwargs)
        slug = self.kwargs['slug']
        context["object"] = Page.objects.get(slug=slug)

        context["current_path"] = str(self.request.path)[3:]
        return dict(list(context.items()) + list(self.get_user_context().items()))


class Search(MenuMixin, ListView):
    template_name = "main_app/search.html"
    paginate_by = 20

    def get_queryset(self):
        if self.request.GET.get("q") != "" and 'tag' not in self.request.GET:
            queryset = Article.objects.filter(is_draft=False, status=ArticleStatusEnum.published.value ).filter(
                title__icontains=self.request.GET.get("q"))
            return queryset.distinct()

        queryset = Article.objects.filter(is_draft=False, status=ArticleStatusEnum.published.value)
        tags = self.request.GET.getlist("tag")
        print(self.request.GET.getlist("tag"))
        for tag in tags:
            queryset = queryset.filter(tags=tag)

        if self.request.GET.get("q") != "" and 'tag' in self.request.GET:
            queryset = queryset.filter(title__icontains=self.request.GET.get("q"))

        # distinct чтобы не было дубликаций модели
        return queryset.distinct()

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        if self.request.GET.get("q"):
            context["q"] = self.request.GET.get("q")
        else:
            context["q"] = ""

        for tag in Tags.objects.all():
            related_articles = Article.objects.filter(tags=tag)
            tag.related_articles_number = related_articles.count()
            tag.save()

        context["filter_tags"] = self.request.GET.getlist("tag")
        context["tags"] = Tags.objects.order_by("-related_articles_number")

        context["current_path"] = f"{str(self.request.path)[3:]}?q="
        return dict(list(context.items()) + list(self.get_user_context().items()))


class EditorialPage(MenuMixin, ListView):
    model = EditorialMember
    template_name = "main_app/editorial_page.html"

    def get_context_data(self, **kwargs):
        context = super(EditorialPage, self).get_context_data(**kwargs)
        context["posts"] = Post.objects.all()
        context["members"] = EditorialMember.objects.all()

        context["current_path"] = str(self.request.path)[3:]
        return dict(list(context.items()) + list(self.get_user_context().items()))


class EditorialMemberPage(MenuMixin, DetailView):
    model = EditorialMember
    template_name = "main_app/editorial_member_page.html"
    slug_field = 'slug'

    def get_context_data(self, **kwargs):
        context = super(EditorialMemberPage, self).get_context_data(**kwargs)
        slug = self.kwargs['slug']
        context["object"] = self.model.objects.get(slug=slug)

        context["current_path"] = str(self.request.path)[3:]
        return dict(list(context.items()) + list(self.get_user_context().items()))


class AuthorsPage(MenuMixin, ListView):
    model = Authors
    template_name = "main_app/authors.html"
    paginate_by = 10

    def get_queryset(self):
        if "/ru/" in self.request.path:
            queryset = self.model.objects.order_by("last_name_ru")
        else:
            queryset = self.model.objects.order_by("last_name_en")
        print(queryset)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(AuthorsPage, self).get_context_data(**kwargs)

        context["current_path"] = str(self.request.path)[3:]
        return dict(list(context.items()) + list(self.get_user_context().items()))


class AuthorsDetailPage(MenuMixin, DetailView):
    model = Authors
    template_name = "main_app/author's_articles.html"
    slug_field = "slug"

    def get_context_data(self, **kwargs):
        context = super(AuthorsDetailPage, self).get_context_data(**kwargs)
        slug = self.kwargs['slug']
        context["authors"] = self.model.objects.all()
        context["article_section"] = ArticleSection.objects.all()
        context["articles"] = Article.objects.filter(authors=self.model.objects.get(slug=slug)).distinct()

        context["current_path"] = str(self.request.path)[3:]
        return dict(list(context.items()) + list(self.get_user_context().items()))


class Registration(MenuMixin, ListView):
    model = User
    template_name = "main_app/registration.html"

    def get(self, request, *args, **kwargs):
        form = RegisterUserForm()
        links = Page.objects.filter(linklocation__title="About us")
        menu_links = Page.objects.filter(linklocation__title="Menu")
        side_bar_links = Page.objects.filter(linklocation__title="Side bar")
        try:
            next_volume = Volume.objects.filter(status_str="Следующий")[0]
        except:
            next_volume = None
        current_path = str(self.request.path)[3:]

        return render(request, 'main_app/registration.html', {'form': form,
                                                              'links': links,
                                                              'menu_links': menu_links,
                                                              'side_bar_links': side_bar_links,
                                                              'next_volume': next_volume,
                                                              'current_path': current_path})

    def post(self, request, *args, **kwargs):
        form = RegisterUserForm(request.POST)
        print(2)
        if form.is_valid():
            # save form in the memory not in database
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            # to get the domain of the current site
            current_site = get_current_site(request)
            mail_subject = 'Activation link has been sent to your email id'
            message = render_to_string('main_app/registration/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            return HttpResponseRedirect(reverse_lazy("registration-confirm"))
        else:
            return render(request, self.template_name, {"form": form})


def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return HttpResponseRedirect(reverse_lazy("successful-registration"))
    else:
        return HttpResponseRedirect(reverse_lazy("invalid-link"))


class EmailConfirmation(MenuMixin, ListView):
    model = User
    template_name = "main_app/registration/email_confirm_page.html"

    def get_context_data(self, **kwargs):
        context = super(EmailConfirmation, self).get_context_data(**kwargs)

        context["current_path"] = str(self.request.path)[3:]
        return dict(list(context.items()) + list(self.get_user_context().items()))


class SuccessfulRegisration(MenuMixin, ListView):
    model = User
    template_name = "main_app/registration/email_activation_page.html"

    def get_context_data(self, **kwargs):
        context = super(SuccessfulRegisration, self).get_context_data(**kwargs)

        context["current_path"] = str(self.request.path)[3:]
        return dict(list(context.items()) + list(self.get_user_context().items()))


class InvalidLink(MenuMixin, ListView):
    model = User
    template_name = "main_app/registration/invalid_link.html"

    def get_context_data(self, **kwargs):
        context = super(InvalidLink, self).get_context_data(**kwargs)

        context["current_path"] = str(self.request.path)[3:]
        return dict(list(context.items()) + list(self.get_user_context().items()))


class LoginUser(MenuMixin, LoginView):
    form_class = AuthenticationForm
    template_name = "main_app/login.html"

    def get_context_data(self, **kwargs):
        context = super(LoginUser, self).get_context_data(**kwargs)

        context["current_path"] = str(self.request.path)[3:]
        return dict(list(context.items()) + list(self.get_user_context().items()))

    def get_success_url(self):
        return reverse_lazy("home")

