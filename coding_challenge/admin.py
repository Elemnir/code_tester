from django.contrib import admin

from .models import Challenge, ChallengeTest, ChallengeAttempt


def publish_challenges(modeladmin, request, queryset):
    for challenge in queryset:
        challenge.publish()
publish_challenges.short_description = "Publish the selected challenges"

class ChallengeTestInline(admin.StackedInline):
    model = ChallengeTest

class ChallengeAdmin(admin.ModelAdmin):
    class Meta:
        model = Challenge
    actions = [publish_challenges]
    fields  = ['name','description','solution']
    inlines = [ChallengeTestInline]
    list_display = ('name', 'ispublished', 'pub_date')
admin.site.register(Challenge, ChallengeAdmin)


class ChallengeTestAdmin(admin.ModelAdmin):
    class Meta:
        model = ChallengeTest
admin.site.register(ChallengeTest, ChallengeTestAdmin)


class ChallengeAttemptAdmin(admin.ModelAdmin):
    class Meta:
        model = ChallengeAttempt
admin.site.register(ChallengeAttempt, ChallengeAttemptAdmin)
