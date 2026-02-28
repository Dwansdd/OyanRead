from django.shortcuts import render
import requests
from .models import Articles, Author, Genre
from django.http import JsonResponse, HttpResponse
from catalog.models import Articles
from .serializers import ArticleSerializer
from django.views.generic.detail import DetailView
from django.views import generic
from catalog.models import Articles
from requests.utils import quote
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework import viewsets
from .models import Author, Genre, Articles
from .serializers import ArticlesSerializer1
# прописываем логику в обьект request 

def index(request):
    num_articles=Articles.objects.all().count()
    num_authors=Author.objects.count()
# передаем в шаблон в контенте
    return render(
        request,
        'index.html',
        context={'num_articles':num_articles,'num_authors':num_authors},
    )

# рендер оборачивает несколько вызовов в один и ищет файл куда будет вставялтся шаблон
def article_view_api(req):
    print("view!!")
    articles = [
        "Алматы",
        "Астана",
        "Қазақстан",
        "Шымкент"
    ]
    headers = {"User-Agent": "Oyan/1.0 (duimagambetovadaneliya@example.com)"}
    for title in articles:
        url = f"https://kk.wikipedia.org/api/rest_v1/page/summary/{quote(title)}"
        response=requests.get(url,headers=headers)
        if response.status_code==200:
            wiki_data = response.json()
            data = {
            "title": wiki_data.get("title"),
            "description": wiki_data.get("extract"),
            "content": wiki_data.get("extract"),
            "image": wiki_data.get("thumbnail", {}).get("source"),
            "source_url": wiki_data.get("content_urls", {})
                    .get("desktop", {})
                    .get("page"),
}
            if Articles.objects.filter(title=data['title']).exists():
                continue

            serializer=ArticleSerializer(data=data)
            if  serializer.is_valid():
                serializer.save()
            else:
                print(serializer.errors)
    return HttpResponse("Articles saved successfully")


class archive_articleslist(generic.ListView):
    model=Articles
    template_name = 'article.html'
    context_object_name = "articles_list"
# LoginRequiredMixin
class ArticleDetailView(generic.DetailView):
    model=Articles
    template_name='article_detail.html'
    context_object_name = "article"

# user=User.objects.create_user('myusername', 'myemail@crazymail.com', 'mypassword')

# user.first_name='Daneliya'
# user.last_name='Duima'

# user.save()

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["now"] = timezone.now()
#         return context

class ArticlesViewSet(viewsets.ModelViewSet):
    queryset = Articles.objects.all()
    serializer_class = ArticlesSerializer1