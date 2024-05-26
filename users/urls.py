from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views

from django.contrib.auth.decorators import login_required

from . import views

app_name = "users"

urlpatterns = [
    path("register/", views.register, name="register"),
    path("login/", views.login_user, name="login_user"),
    path("logout/", views.logout_user, name="logout_user"),
    path("inbox/", views.inbox, name="inbox"),
    path("conversation/<int:pk>", views.conversation, name="conversation"),
    path("profile/<int:pk>", views.profile_view, name="profile_view"),
    path("profile/update/", views.update_profile, name="update_profile"),
    path(
        "password_change/",
        auth_views.PasswordChangeView.as_view(
            template_name="users/password_change.html",
            success_url=reverse_lazy(
                "users:password_change_done"
            ),  # I need to specify that password_change_done is in the users app
        ),
        name="password_change",
    ),
    path(
        "password_change/done/",
        auth_views.PasswordChangeDoneView.as_view(
            template_name="users/password_change_done.html"
        ),
        name="password_change_done",
    ),
    path("api/user/", views.UserProfileList.as_view()),
    path("api/user/<int:user>", views.UserProfileDetail.as_view()),
]
