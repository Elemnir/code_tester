from django.conf.urls import url

from .views import ChallengeList, ViewChallenge

urlpatterns = [
    url(r"^$", 
        ChallengeList.as_view(), 
        name="challenge_list"
    ),
    url(r"^view/(?P<cid>\d+)/$", 
        ViewChallenge.as_view(), 
        name="challenge_view"
    ),
]
