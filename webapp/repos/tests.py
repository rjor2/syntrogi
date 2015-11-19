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

    def test_downloaded_invalid_url(self):
        repo = Repo.objects.get(name="testrepo")
        repo.url = "https://'':''@github.com/rjor2/made_up_url"
        with self.assertRaises(Exception) as e:
            repo.download()
        self.assertEqual(u"Git Repo does not exist or is password protected.", str(e.exception))
        self.assertEqual(repo.downloaded, False)

    def test_downloaded_invalid_branch(self):
        repo = Repo.objects.get(name="testrepo")
        repo.branch = "made_up_branch"
        with self.assertRaises(Exception) as e:
            repo.download()
        self.assertEqual(u"Branch does not exist.", str(e.exception))
        self.assertEqual(repo.downloaded, False)

    def test_downloaded_invalid_revision(self):
        repo = Repo.objects.get(name="testrepo")
        repo.revision = "made_up_commit"
        with self.assertRaises(Exception) as e:
            repo.download()
        self.assertEqual(u"Revision does not exist.", str(e.exception))
        self.assertEqual(repo.downloaded, False)

    def test_remove(self):
        repo = Repo.objects.get(name="testrepo")
        repo.download()
        repo.remove()
        self.assertEqual(True, True)

    def test_remove_with_no_folder(self):
        repo = Repo.objects.get(name="testrepo")
        repo.remove()
        self.assertEqual(True, True)

class RepoAPITestCase(APITestCase):
    # Probably should be using a fixture of some sort.

    # Test POST
    def test_post(self):
        url = "/repos/"
        data = {'url': 'https://github.com/rjor2/syntrogi', 'name': 'testrepo'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Repo.objects.count(), 1)
        self.assertEqual(Repo.objects.get().url, 'https://github.com/rjor2/syntrogi')

    def test_post_with_branch(self):
        url = "/repos/"
        data = {'url': 'https://github.com/rjor2/syntrogi', 'branch': 'dev', 'name': 'testrepo'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Repo.objects.get().url, 'https://github.com/rjor2/syntrogi')
        self.assertEqual(Repo.objects.get().branch, 'dev')

    def test_post_with_revision(self):
        url = "/repos/"
        data = {'url': 'https://github.com/rjor2/syntrogi', 'revision': 'e9fb0c8c4fff1b67f5f2c3984335df75d4acf754', 'name': 'testrepo'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Repo.objects.get().url, 'https://github.com/rjor2/syntrogi')
        self.assertEqual(Repo.objects.get().revision, 'e9fb0c8c4fff1b67f5f2c3984335df75d4acf754')

    def test_post_with_incorrect_url(self):
        url = "/repos/"
        data = {'url': 'https://'':''@github.com/made_up_url', 'name': 'testrepo'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 400)
        stream = BytesIO(response.content)
        data = JSONParser().parse(stream)
        self.assertIn('error', data)

    def test_post_with_incorrect_branch(self):
        url = "/repos/"
        data = {'url': 'https://github.com/rjor2/syntrogi', 'branch': 'made_up_branch', 'name': 'testrepo'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 400)
        stream = BytesIO(response.content)
        data = JSONParser().parse(stream)
        self.assertIn('error', data)

    def test_post_with_incorrect_revision(self):
        url = "/repos/"
        data = {'url': 'https://github.com/rjor2/syntrogi', 'revision': 'made_up_revision', 'name': 'testrepo'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 400)
        stream = BytesIO(response.content)
        data = JSONParser().parse(stream)
        self.assertIn('error', data)

    # Test GET
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

    # Test DELETE
    def test_delete(self):
        self.test_post()
        repo = Repo.objects.get(name="testrepo")
        url = "/repos/%s/" %repo.id
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    # Test PUT
    def test_put(self):
        repo = Repo.objects.create(name="testrepo", url="https://github.com/rjor2/syntrogi")
        repo.download()
        url = "/repos/%s/" %repo.id
        data = {'url': repo.url, 'branch': 'dev'}
        response = self.client.put(url, data, format='json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Repo.objects.get().branch, 'dev')

    def test_put_with_incorrect_branch(self):
        repo = Repo.objects.create(name="testrepo2", url="https://github.com/rjor2/syntrogi")
        repo.download()
        url = "/repos/%s/" %repo.id
        data = {'url': repo.url, 'branch': 'made_up_branch'}
        response = self.client.put(url, data, format='json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(Repo.objects.get().branch, repo.branch)

    def tearDown(self):
        try:
            repo = Repo.objects.get(name="testrepo")
            repo.remove()
        except:
            pass
