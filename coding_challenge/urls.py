from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from .views import ChallengeList, ViewChallenge

urlpatterns = [
    url(r"^$", ChallengeList.as_view(), name="challenge_list"),
    url(r"^view/(?P<cid>\d+)/$", 
        login_required(ViewChallenge.as_view()), 
        name="challenge_view"
    ),
]
