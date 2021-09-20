from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import gettext_lazy as _
from django.views.generic import FormView, ListView

from .forms import LoginForm
from .models import Message


class ChatLoginFormView(FormView):
    """
    View для входа в чат-комнату.
    """
    form_class = LoginForm
    success_url = settings.LOGIN_REDIRECT_URL
    template_name = 'chat/login.html'
    extra_context = {'title': _('login page')}

    def form_valid(self, form):
        user = form.get_or_create_user()
        login(self.request, user)
        return super().form_valid(form)


class RoomTemplateView(LoginRequiredMixin, ListView):
    """
    View для чат-комнаты
    """
    template_name = 'chat/room.html'
    model = Message
    extra_context = {'title': _('chat room')}

    def get_queryset(self):
        return super().get_queryset()[:settings.MAX_MESSAGES_HISTORY_LENGTH]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['room_name'] = self.kwargs['room_name']
        return context
