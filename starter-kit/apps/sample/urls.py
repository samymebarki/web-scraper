from django import views
from django.urls import path
from .views import SampleView,category_articles


urlpatterns = [
    path(
        "",
        SampleView.as_view(template_name="index.html"),
        name="index",
    ),
    path(
        "page_2/",
        SampleView.as_view(template_name="page_2.html"),
        name="page-2",
    ),
    path('category/Computing/', category_articles, name='category_articles'),
]
