from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, Http404
from django.views.generic import UpdateView, CreateView, ListView
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic.edit import FormMixin

from blogs.forms import ArticleCreateForm, CommentCreateForm, AuthorCreateForm
from .models import AuthorsProfile, ReviewersProfile
from main_app.utils import MenuMixin, get_or_none
from blogs.models import Article, ArticleStatusEnum, Comment, Authors


class ProfilePage(LoginRequiredMixin, MenuMixin, ListView):
    login_url = reverse_lazy("login")
    model = AuthorsProfile
    template_name = "profiles/authors_profile.html"

    def get_context_data(self, **kwargs):
        context = super(ProfilePage, self).get_context_data(**kwargs)
        user = self.request.user
        reviewer = get_or_none(ReviewersProfile, user=user)
        author = get_or_none(AuthorsProfile, user=user)
        context["is_author"] = bool(author)
        context["is_reviewer"] = bool(reviewer)
        if not (author or reviewer):
            raise Http404()
        context["articles"] = Article.objects.filter(profile_author=author)
        context["reviews"] = Article.objects.filter(is_draft=False, status=ArticleStatusEnum.reviewing.value).exclude(
            comment_article__reviewer=reviewer).distinct()
        context["comments"] = Comment.objects.filter(reviewer=reviewer).exclude(
            article__is_draft=True, article__status=ArticleStatusEnum.draft.value).distinct()
        context["authors"] = Authors.objects.filter(linked_profile=author)
        return dict(list(context.items()) + list(self.get_user_context().items()))


class ArticleCreate(LoginRequiredMixin, MenuMixin, CreateView):
    form_class = ArticleCreateForm
    template_name = "profiles/article_create.html"
    login_url = reverse_lazy("login")

    def get_form_kwargs(self):
        kwargs = super(ArticleCreate, self).get_form_kwargs()
        kwargs['profile'] = AuthorsProfile.objects.get(user=self.request.user)
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(ArticleCreate, self).get_context_data(**kwargs)
        return dict(list(context.items()) + list(self.get_user_context().items()))

    def form_valid(self, form, *args, **kwargs):
        article = form.save()
        article.authors.add(AuthorsProfile.objects.get(user=self.request.user))
        article.save()
        messages.add_message(
            self.request, messages.INFO,
            "Для заполнения полей на других языках переключайтесь между языками в правой панеле"
        )
        return HttpResponseRedirect(reverse_lazy("article-update", kwargs={"slug": article.slug}))


class ArticleUpdate(LoginRequiredMixin, MenuMixin, UpdateView):
    model = Article
    form_class = ArticleCreateForm
    template_name = "profiles/article_update.html"
    success_url = reverse_lazy("author-profile")
    login_url = reverse_lazy("login")

    def get_context_data(self, **kwargs):
        context = super(ArticleUpdate, self).get_context_data(**kwargs)
        try:
            author = AuthorsProfile.objects.get(user=self.request.user)
            article = Article.objects.get(pk=self.object.pk, authors=author)
        except:
            raise Http404()
        context["comments"] = Comment.objects.filter(article=article).select_related("reviewer")\
            .only("reviewer__full_name")
        return dict(list(context.items()) + list(self.get_user_context().items()))


class ArticleReviewing(MenuMixin, CreateView):
    form_class = CommentCreateForm
    template_name = "profiles/article_reviewing.html"
    slug_field = 'pk'

    def get_context_data(self, **kwargs):
        context = super(ArticleReviewing, self).get_context_data(**kwargs)
        pk = self.kwargs['int']
        if Article.objects.get(pk=pk).is_draft:
            raise Http404()

        context["object"] = Article.objects.get(pk=pk)

        return dict(list(context.items()) + list(self.get_user_context().items()))

    def form_valid(self, form, *args, **kwargs):
        comment = form.save(commit=False)
        comment.article = Article.objects.get(pk=self.kwargs["int"])
        reviewer = ReviewersProfile.objects.get(user=self.request.user)
        comment.reviewer = reviewer
        comment.save()
        messages.add_message(
            self.request, messages.INFO,
            "Ваша рецензия была принята!"
        )
        return HttpResponseRedirect(reverse_lazy("author-profile"))


class ArticleUpdatingReview(LoginRequiredMixin, MenuMixin, UpdateView):
    model = Comment
    form_class = CommentCreateForm
    template_name = "profiles/article_update_review.html"
    success_url = reverse_lazy("author-profile")
    login_url = reverse_lazy("login")

    def get_context_data(self, **kwargs):
        context = super(ArticleUpdatingReview, self).get_context_data(**kwargs)
        pk = self.kwargs["pk"]
        comment = Comment.objects.get(pk=pk)
        context["object"] = Article.objects.get(comment_article=comment)
        return dict(list(context.items()) + list(self.get_user_context().items()))

    def form_valid(self, form, *args, **kwargs):
        comment = form.save()
        comment.save()
        messages.add_message(
            self.request, messages.INFO,
            "Ваша рецензия успешно изменена!")
        return HttpResponseRedirect(reverse_lazy("author-profile"))


class AuthorCreate(LoginRequiredMixin, MenuMixin, CreateView):
    form_class = AuthorCreateForm
    template_name = "profiles/author_create.html"
    success_url = reverse_lazy("author-profile")
    login_url = reverse_lazy("login")

    def form_valid(self, form, *args, **kwargs):
        author = form.save()
        author.linked_profile = AuthorsProfile.objects.get(user=self.request.user)
        author.save()
        messages.add_message(
            self.request, messages.SUCCESS,
            "Автор зарегестрирован!"
        )
        return HttpResponseRedirect(reverse_lazy("author-profile"))


class AuthorUpdate(LoginRequiredMixin, MenuMixin, UpdateView):
    model = Authors
    form_class = AuthorCreateForm
    template_name = "profiles/author_update.html"
    success_url = reverse_lazy("author-profile")
    login_url = reverse_lazy("login")

    def get_context_data(self, **kwargs):
        context = super(AuthorUpdate, self).get_context_data(**kwargs)
        try:
            author_profile = AuthorsProfile.objects.get(user=self.request.user)
            author = Authors.objects.get(pk=self.object.pk, linked_profile=author_profile)
        except:
            raise Http404()
        return dict(list(context.items()) + list(self.get_user_context().items()))
