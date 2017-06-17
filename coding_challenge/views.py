from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts           import get_object_or_404, render
from django.utils               import timezone
from django.views               import View
from django.views.generic       import ListView

from .models    import Challenge, ChallengeTest, ChallengeAttempt

class ChallengeList(ListView):
    context_object_name = "challenge_list"
    queryset = Challenge.objects.filter(ispublished=True).order_by('-pub_date')
    template_name = "challenges/pub_list.html"


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
        if not failed:
            attempt.pass_time = timezone.now()
            attempt.passed = True
        attempt.save()
        
        return render(request, "challenges/view_prob.html", {
            'attempt'   : attempt,
            'challenge' : challenge,
            'failed'    : failed,
        })
