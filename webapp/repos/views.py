from rest_framework import status
from rest_framework import mixins
from rest_framework import generics
from rest_framework.response import Response

from .models import Repo
from .serializers import RepoSerializer

class RepoList(mixins.ListModelMixin,
               mixins.CreateModelMixin,
               generics.GenericAPIView):
    """
    List all repos, or create a new repo.
    """

    queryset = Repo.objects.all()
    serializer_class = RepoSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

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


class RepoDetail(mixins.RetrieveModelMixin,
                 mixins.UpdateModelMixin,
                 mixins.DestroyModelMixin,
                 generics.GenericAPIView):
    """
    Retrieve, update or delete a code snippet.
    """

    queryset = Repo.objects.all()
    serializer_class = RepoSerializer#
    lookup_field = 'id'

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, id, format=None):
        # keep old settings.
        repo = self.get_object()
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
        repo = self.get_object()
        repo.remove()
        repo.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
