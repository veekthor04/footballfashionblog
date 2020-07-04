from django.urls import path
from . import views

urlpatterns = [
    path('', views.blog_index, name = 'blog_index'),
    path("post/<int:pk>/", views.blog_detail, name="blog_detail"),
    path("post/<category>/", views.blog_category, name="blog_category"),
    path("contact/", views.blog_contact, name="blog_contact"),
    path("about/", views.blog_about, name="blog_about"),
]
