from django.contrib import admin

from .models import Articles,Author, Genre

admin.site.register(Articles)
admin.site.register(Author)
admin.site.register(Genre)
