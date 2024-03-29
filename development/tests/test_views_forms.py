from unittest.mock import patch

from django.http import HttpResponse
from django.test import RequestFactory, TestCase
from parameterized import parameterized

from ..views import (
    AddBotView,
    ChallengeView,
    MatchListView,
    MyBotsView,
)

from auth_app.models import User, Bot
from ..forms import ChallengeForm


class TestView(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user1 = User.objects.create(email='test1@gmail.com', username='UsuarioTest1')
        self.bot1 = Bot.objects.create(name='bot1', user=self.user1)
        self.user2 = User.objects.create(email='test2@gmail.com', username='UsuarioTest2')
        self.bot2 = Bot.objects.create(name='bot2', user=self.user2)

    def test_get_form_get(self):
        request = self.factory.get('development:challenge')
        request.user = self.user1
        response = ChallengeView.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_get_form_post(self):
        request = self.factory.post('development:challenge')
        request.user = self.user1
        response = ChallengeView.as_view()(request)
        self.assertEqual(response.status_code, 200)

    @parameterized.expand(
        [
            ('with_debug_mode_enable', True,),
            ('with_debug_mode_disable', False,),
        ]
    )
    @patch('development.views.messages')
    @patch('requests.post')
    def test_form_valid(self, name, debug_mode, post_patched, messages_patched):
        post_patched.return_value = HttpResponse(status=200)
        form = ChallengeForm({'bot1': '0', 'bot2': '1', 'debug_mode': debug_mode})
        form.fields['bot1'].choices = [(0, 'bot1')]
        form.fields['bot2'].choices = [(0, 'bot1'), (1, 'bot2')]
        form.is_valid()
        view = ChallengeView()
        view.request = self.factory.post('development:challenge')
        view.form_valid(form)
        post_patched.assert_called()

    def test_get_queryset_match_history(self):
        request = self.factory.get('development:match_history')
        request.user = self.user1
        response = MatchListView.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_get_queryset_my_bots(self):
        request = self.factory.get('development:my_bots')
        request.user = self.user1
        response = MyBotsView.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_get_form_add_bot_get(self):
        request = self.factory.get('development:addbot')
        request.user = self.user1
        response = AddBotView.as_view()(request)
        self.assertEqual(response.status_code, 200)

    @patch('development.views.messages')
    def test_get_form_add_bot_post_ok(self, patched_message):
        prev_cant = Bot.objects.filter(name='botty').count()
        request = self.factory.post('development:addbot', {'name': 'botty'})
        request.user = self.user1
        response = AddBotView.as_view()(request)
        post_cant = Bot.objects.filter(name='botty').count()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(prev_cant, 0)
        self.assertEqual(post_cant, 1)

    @patch('development.views.messages')
    def test_get_form_add_bot_post_wrong(self, patched_message):
        prev_cant = Bot.objects.filter(name='bot2').count()
        request = self.factory.post('development:addbot', {'name': 'bot2'})
        request.user = self.user1
        post_cant = Bot.objects.filter(name='bot2').count()
        response = AddBotView.as_view()(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(prev_cant, 1)
        self.assertEqual(post_cant, 1)
