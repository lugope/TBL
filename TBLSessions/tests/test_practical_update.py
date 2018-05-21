from django.core.urlresolvers import reverse_lazy
from django.shortcuts import reverse
from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from core.test_utils import check_messages
from model_mommy import mommy
from TBLSessions.models import TBLSession

User = get_user_model()


class UpdatePracticalTestCase(TestCase):
    """
    Test to update the practical test.
    """

    def setUp(self):
        """
        This method will run before any test case.
        """
        self.client = Client()
        self.session = mommy.make('TBLSession')
        self.teacher = User.objects.create_user(
            username='someTeacher',
            email='someTeacher@email.com',
            password='somepass',
            is_teacher=True,
        )
        self.session.discipline.teacher = self.teacher
        self.session.discipline.save()

        self.url = reverse('TBLSessions:practical-update',
                           kwargs={'slug': self.session.discipline.slug,
                                   'pk': self.session.pk})

    def tearDown(self):
        """
        This method will run after any test.
        """
        self.teacher.delete()

    def test_only_teacher_can_update(self):
        """
        Teacher and monitors that is a teacher can update the practical test.
        """
        self.client.login(
            username=self.teacher.username,
            password='somepass'
        )

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
