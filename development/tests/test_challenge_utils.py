from unittest.mock import patch

from django.http import HttpResponse
from django.test import (
    RequestFactory,
    TestCase,
)

from auth_app.models import (
    Bot,
    User,
)
from development.models import Challenge
from ..forms import ChallengeForm
from ..views import ChallengeView


class TestChallangeUtils(TestCase):
    def setUp(self) -> None:
        self.factory = RequestFactory()
        self.user1 = User.objects.create(email='test1@gmail.com', username='UsuarioTest1')
        self.bot1 = Bot.objects.create(name='bot1', user=self.user1)
        self.user2 = User.objects.create(email='test2@gmail.com', username='UsuarioTest2')
        self.bot2 = Bot.objects.create(name='bot2', user=self.user2)

    @patch('development.views.messages')
    @patch('requests.post')
    def test_should_save_a_challenge_after_send_it(self, post_patched, messages_patched):
        post_patched.return_value = HttpResponse(status=200)
        form = ChallengeForm({'bot1': '0', 'bot2': '1'})
        form.fields['bot1'].choices = [(0, 'bot1')]
        form.fields['bot2'].choices = [(0, 'bot1'), (1, 'bot2')]
        form.is_valid()
        view = ChallengeView()
        view.request = self.factory.post('development:challenge')
        view.form_valid(form)
        challenge = Challenge.objects.all().first()
        self.assertEqual(
            challenge.bot_challenger.name,
            'bot1'
        )
        self.assertEqual(
            challenge.bots_challenged.first().name,
            'bot2'
        )

    @patch('development.views.messages')
    @patch('requests.post')
    def test_should_raise_error_if_bot_challenger_doesnt_exists(self, post_patched, messages_patched):
        post_patched.return_value = HttpResponse(status=200)
        form = ChallengeForm({'bot1': '0', 'bot2': '1'})
        form.fields['bot1'].choices = [(0, 'bot_not_exists')]
        form.fields['bot2'].choices = [(0, 'bot_not_exists'), (1, 'bot2')]
        form.is_valid()
        view = ChallengeView()
        view.request = self.factory.post('development:challenge')
        view.form_valid(form)
        challenge = Challenge.objects.all().first()
        self.assertIsNone(challenge.bot_challenger)
