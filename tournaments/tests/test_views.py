from auth_app.models import User
from django.test import RequestFactory, TestCase
from ..views import CreateTournamentView


class TestCreateTournamentView(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user1 = User.objects.create_superuser(username='username1', password='password1', email='email1')
        self.user1.is_staff = True
        self.user2 = User.objects.create(username='username2', password='password2', email='email2')

    def test_get_form_get(self):
        request = self.factory.get('tournaments:create_tournament')
        request.user = self.user1
        response = CreateTournamentView.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_get_form_post(self):
        request = self.factory.post('tournaments:create_tournament')
        request.user = self.user1
        response = CreateTournamentView.as_view()(request)
        self.assertEqual(response.status_code, 200)

    # @patch('tournaments.views.messages')
    # @patch('requests.post')
    # def test_form_valid(self, post_patched, messages_patched):
    #     post_patched.return_value = HttpResponse(status=200)
    #     form = ChallengeForm({'bot1': '0', 'bot2': '1'})
    #     form.fields['bot1'].choices = [(0, 'bot1')]
    #     form.fields['bot2'].choices = [(0, 'bot1'), (1, 'bot2')]
    #     form.is_valid()
    #     view = ChallengeView()
    #     view.request = self.factory.post('development:challenge')
    #     view.form_valid(form)
    #     post_patched.assert_called()

    # def test_get_queryset_match_history(self):
    #     request = self.factory.get('development:match_history')
    #     request.user = self.user1
    #     response = MatchListView.as_view()(request)
    #     self.assertEqual(response.status_code, 200)

    # def test_get_queryset_my_bots(self):
    #     request = self.factory.get('development:my_bots')
    #     request.user = self.user1
    #     response = MyBotsView.as_view()(request)
    #     self.assertEqual(response.status_code, 200)

    # def test_get_form_add_bot_get(self):
    #     request = self.factory.get('development:addbot')
    #     request.user = self.user1
    #     response = AddBotView.as_view()(request)
    #     self.assertEqual(response.status_code, 200)









    # @patch('development.views.messages')
    # def test_get_form_add_bot_post_ok(self, patched_message):
    #     prev_cant = Bot.objects.filter(name='botty').count()
    #     request = self.factory.post('development:addbot', {'name': 'botty'})
    #     request.user = self.user1
    #     response = AddBotView.as_view()(request)
    #     post_cant = Bot.objects.filter(name='botty').count()
    #     self.assertEqual(response.status_code, 302)
    #     self.assertEqual(prev_cant, 0)
    #     self.assertEqual(post_cant, 1)

    # @patch('development.views.messages')
    # def test_get_form_add_bot_post_wrong(self, patched_message):
    #     prev_cant = Bot.objects.filter(name='bot2').count()
    #     request = self.factory.post('development:addbot', {'name': 'bot2'})
    #     request.user = self.user1
    #     post_cant = Bot.objects.filter(name='bot2').count()
    #     response = AddBotView.as_view()(request)
    #     self.assertEqual(response.status_code, 302)
    #     self.assertEqual(prev_cant, 1)
    #     self.assertEqual(post_cant, 1)
