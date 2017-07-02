from django.conf.urls   import include, url

from .views import Profile, Register

urlpatterns = [
    url(r"^", include('django.contrib.auth.urls')),
    url(r"^profile/$",  Profile.as_view(),  name='accounts_profile'),
    url(r"^register/$", Register.as_view(), name='accounts_register'),
]
