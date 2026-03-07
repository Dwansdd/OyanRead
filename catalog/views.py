from django.shortcuts import render
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.views import generic
from django.views.generic.detail import DetailView
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from rest_framework import viewsets

import requests
from requests.utils import quote

from catalog.models import Articles, Author, Genre


from .serializers import ArticleSerializer, ArticlesSerializer1

from oyan.forms import ArticleForm, UserRegisterForm
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


@login_required
def article_add_view_api(request):
    query = request.GET.get("q")
    article_added = None

    if query:
        headers = {"User-Agent": "Oyan/1.0 (duimagambetovadaneliya@example.com)"}
        url = f"https://kk.wikipedia.org/api/rest_v1/page/summary/{quote(query)}"
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
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
            if not Articles.objects.filter(title=data['title']).exists():
                serializer = ArticleSerializer(data=data)
                if serializer.is_valid():
                    serializer.save()
                    article_added = data 
                else:
                    print(serializer.errors)
            else:
                print("Такая статья уже есть")

    context = {
        "query": query,
        "article_added": article_added
    }

    return render(request, 'add_article.html', context)




def article_view_api():
    print("view!!")
    articles = [
        
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


class Search(generic.ListView):
    model=Articles
    template_name = 'article.html'

    def get_queryset(self):
        return Articles.objects.filter(title__icontains=self.request.GET.get('q'))
    #     query=self.request.GET.get('q')
    #     object_list=Articles.objects.filter(
    #         Q(name__icontains=query)
    # )
    #     return object_list
    
class archive_articleslist(generic.ListView):
    model=Articles
    template_name = 'article.html'
    context_object_name = "articles_list"


# LoginRequiredMixin
class ArticleDetailView(generic.DetailView):
    model=Articles
    template_name='article_detail.html'
    context_object_name = "article"


class ArticlesViewSet(viewsets.ModelViewSet):
    queryset = Articles.objects.all()
    serializer_class = ArticlesSerializer1


@login_required
def FormView(request):
    if request.method=="POST":
        form=ArticleForm(request.POST)
        if form.is_valid():
            article=form.save(commit=False)
            article.author=request.user
            article.save()
            return HttpResponseRedirect("сәтті жүктелді")
    else:
        form=ArticleForm()
    user_article=Articles.objects.filter(author=request.user)
    return render(
    request,
    "team_form.html",
    {
        "form": form,
        "user_article": user_article
    }
)

    


def ReigisterForm(request):
    if request.method=="POST":
        register_form=UserRegisterForm(request.POST)
    else:
        register_form=UserRegisterForm()

    if register_form.is_valid():
            register_form.save()
            username=register_form.cleaned_data.get("username")
            messages.success(request, f'сіз сәтті тіркелдіңіз {username}')
            return HttpResponseRedirect("/")
    return render(request,"registration_user.html", {"form":register_form})