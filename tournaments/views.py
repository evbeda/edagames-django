from django.views.generic.edit import FormView
# import requests
from auth_app.models import Bot
from .forms import BotForm
from django.urls import reverse_lazy
from django.contrib import messages
from development.encode_jwt import encode_data


class AddBotView(FormView):
    form_class = BotForm
    success_url = reverse_lazy('development:mybots')
    template_name = 'development/add_bot.html'

    def get_form(self, form_class=None):
        if self.request.method == 'POST':
            form = BotForm(data=self.request.POST)
        else:
            form = BotForm()
        return form

    def form_valid(self, form):
        new_bot = form.save(commit=False)
        new_bot.user = self.request.user
        new_bot.token = encode_data(
            key='user',
            value=new_bot.name,
        )
        if not Bot.objects.filter(name=new_bot.name,).exists():
            new_bot.save()
            messages.add_message(
                self.request,
                messages.SUCCESS,
                'Bot '
                '{} successfully added'.format(new_bot.name)
            )
        else:
            messages.add_message(
                self.request,
                messages.ERROR,
                'It is not possible to create this record, a bot already exists with the name '
                '{}. Try a new name'.format(new_bot.name)
            )
            self.success_url = reverse_lazy('development:addbot')
        return super().form_valid(form)
