from django.test import TestCase
from django.test import Client
from django.core.urlresolvers import reverse
from django.utils.six import BytesIO

from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.parsers import JSONParser

from repos.models import Repo
import json
# Create your tests here.

class RepoTestCase(TestCase):
    def setUp(self):
        Repo.objects.create(name="testrepo", url="https://github.com/rjor2/melosycn")

    def tearDown(self):
        repo = Repo.objects.get(name="testrepo")
        repo.remove()

    def test_downloaded(self):
        repo = Repo.objects.get(name="testrepo")
        repo.download()
        self.assertEqual(repo.downloaded, True)


class RepoAPITestCase(APITestCase):
    # Probably should be using a fixture of some sort.
    def test_post(self):
        url = "/repos/"
        data = {'url': 'https://github.com/rjor2/melosycn', 'name': 'testrepo'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Repo.objects.count(), 1)
        self.assertEqual(Repo.objects.get().url, 'https://github.com/rjor2/melosycn')

    def test_get(self):
        self.test_post()
        repo = Repo.objects.get(name="testrepo")
        url = "/repos/%s/" %repo.id
        response = self.client.get(url)
        stream = BytesIO(response.content)
        data = JSONParser().parse(stream)
        self.assertEqual(data['name'], "testrepo")
        self.assertIn('id', data)
        self.assertIn('url', data)
        self.assertIn('branch', data)
        self.assertIn('revision', data)
        # self.assertIn('stats', data)

    def test_delete(self):
        self.test_post()
        repo = Repo.objects.get(name="testrepo")
        url = "/repos/%s/" %repo.id
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def tearDown(self):
        try:
            repo = Repo.objects.get(name="testrepo")
            repo.remove()
        except:
            pass
