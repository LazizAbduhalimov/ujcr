from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import *
from django.contrib.auth.views import PasswordResetView, PasswordResetCompleteView, PasswordResetDoneView, PasswordResetConfirmView

urlpatterns = [
    path("favicon.ico", favicon),

    path('authors/', AuthorsPage.as_view(), name="authors"),
    path('authors/<slug:slug>/', AuthorsDetailPage.as_view(), name="author-detail"),
    path('editorial-office/', EditorialPage.as_view(), name="editorial-team"),
    path('editorial-office/<slug:slug>', EditorialMemberPage.as_view(), name="editorial-member"),

    path('activate/<uidb64>/<token>/', activate, name='activate'),
    path('registration/', Registration.as_view(), name="registration"),
    path('registration/confirmation/', EmailConfirmation.as_view(), name="registration-confirm"),
    path('registration/activation/', SuccessfulRegisration.as_view(), name="successful-registration"),
    path('registration/invalid/', InvalidLink.as_view(), name="invalid-link"),

    path('password-reset/',
         PasswordResetView.as_view(
             template_name='main_app/registration/password_reset.html',
             subject_template_name='registration/password_reset_subject.txt',
             email_template_name='registration/password_reset_email.html',
         ), name='password_reset'),
    path('password-reset/done/',
         PasswordResetDoneView.as_view(template_name='main_app/registration/password_reset_mail_sent.html'
         ),name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         PasswordResetConfirmView.as_view(template_name='main_app/registration/password_reset_confirmation.html'
         ),name='password_reset_confirm'),
    path('password-reset-complete/',
         PasswordResetCompleteView.as_view(template_name='main_app/registration/password_reset_completed.html'),
         name='password_reset_complete'),

    path('login/', LoginUser.as_view(), name="login"),
    path('log-out', LogoutView.as_view(next_page="home"), name="exit"),

    path('<slug:slug>/', SamePages.as_view(), name="same-pages"),
]
