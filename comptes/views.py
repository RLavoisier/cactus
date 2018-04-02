from django.contrib.auth import get_user_model

# Create your views here.
from django.views.generic import TemplateView
from django.views.generic.edit import ModelFormMixin, ProcessFormView, CreateView

from comptes.forms import CactusUserCreationForm


class UserSignupView(CreateView):
    template_name = "comptes/signup.html"
    form_class = CactusUserCreationForm
