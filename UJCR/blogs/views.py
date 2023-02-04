from django.http import FileResponse, Http404
from django.views.generic import ListView, DetailView

from blogs.models import *
from main_app.utils import MenuMixin
from ujcr.settings import MEDIA_ROOT


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('HTTP_USER_AGENT') # В REMOTE_ADDR значение айпи пользователя
    return ip


class ArticleView(MenuMixin, DetailView):
    model = Article
    template_name = "blogs/article.html"
    slug_field = 'slug'

    def get_context_data(self, **kwargs):
        context = super(ArticleView, self).get_context_data(**kwargs)
        slug = self.kwargs['slug']
        ip = get_client_ip(self.request)
        user_id = ip
        if not UniqueViewers.objects.filter(user_id=user_id).exists():
            user = UniqueViewers()
            user.user_id = user_id
            user.save()

        viewer = UniqueViewers.objects.get(user_id=user_id)
        a = Article.objects.get(slug=slug)
        a.viewers.add(viewer)
        a.save()

        context["object"] = Article.objects.get(slug=slug)
        context["published_date"] = Article.objects.get(slug=slug).published_date.strftime("%Y/%m/%d")
        context["authors"] = Article.objects.get(slug=slug).authors_text.strip().split(",")
        context["current_path"] = str(self.request.path)[3:]
        context["current_lang"] = str(self.request.path)[:3]

        return dict(list(context.items()) + list(self.get_user_context().items()))


class ArchiveView(MenuMixin, ListView):
    model = Volume
    template_name = "blogs/archives.html"
    queryset = model.objects.filter(status_str="Архивный")

    def get_context_data(self, **kwargs):
        context = super(ArchiveView, self).get_context_data(**kwargs)

        context["current_volume"] = Volume.objects.filter(status_str="Активный")[0]
        context["current_path"] = str(self.request.path)[3:]
        if "/ru/" in context["current_path"]:
            context["title"] = "Архивы | UJCR"
        else:
            context["title"] = "Archives | UJCR"
        return dict(list(context.items()) + list(self.get_user_context().items()))


class IssueDetail(MenuMixin, DetailView):
    model = Volume
    template_name = "blogs/issue.html"
    slug_field = 'slug'

    def get_context_data(self, **kwargs):
        context = super(IssueDetail, self).get_context_data(**kwargs)
        slug = self.kwargs['slug']
        context["articles"] = Article.objects.filter(is_active=True,
                                                     linked_volume=self.model.objects.filter(slug=slug)[0].id)

        a = set()
        for i in context["articles"]:
            if i.chapter is None:
                continue
            a.add(i.chapter)

        context["article_section"] = ArticleSection.objects.filter(title__in=list(a))
        context["title"] = Volume.objects.get(slug=self.kwargs["slug"])

        context["current_path"] = str(self.request.path)[3:]
        return dict(list(context.items()) + list(self.get_user_context().items()))


class TagCloudPage(MenuMixin, ListView):
    model = Tags
    template_name = "blogs/tag_cloud_page.html"
    queryset = model.objects.all()

    def get_context_data(self, **kwargs):
        context = super(TagCloudPage, self).get_context_data(**kwargs)
        print(self.request.user.id)
        # сортируем теги по количеству статей
        for tag in Tags.objects.all():
            related_articles = Article.objects.filter(tags=tag)
            tag.related_articles_number = related_articles.count()
            tag.save()

        context["tags"] = Tags.objects.order_by("-related_articles_number")

        context["current_path"] = str(self.request.path)[3:]

        return dict(list(context.items()) + list(self.get_user_context().items()))


class Pdf_view(DetailView):
    slug_field = "slug"
    def get(self, *args, **kwargs):
        try:
            a = Article.objects.get(slug=self.kwargs["slug"])
            return FileResponse(open(MEDIA_ROOT.replace("\\", "/") + "/" + str(a.file), 'rb'), content_type='application/pdf')
        except FileNotFoundError:
            raise Http404()


class Pdf_view_volume(DetailView):
    slug_field = "slug"
    def get(self, *args, **kwargs):
        try:
            a = Volume.objects.get(slug=self.kwargs["slug"])
            return FileResponse(open(MEDIA_ROOT.replace("\\", "/") + "/" + str(a.file), 'rb'), content_type='application/pdf')
        except FileNotFoundError:
            raise Http404()


