from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response

from .models import Repo
from .serializers import RepoSerializer

import logging

logger = logging.getLogger('default')

class RepoList(generics.ListCreateAPIView):
    """
    List all repos, or create a new repo.
    """

    queryset = Repo.objects.all()
    serializer_class = RepoSerializer

    def post(self, request, format=None):
        serializer = RepoSerializer(data=request.data)

        if serializer.is_valid():
            repo = serializer.create(serializer.validated_data)

            try:
                repo.download()
            except Exception as e:
                # Probably should override some self.create method now
                repo.delete()
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

            logger.debug("Created Repo from POST id:%s url:%s branch:%s revision:%s downloaded:%s" \
                         %(repo.id, repo.url, repo.branch, repo.revision, repo.downloaded))

            # If using celery change this to 202
            return Response(RepoSerializer(repo).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RepoDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a code snippet.
    """

    queryset = Repo.objects.all()
    serializer_class = RepoSerializer#
    lookup_field = 'id'

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
