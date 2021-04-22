from django.views.generic.edit import FormView
from development.forms import ChallengeForm
from django.views.generic.list import ListView
from .models import Match
from django.urls import reverse_lazy
from django.contrib import messages


class ChallengeView(FormView):
    form_class = ChallengeForm
    success_url = reverse_lazy('development:challenge')

    def form_valid(self, form):
        option1 = form.cleaned_data['bot1']
        option2 = form.cleaned_data['bot2']
        bot1 = dict(form.fields['bot1'].choices)[option1]
        bot2 = dict(form.fields['bot2'].choices)[option2]
        messages.add_message(
            self.request,
            messages.INFO,
            str(bot1) + ' VS ' + str(bot2),
        )
        return super().form_valid(form)


class MatchListView(ListView):
    template_name = 'development/match_history.html'
    model = Match
