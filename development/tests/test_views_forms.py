from auth_app.models import User, Bot
from django.test import RequestFactory, TestCase
from ..views import ChallengeView, MatchListView
from ..forms import ChallengeForm
from unittest.mock import patch
from django.http import HttpResponse


class TestChallengeView(TestCase):
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

    def test_get_queryset(self):
        request = self.factory.get('development:match_history')
        request.user = self.user1
        response = MatchListView.as_view()(request)
        self.assertEqual(response.status_code, 200)

    @patch('development.views.messages')
    @patch('requests.post')
    def test_form_valid(self, post_patched, messages_patched):
        post_patched.return_value = HttpResponse(status=200)
        form = ChallengeForm({'bot1': '0', 'bot2': '1'})
        form.fields['bot1'].choices = [(0, 'bot1')]
        form.fields['bot2'].choices = [(0, 'bot1'), (1, 'bot2')]
        form.is_valid()
        view = ChallengeView()
        view.request = self.factory.post('development:challenge')
        view.form_valid(form)
        post_patched.assert_called()