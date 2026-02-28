from catalog.models import Articles,Genre
from rest_framework import serializers

class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model=Articles
        fields = '__all__'
        extra_kwargs = {'author': {'required': False}, 'genre': {'required': False}}
class ArticlesSerializer1(serializers.ModelSerializer):
    # Optional: Nested serializers to show name instead of ID
    author_name = serializers.ReadOnlyField(source='author.name')
    genre_name = serializers.ReadOnlyField(source='genre.name')

    class Meta:
        model = Articles
        fields = '__all__'