import datetime
import os
import subprocess
import tempfile

from django.contrib.auth.models import User
from django.db                  import models
import markdown


class Challenge(models.Model):
    name        = models.CharField(max_length=200)
    description = models.TextField()
    solution    = models.TextField()
    points      = models.IntegerField(default=0)
    author      = models.ForeignKey(User)
    author_date = models.DateTimeField(auto_now_add=True)
    pub_date    = models.DateTimeField(null=True, blank=True)
    ispublished = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name
    
    def render_description(self):
        """Returns the Challenge's markdown description rendered as html."""
        return markdown.markdown(self.description)
    
    def publish(self):
        """Mark the Challenge for publishing."""
        self.ispublished = True
        self.pub_date = datetime.datetime.now()
        self.save()
  
    def unpublish(self):
        """Hide the Challenge from normal users."""
        self.ispublished = False
        self.pub_date = None
        self.save()

    def run_tests(self, attempt):
        """Run all tests for the Challenge against the attempt."""
        tests = ChallengeTest.objects.filter(challenge=self)
        failed = []
        for test in tests:
            sample_out  = test.run_test(attempt.submission)
            correct_out = test.run_test(self.solution)
            if sample_out != correct_out:
                failed.append({
                    'debug_text'    : test.debug_text,
                    'correct_out'   : correct_out,
                    'test_out'      : sample_out,
                })
        return failed


class ChallengeTest(models.Model):
    challenge   = models.ForeignKey(Challenge)
    debug_text  = models.TextField()
    harness     = models.TextField()

    def __str__(self):
        return self.debug_text

    def run_test(self, source):
        """Run the given source in the ChallengeTest's harness."""
        try:
            handle = tempfile.NamedTemporaryFile(mode="w+", delete=False)
            handle.write(self.harness.replace("$CODE$", source))
            handle.close()
            output = subprocess.check_output(
                ["python3", handle.name], 
                stderr=subprocess.STDOUT, 
                universal_newlines=True,
                timeout=15
            )
        except subprocess.CalledProcessError as e:
            return "Runtime Error: " + e.output
        except subprocess.TimeoutExpired:
            return "Process timed out"
        finally:
            os.remove(handle.name)
        return output


class ChallengeAttempt(models.Model):
    challenge   = models.ForeignKey(Challenge)
    submitter   = models.ForeignKey(User)
    open_time   = models.DateTimeField(auto_now_add=True)
    pass_time   = models.DateTimeField(null=True, blank=True)
    passed      = models.BooleanField(blank=True, default=False)
    earned_pts  = models.IntegerField(blank=True, default=0)
    submission  = models.TextField()
    
    def __str__(self):
        return str(self.challenge) + ' - ' + str(self.submitter)

    def calc_points(self):
        """Calculate how many points the attempt is worth"""
        if self.earned_pts != 0:
            return self.earned_pts
        tdiff = self.pass_time - self.open_time
        tdiff -= datetime.timedelta(minutes=5)
        max_pts = self.challenge.points
        if tdiff < datetime.timedelta():
            return max_pts
        return max(
            int(max_pts * 0.15), 
            int(max_pts * (1 - tdiff / datetime.timedelta(hours=3)))
        )
