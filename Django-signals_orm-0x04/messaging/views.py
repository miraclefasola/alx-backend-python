from django.shortcuts import render
from models import *
# Create your views here.
from django.views.generic import ListView, DeleteView, CreateView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model, logout
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page, vary_on_cookie
from django.db.models import Q

User = get_user_model()

class InboxView(LoginRequiredMixin, ListView):
    model = Message
    template_name = "messaging/inbox.html"
    context_object_name = "messages"

    def get_queryset(self):
        return Message.unread.unread_for_user(self.request.user).only(
            "id", "sender", "content", "created_at"
        )

class UserDeleteView(LoginRequiredMixin, DeleteView):
    model = User
    template_name = "users/user_confirm_delete.html"
    success_url = reverse_lazy("home")  # redirect after deletion

    def get_object(self, queryset=None):
        # Always delete the logged-in user
        return self.request.user

    def delete(self, request, *args, **kwargs):
        # Log out before deletion
        logout(request)
        return super().delete(request, *args, **kwargs)
    


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    fields = ['content', 'parent_message']  # form fields user can set
    template_name = 'messaging/send_message.html'

    def form_valid(self, form):
        # automatically set sender and receiver
        form.instance.sender = self.request.user
        form.instance.receiver = get_object_or_404(User, pk=self.kwargs['receiver_id'])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('inbox')  # redirect after sending



@method_decorator([login_required, vary_on_cookie, cache_page(60)], name='dispatch')
class ConversationView(LoginRequiredMixin, TemplateView):
    template_name = "messaging/conversation.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id = self.kwargs['user_id']

        # ✅ Use Q objects for clean OR filtering
        messages = Message.objects.filter(
            Q(sender=self.request.user, receiver_id=user_id) |
            Q(sender_id=user_id, receiver=self.request.user),
            parent_message__isnull=True  # only top-level messages
        ).select_related("sender", "receiver").prefetch_related(
            "replies__sender", "replies__receiver"
        )

        # build threaded conversation recursively
        threads = [self.get_thread(msg) for msg in messages]

        context['messages'] = threads
        return context

    def get_thread(self, message):
        """Recursive helper to fetch a message and all replies"""
        thread = [message]  # start with the parent
        for reply in message.replies.all().select_related("sender", "receiver"):
            thread.extend(self.get_thread(reply))  # flatten replies recursively
        return thread


class MessageThreadView(LoginRequiredMixin, TemplateView):
    template_name = "messaging/thread.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        message_id = self.kwargs['message_id']

        # fetch message with related sender/receiver
        message = get_object_or_404(
            Message.objects.select_related("sender", "receiver"),
            pk=message_id
        )

        # recursive thread
        context['thread'] = self.get_thread(message)
        return context

    def get_thread(self, message):
        """Recursive helper to fetch a message and all replies"""
        thread = [message]
        for reply in message.replies.all().select_related("sender", "receiver"):
            thread.extend(self.get_thread(reply))
        return thread


