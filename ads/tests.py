from django.test import TestCase
from django.contrib.auth.models import User
from .models import Ad, ExchangeProposal

class AdTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.ad = Ad.objects.create(
            user=self.user,
            title="Книга",
            description="Отличная книга для обмена",
            category="Книги",
            condition="new",
        )

    def test_create_ad(self):
        ad_count = Ad.objects.count()
        self.assertEqual(ad_count, 1)
        self.assertEqual(self.ad.title, "Книга")

    def test_edit_ad(self):
        self.ad.title = "Обновленная книга"
        self.ad.save()
        self.assertEqual(Ad.objects.get(id=self.ad.id).title, "Обновленная книга")

    def test_delete_ad(self):
        ad_id = self.ad.id
        self.ad.delete()
        self.assertFalse(Ad.objects.filter(id=ad_id).exists())

class ExchangeProposalTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='pass1')
        self.user2 = User.objects.create_user(username='user2', password='pass2')
        self.ad1 = Ad.objects.create(
            user=self.user1,
            title="Ноутбук",
            description="Рабочий ноутбук",
            category="Электроника",
            condition="used",
        )
        self.ad2 = Ad.objects.create(
            user=self.user2,
            title="Смартфон",
            description="Хороший телефон",
            category="Электроника",
            condition="used",
        )

    def test_create_exchange_proposal(self):
        proposal = ExchangeProposal.objects.create(
            ad_sender=self.ad1,
            ad_receiver=self.ad2,
            comment="Готов обменяться"
        )
        self.assertEqual(proposal.status, 'pending')
        self.assertEqual(proposal.ad_sender.title, "Ноутбук")
