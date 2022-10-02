from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import *

urlpatterns = [
    path('tag-cloud/', TagCloudPage.as_view(), name="tag-cloud"),
    path('issue/', ArchiveView.as_view(), name="issue"),
    path('issue/<slug:slug>/', IssueDetail.as_view(), name="issue-detail"),
    path('issue/article/<slug:slug>/', ArticleView.as_view(), name="article"),
    path("pdf/article/<slug:slug>.pdf", Pdf_view.as_view(), name="pdf-view"),
    path("pdf/volume/<slug:slug>", Pdf_view_volume.as_view(), name="pdf-view-volume"),
]
