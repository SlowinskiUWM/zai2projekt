from rest_framework import viewsets
from .models import Movie
from .serializers import MovieSerializer, DescriptionSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response

from django.db.models.functions import Length
from django.db.models import Avg, Max


class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all().order_by('-id')
    serializer_class = MovieSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'])
    def count(self, request):
        count = self.get_queryset().count()
        return Response({'count': count})

    @action(detail=False, methods=['get'])
    def latest(self, request):
        movie = self.get_queryset().order_by('-id').first()
        serializer = self.get_serializer(movie)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def oldest(self, request):
        movie = self.get_queryset().order_by('id').first()
        serializer = self.get_serializer(movie)
        return Response(serializer.data)

    @action(detail=True, methods=['post', 'get'])
    def del_description(self, request, pk=None):
        movie = self.get_object()
        movie.description = None
        movie.save()
        return Response({'Tytuł': movie.title, 'Opis': movie.description})

    @action(detail=True, methods=['post', 'get'])
    def add_to_description(self, request, pk=None):
        movie = self.get_object()

        serializer = DescriptionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        message = serializer.validated_data.get('description') or 'OPIS FILMU'

        # message = request.data.get('description') or 'OPIS FILMU'

        if not movie.description:
            movie.description = message
        else:
            movie.description = movie.description + ' ' + message

        movie.save()
        return Response({'Tytuł': movie.title, 'Opis': movie.description})



    @action(detail=False, methods=['get'])
    def longest_descriptions(self, request):
        queryset = self.get_queryset()\
            .filter(description__isnull=False)\
            .annotate(dl_opisu=Length('description'))\
            .order_by('-dl_opisu')

        serializer = self.get_serializer(queryset, many=True)

        # dodajemy długość do odpowiedzi
        data = serializer.data
        for i, movie in enumerate(queryset):
            data[i]['dl_opisu'] = movie.dl_opisu

        return Response(data)

    @action(detail=False, methods=['get'])
    def avg_description_length(self, request):
        result = self.get_queryset()\
            .annotate(dl_opisu=Length('description'))\
            .aggregate(srednia=Avg('dl_opisu'))

        return Response(result)

    @action(detail=False, methods=['get'])
    def max_description_length(self, request):
        result = self.get_queryset()\
            .annotate(dl_opisu=Length('description'))\
            .aggregate(max_dl=Max('dl_opisu'))

        return Response(result)

    @action(detail=False, methods=['get'])
    def longest_description_movie(self, request):
        movie = self.get_queryset()\
            .annotate(dl_opisu=Length('description'))\
            .order_by('-dl_opisu')\
            .first()

        if not movie:
            return Response({'error': 'Brak filmów'})

        return Response({
            'Tytuł': movie.title,
            'Opis': movie.description,
            'dl_opisu': movie.dl_opisu
        })