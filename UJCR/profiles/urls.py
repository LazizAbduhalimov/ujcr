from django.urls import path
from .views import *

urlpatterns = [
    path('review/article/<int:int>', ArticleReviewing.as_view(), name="article-review"),
    path('update-review/article/<slug:pk>', ArticleUpdatingReview.as_view(), name="article-update-review"),

    path('profile/', ProfilePage.as_view(), name="author-profile"),
    path('article/create/', ArticleCreate.as_view(), name="article-create"),
    path('article/update/<slug:slug>', ArticleUpdate.as_view(), name="article-update"),

    path('author/create/', AuthorCreate.as_view(), name="author-create"),
    path('author/update/<slug:slug>', AuthorUpdate.as_view(), name="author-update"),
]
