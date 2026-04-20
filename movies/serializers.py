from rest_framework import serializers
from .models import Movie

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'


class MovieSerializerTEST(serializers.Serializer):
    title = serializers.CharField(max_length=200)
    year = serializers.IntegerField()
    description = serializers.CharField(allow_blank=True)
    created_at = serializers.DateTimeField()

    def create(self, validated_data):
        return Movie.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.year = validated_data.get('year', instance.year)
        instance.description = validated_data.get('description', instance.description)
        instance.created_at = validated_data.get('created_at', instance.created_at)
        instance.save()
        return instance





