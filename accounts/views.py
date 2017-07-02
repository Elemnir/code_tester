from django.http                import HttpResponseRedirect
from django.shortcuts           import redirect, render
from django.contrib.auth        import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.forms  import UserCreationForm
from django.urls                import reverse_lazy
from django.views               import View
from django.views.generic.edit  import FormView
from accounts.forms             import CreateUserForm


class Profile(View):
    def get(self, request):
        return render(request, "registration/profile.html")


class Register(FormView):
    template_name = 'registration/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('accounts_profile')

    def form_valid(self, form):
        user = form.save()
        user = authenticate(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password2']
        )
        login(request, user)
        return super(ContactView, self).form_valid(form)

