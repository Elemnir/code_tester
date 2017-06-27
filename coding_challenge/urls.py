from django.conf.urls import url

from .views import ChallengeList, LeaderBoard, ViewChallenge

urlpatterns = [
    url(r"^$", 
        ChallengeList.as_view(), 
        name="challenge_list"
    ),
    url(r"^rankings/$",
        LeaderBoard.as_view(),
        name="challenge_rank"
    ),
    url(r"^view/(?P<cid>\d+)/$", 
        ViewChallenge.as_view(), 
        name="challenge_view"
    ),
]
