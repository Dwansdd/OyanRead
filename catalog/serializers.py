from catalog.models import Articles
from rest_framework import serializers

class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model=Articles
        fields = '__all__'
        extra_kwargs = {'author': {'required': False}}
class ArticlesSerializer1(serializers.ModelSerializer):
    # Optional: Nested serializers to show name instead of ID
    author_name = serializers.ReadOnlyField(source='author.name')

    class Meta:
        model = Articles
        fields = '__all__'