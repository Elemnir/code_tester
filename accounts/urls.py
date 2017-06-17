from django.conf.urls           import url
from django.contrib.auth.views  import LoginView, LogoutView

from .views import register

urlpatterns = [
    url(r"^login/$",    LoginView.as_view(),    name='accounts_login'),
    url(r"^logout/$",   LogoutView.as_view(),   name='accounts_logout'),
    url(r"^register/$", register,               name='accounts_register'),
]
