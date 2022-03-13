from rest_framework import views, status, generics
from rest_framework.response import Response

from comics.models import Comic
from comics.serializers import ComicSerializer
from comics.utils import normalize_content
from core.es import search


class RandomView(generics.ListAPIView):

    queryset = Comic.objects.order_by("?")[:60]
    serializer_class = ComicSerializer


class DetailView(generics.RetrieveAPIView):
    serializer_class = ComicSerializer
    queryset = Comic.objects.all()


class SearchView(views.APIView):

    def get(self, request):
        query_param = normalize_content(request.GET.get("q"))

        query = {
            "match": {
                "content": {
                    "query": query_param,
                    "operator": "and"
                }
            }
        }

        if query_param:
            data = search('comic', query=query)
            data = data["hits"]
            http_status = status.HTTP_200_OK
        else:
            data = {
                "error": "null value",
                "code": 100
            }
            http_status = status.HTTP_400_BAD_REQUEST
        return Response(data, status=http_status)