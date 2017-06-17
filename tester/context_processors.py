from django.core.urlresolvers import reverse

def nav_menu(request):
    return { 'nav_menu': [
        (
            { 'name': 'Challenges', 'url': reverse('challenge_list')},
            {}
        ),
    ]}
