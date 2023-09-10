from django.urls import reverse
from django.contrib.auth.models import AbstractUser


# using-a-custom-user-model-when-starting-a-project
# https://docs.djangoproject.com/en/4.2/topics/auth/customizing/
class User(AbstractUser):

    def get_absolute_url(self):
        return reverse('account:show_profile')
