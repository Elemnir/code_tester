from django.contrib import admin

from .models import Challenge, ChallengeTest, ChallengeAttempt


def publish_challenges(modeladmin, request, queryset):
    for challenge in queryset:
        challenge.publish()
publish_challenges.short_description = "Publish the selected challenges"

def unpublish_challenges(modeladmin, request, queryset):
    for challenge in queryset:
        challenge.unpublish()
unpublish_challenges.short_description = "Unpublish the selected challenges"

class ChallengeTestInline(admin.StackedInline):
    model = ChallengeTest

class ChallengeAdmin(admin.ModelAdmin):
    class Meta:
        model = Challenge
    actions = [publish_challenges, unpublish_challenges]
    fields  = ['name', 'author', 'points', 'description', 'solution']
    inlines = [ChallengeTestInline]
    list_display = (
        'name', 'author', 'author_date', 'points', 'ispublished', 'pub_date'
    )
admin.site.register(Challenge, ChallengeAdmin)


class ChallengeAttemptAdmin(admin.ModelAdmin):
    class Meta:
        model = ChallengeAttempt
admin.site.register(ChallengeAttempt, ChallengeAttemptAdmin)
