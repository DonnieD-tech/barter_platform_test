from django.test import TestCase, Client
from django.contrib.auth.models import User
from ads.models import Ad, Category, ExchangeProposal


class AdTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password')
        self.category = Category.objects.create(name='Test Category')
        self.ad_data = {
            'title': 'Test Ad',
            'description': 'Test description',
            'category': self.category.id,  # Важно! id категории
            'condition': 'new',
        }

    def test_create_ad(self):
        self.client.login(username='testuser', password='password')
        response = self.client.post('/ads/create/', data=self.ad_data, follow=True)
        self.assertEqual(response.status_code, 200)  # Ожидаем успешный переход
        self.assertEqual(Ad.objects.count(), 1)
        ad = Ad.objects.first()
        self.assertEqual(ad.title, 'Test Ad')

    def test_edit_ad(self):
        ad = Ad.objects.create(
            user=self.user,
            title='Test Ad',
            description='Test description',
            category=self.category,
            condition='new',
        )
        self.client.login(username='testuser', password='password')
        response = self.client.post(f'/ads/{ad.pk}/edit/', {
            'title': 'Updated Title',
            'description': ad.description,
            'category': self.category.id,  # id!
            'condition': ad.condition,
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        ad.refresh_from_db()
        self.assertEqual(ad.title, 'Updated Title')

    def test_delete_ad(self):
        ad = Ad.objects.create(
            user=self.user,
            title='Test Ad',
            description='Test description',
            category=self.category,
            condition='new',
        )
        self.client.login(username='testuser', password='password')
        response = self.client.post(f'/ads/{ad.pk}/delete/', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Ad.objects.count(), 0)

    def test_search_ads(self):
        Ad.objects.create(
            user=self.user,
            title='Find Me',
            description='Hidden gem',
            category=self.category,
            condition='new',
        )
        response = self.client.get('/', {'q': 'Find'})
        self.assertContains(response, 'Find Me')


class ExchangeProposalTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.sender = User.objects.create_user(username='sender', password='password')
        self.receiver = User.objects.create_user(username='receiver', password='password')
        self.category = Category.objects.create(name='Test Category')
        self.ad_sender = Ad.objects.create(
            user=self.sender,
            title='Sender Ad',
            description='Sender ad description',
            category=self.category,
            condition='new',
        )
        self.ad_receiver = Ad.objects.create(
            user=self.receiver,
            title='Receiver Ad',
            description='Receiver ad description',
            category=self.category,
            condition='used',
        )

    def test_create_exchange_proposal(self):
        self.client.login(username='sender', password='password')
        response = self.client.post('/exchange/create/', {
            'ad_sender': self.ad_sender.pk,
            'ad_receiver': self.ad_receiver.pk,
            'comment': 'Want to trade?',
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(ExchangeProposal.objects.count(), 1)

    def test_accept_exchange_proposal(self):
        proposal = ExchangeProposal.objects.create(
            ad_sender=self.ad_sender,
            ad_receiver=self.ad_receiver,
            status='pending',
        )
        self.client.login(username='receiver', password='password')
        response = self.client.post(f'/exchange/{proposal.pk}/accept/', follow=True)
        self.assertEqual(response.status_code, 200)
        proposal.refresh_from_db()
        self.assertEqual(proposal.status, 'accepted')

    def test_decline_exchange_proposal(self):
        proposal = ExchangeProposal.objects.create(
            ad_sender=self.ad_sender,
            ad_receiver=self.ad_receiver,
            status='pending',
        )
        self.client.login(username='receiver', password='password')
        response = self.client.post(f'/exchange/{proposal.pk}/decline/', follow=True)
        self.assertEqual(response.status_code, 200)
        proposal.refresh_from_db()
        self.assertEqual(proposal.status, 'declined')
