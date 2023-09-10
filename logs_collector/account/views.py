from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic

from collector.utils.mixins import ExtraContextMixin

from .forms import UserProfileForm
from .models import User


class DetailProfile(LoginRequiredMixin, ExtraContextMixin, generic.DetailView):
    model = User
    template_name = 'account/profile_info.html'
    context_object_name = 'profile'

    def get_title(self, **kwargs):
        return f'{self.title} - {self.request.user}'

    def get_object(self):
        return self.model.objects.get(username=self.request.user)


class UpdateProfile(LoginRequiredMixin, ExtraContextMixin, generic.UpdateView):
    model = User
    template_name = 'account/profile_update.html'
    context_object_name = 'profile'
    form_class = UserProfileForm

    def get_object(self):
        return self.model.objects.get(username=self.request.user)

    def get_title(self, **kwargs):
        return f'{self.title} - {self.kwargs.get("username", "account")}'
