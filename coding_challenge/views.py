from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db.models           import Sum
from django.shortcuts           import get_object_or_404, render
from django.utils               import timezone
from django.views               import View
from django.views.generic       import ListView

from .models    import Challenge, ChallengeTest, ChallengeAttempt

class ChallengeList(ListView):
    context_object_name = "challenge_list"
    queryset = Challenge.objects.filter(ispublished=True).order_by('-pub_date')
    template_name = "challenges/pub_list.html"
    paginate_by = 25

class LeaderBoard(ListView):
    context_object_name = "user_scores"
    queryset = User.objects.annotate(
        total_points=Sum('challengeattempt__earned_pts')
    ).filter(total_points__gt=0)
    template_name = "challenges/leaderboard.html"
    paginate_by = 25

class ViewChallenge(LoginRequiredMixin, View):
    def get(self, request, cid):
        challenge = get_object_or_404(Challenge, pk=cid)
        attempt, created = ChallengeAttempt.objects.get_or_create(
            challenge=challenge,
            submitter=request.user
        )
        return render(request, "challenges/view_prob.html", {
            'attempt'   : attempt,
            'challenge' : challenge,
        })
    
    def post(self, request, cid):
        challenge = get_object_or_404(Challenge, pk=cid)
        attempt = get_object_or_404(ChallengeAttempt, 
            challenge=challenge, 
            submitter=request.user
        )
        
        attempt.submission = request.POST.get("submission", attempt.submission)
        failed = challenge.run_tests(attempt)
        if not failed and not attempt.passed:
            attempt.pass_time = timezone.now()
            attempt.earned_pts = attempt.calc_points()
            attempt.passed = True
        attempt.save()
        
        return render(request, "challenges/view_prob.html", {
            'attempt'   : attempt,
            'challenge' : challenge,
            'failed'    : failed,
        })
