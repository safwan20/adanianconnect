from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("",views.register,name="register"),
    #path("login",auth_views.LoginView.as_view(redirect_authenticated_user=True),name="login"),
    path("login", views.login, name="login"),
    path("logout",auth_views.LogoutView.as_view(template_name='registration/logout.html'),name="logout"),
    path("profile",views.profile,name="profile"),
    path("like",views.like,name="like"),
    path("home",views.home,name="home"),
    path("edit",views.edit,name="edit"),
    path("show/<int:id>", views.show, name="show"),
    path("friends", views.friends, name="friends"),
    path("editu", views.editu, name="editu"),
    path("delete", views.delete, name="delete"),
    path("stats", views.stats, name="stats"),
    path('message-box/<int:id>', views.messagebox, name="messagebox"),
    path('show-messages', views.messageshow, name='messageshow'),
    path('single-message/<int:id>', views.singlemessage, name='singlemessage'),


    path('password-reset',
         auth_views.PasswordResetView.as_view(
             template_name='password_reset.html'
         ),
         name='password_reset'),

    path('password-reset/done',

         auth_views.PasswordResetDoneView.as_view(
             template_name='password_reset_done.html'
         ),
         name='password_reset_done'),

    path('password-reset-confirm/<uidb64>/<token>',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='password_reset_confirm.html'
         ),
         name='password_reset_confirm'),

    path('password-reset-complete',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='password_reset_complete.html'
         ),
         name='password_reset_complete'),

]


