from django.urls import path
from .views import PostListView, PostDetailView, load_more_posts

app_name = 'blog'

urlpatterns = [
    path('', PostListView.as_view(), name='post_list'),
    path('load-more/', load_more_posts, name='load_more'),
    path('<slug:slug>/', PostDetailView.as_view(), name='post_detail'),
]
