from django.test import TestCase
from django.contrib.auth import get_user_model


class TestViewsAnonimous(TestCase):
    def test_home_no_authenticated(self):
        response = self.client.get('/')
        self.assertEqual(
            response.status_code,
            302,
        )
        self.assertEqual(
            response.url,
            '/accounts/login/?next=/',
        )
        self.assertRedirects(
            response,
            '/accounts/login/?next=/',
        )


class TestViewsAuthenticated(TestCase):
    def setUp(self):
        super().setUp()
        self.user = get_user_model().objects.create_user(
            "Gabriel",
            "gabriel@email.com",
            "my_pass",
        )
        self.client.force_login(self.user)

    def test_home_authenticated_no_tasks(self):
        response = self.client.get('/')
        self.assertEqual(
            response.status_code,
            200,
        )
        self.assertEqual(
            len(response.context['object_list']),
            0,
        )
        self.assertIn(
            'ahora',
            response.context,
        )

    # def test_home_authenticated_with_tasks(self):
    #     Todo.objects.bulk_create(
    #         [
    #             Todo(description='Buy', assigned_user=self.user),
    #             Todo(description='Pay', assigned_user=self.user),
    #             Todo(description='Diet', assigned_user=self.user),
    #         ],
    #         3
    #     )
    #     other_user = get_user_model().objects.create_user(
    #         "Pepe",
    #         "pepe@email.com",
    #         "my_pass",
    #     )
    #     Todo.objects.create(description='Beers', assigned_user=other_user)
    #     response = self.client.get('/')
    #     self.assertEqual(
    #         response.status_code,
    #         200,
    #     )
    #     self.assertEqual(
    #         len(response.context['object_list']),
    #         3,
    #     )
    #     self.assertIn(
    #         'ahora',
    #         response.context,
    #     )
    # def test_create_task(self):
    #     Todo.objects.bulk_create(
    #         [
    #             Todo(description='Buy', assigned_user=self.user),
    #             Todo(description='Pay', assigned_user=self.user),
    #             Todo(description='Diet', assigned_user=self.user),
    #         ],
    #         3
    #     )
    #     first_priority = Priority.objects.first()
    #     response = self.client.post(
    #         '/create/',
    #         {
    #             'description': 'Climb',
    #             'done': True,
    #             'priority': first_priority.id,
    #         }
    #     )
    #     self.assertEqual(
    #         Todo.objects.filter(assigned_user=self.user).count(),
    #         4,
    #     )
    #     last_todo = Todo.objects.last()
    #     self.assertRedirects(
    #         response,
    #         '/detail/{}/'.format(last_todo.id),
    #     )
    #     last_todo = Todo.objects.filter(assigned_user=self.user).last()
    #     self.assertEqual(
    #         last_todo.description,
    #         'Climb',
    #     )
    #     self.assertTrue(
    #         last_todo.done,
    #     )
    #     self.assertTrue(
    #         last_todo.priority,
    #         first_priority,
    #     )
    # def test_create_task_error(self):
    #     Todo.objects.bulk_create(
    #         [
    #             Todo(description='Buy', assigned_user=self.user),
    #             Todo(description='Pay', assigned_user=self.user),
    #             Todo(description='Diet', assigned_user=self.user),
    #         ],
    #         3
    #     )
    #     response = self.client.post(
    #         '/create/',
    #         {
    #             'description': 'Climb',
    #         }
    #     )
    #     self.assertEqual(
    #         response.status_code,
    #         200,
    #     )
    #     self.assertEqual(
    #         Todo.objects.filter(assigned_user=self.user).count(),
    #         3,
    #     )
