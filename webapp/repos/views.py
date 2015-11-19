from rest_framework import status

from rest_framework.views import APIView
from django.http import Http404
from rest_framework.response import Response

from .models import Repo
from .serializers import RepoSerializer

class RepoList(APIView):
    """
    List all repos, or create a new repo.
    """
    def get(self, request, format=None):
        repos = Repo.objects.all()
        serializer = RepoSerializer(repos, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = RepoSerializer(data=request.data)
        if serializer.is_valid():
            repo = serializer.create(serializer.validated_data)

            try:
                repo.download()
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

            # TODO add logger
            print("Created Repo from POST...")
            print(repo.url)
            print(repo.branch)
            print(repo.revision)

            # If using celery change this to 202
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RepoDetail(APIView):
    """
    Retrieve, update or delete a code snippet.
    """

    def get_object(self, id):
        try:
            return Repo.objects.get(id=id)
        except ValueError:
            # Incorrect formate for uuid
            raise Http404
        except Repo.DoesNotExist:
            # Repo does not exists
            raise Http404

    def get(self, request, id, format=None):
        repo = self.get_object(id)
        serializer = RepoSerializer(repo)
        return Response(serializer.data)

    def put(self, request, id, format=None):
        # keep old settings.
        repo = self.get_object(id)
        old_branch = repo.branch
        old_revision = repo.revision
        serializer = RepoSerializer(repo, data=request.data)
        if serializer.is_valid():
            if serializer.validated_data['url'] != repo.url:
                return Response({'error': 'Cannot change url. Please use Post to create a new resource.'},
                                status=status.HTTP_400_BAD_REQUEST)
            repo = serializer.save()
            try:
                repo.update()
            except Exception as e:
                # put back old settings.
                repo.branch = old_branch
                repo.revision = old_revision
                repo.save()
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, format=None):
        repo = self.get_object(id)
        repo.remove()
        repo.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
