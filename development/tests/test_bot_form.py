from django.test import TestCase
from development.forms import BotForm
from parameterized import parameterized


class AddBotFormTest(TestCase):
    @parameterized.expand([
        ['letters', {'name': 'adsajdqwhjhwqje'}],
        ['numbers', {'name': '12343534'}],
        ['letters_and_numbers', {'name': 'thsjh3j412932hj'}],
    ])
    def test_bot_name_correct_input_data(
        self,
        _test_name,
        data,
    ):
        bot_form = BotForm(data=data)

        self.assertEqual(
            bot_form.errors,
            {},
        )

    def test_it_should_return_error_when_bot_name_contains_symbols(self):
        bot_form = BotForm(data={'name': 'asdas!@#@3213'})

        self.assertEqual(
            bot_form.errors['name'],
            ['Name cannot contains symbols or spaces'],
        )
