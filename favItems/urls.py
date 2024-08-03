"""favItems URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import TemplateView
from django.contrib.auth import views as auth_views
from .forms import LoginForm, MyPasswordChangeForm, MyPasswordResetForm, MySetPasswordForm
from . import views

urlpatterns = [
	path('admin/', admin.site.urls),
	#path("accounts/", include("django.contrib.auth.urls")),
	#path("accounts/", include("accounts.urls")),
	path('registration/', views.CustomerRegistrationView.as_view(), name='customerregistration'),
	path('accounts/login/', auth_views.LoginView.as_view(template_name='login.html', authentication_form=LoginForm), name="login"),
	path('logout/', auth_views.LogoutView.as_view(next_page="login"), name="logout"),
	path('passwordchange/', auth_views.PasswordChangeView.as_view(template_name='passwordchange.html', form_class=MyPasswordChangeForm, success_url="/passwordchangedone/"), name="passwordchange"),
	path('passwordchangedone/', auth_views.PasswordChangeDoneView.as_view(template_name='passwordchangedone.html'), name="passwordchangedone"),
	path('password-reset/',auth_views.PasswordResetView.as_view(template_name='password_reset.html', form_class=MyPasswordResetForm), name="password_reset"),
	path('password-reset/done/',auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name="password_reset_done"),
	path('password-reset-confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html', form_class=MySetPasswordForm),name="password_reset_confirm"),
	path('password-reset-complete',auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),name="password_reset_complete"),
	#path('', views.index, name='Home'),
	path('', TemplateView.as_view(template_name='index.html'), name='home'),
	path('profile/', views.ProfileView.as_view(), name="profile"),
	path('address/', views.address, name="address"),
	path('remAddress', views.remAddress, name="remAdd"),
	path('shop/', include('shop.urls')),
	path('blog/', include('blog.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
