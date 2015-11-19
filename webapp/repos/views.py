from django.http import HttpResponse
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Repo
from .serializers import RepoSerializer


@api_view(['GET', 'POST'])
def repo_list(request):
    """
    List all repos, or create a new repo.
    """
    if request.method == 'GET':
        repos = Repo.objects.all()
        serializer = RepoSerializer(repos, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
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


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def repo_detail(request, id):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        repo = Repo.objects.get(id=id)
    except ValueError:
        # Not a valid for of a UUID
        return Response({'error': 'Not valid id'}, status=status.HTTP_404_NOT_FOUND)
    except Repo.DoesNotExist:
        print("here")
        # Repo does not exists
        return Response({'error': 'Rescource does not exist'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = RepoSerializer(repo)
        return Response(serializer.data)

    elif request.method == 'PUT':
        # keep old settings.
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

    elif request.method == 'DELETE':
        repo.remove()
        repo.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
