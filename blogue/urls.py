from django.urls import path
from .views import details, like_comment, tag_details, get_articles, unlike_comment

urlpatterns = [
    path("article/<slug:slug>/details", details, name="article-details"),
    path("tag/<slug:slug>/tag-details", tag_details, name="tag-details"),
    path('get-articles/<slug:slug>/', get_articles, name='get-articles'),
    path('comment/<int:comment_id>/like/', like_comment, name='like-comment'),
    path('comment/<int:comment_id>/unlike/', unlike_comment, name='unlike-comment'),
]