from django.shortcuts import render, redirect

from django.contrib.auth.models import Group
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic


class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"

    def post(self, request, *args, **kwargs):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            user_group = Group.objects.get(name='staff')
            user.groups.add(user_group)
            return redirect('login')
        else:
            return render(request, self.template_name, {'form' : form })
