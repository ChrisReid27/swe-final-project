from django.test import TestCase
from rest_framework.test import APIRequestFactory
from rest_framework.test import APIClient
from django.urls import include, path, reverse
from rest_framework import status
from rest_framework.test import APITestCase, URLPatternsTestCase
import json

class LeaderboardTest(APITestCase, URLPatternsTestCase):

	urlpatterns = [
		path('api/', include('gridquiz.quickstart.urls')),
		path('api/accounts/', include('accounts.urls')),
	]
	
	def test_create_entry(self):
		factory = APIRequestFactory()

		# login
		request = factory.post('/accounts/register', {'username' : 'johnthebest', 'email' : 'sample@gmail.com', 'password' : 'blue42', 'password2' : 'blue42' })

		client = APIClient()
		client.login(username='johnthebest', password='blue42')



		# test creating a leaderboard entry
		request = client.post('/game/4/leaderboard', {'score' : 1000, 'time_taken' : 100})
		self.assertEqual(request, 'e')

		#response = client.get('/game/4/leaderboard')

		#self.assertEqual(json.loads(response.data), {'id': 4, 'username': 'johnthebest'})

		client.logout()

