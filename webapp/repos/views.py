from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

from .models import Repo
from .serializers import RepoSerializer


class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


@csrf_exempt
def repo_list(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        repos = Repo.objects.all()
        serializer = RepoSerializer(repos, many=True)
        return JSONResponse(serializer.data)

    elif request.method == 'POST':
        try:
            data = JSONParser().parse(request)
        except:
            return JSONResponse({'error': 'Invalid JSON'}, status=400)

        serializer = RepoSerializer(data=data)
        if serializer.is_valid():
            repo = serializer.create(serializer.validated_data)

            try:
                repo.download()
            except Exception as e:
                print("ERROR %s" %e)
                return JSONResponse({'error': str(e)}, status=400)

            # TODO add logger
            print("Created Repo from POST...")
            print(repo.url)
            print(repo.branch)
            print(repo.revision)

            return JSONResponse(serializer.data, status=201)
        return JSONResponse(serializer.errors, status=400)

@csrf_exempt
def repo_detail(request, id):
    """
    Retrieve, update or delete a code snippet.
    """
    print(id)
    try:
        repo = Repo.objects.get(id=id)
    except ValueError:
        # Not a valid for of a UUID
        return HttpResponse(status=404)
    except Repo.DoesNotExist:
        # Repo does not exists
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = RepoSerializer(repo)
        return JSONResponse(serializer.data)

    elif request.method == 'DELETE':
        repo.remove()
        repo.delete()
        return HttpResponse(status=204)