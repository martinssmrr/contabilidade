from django.urls import path
from .views import PostListView, PostDetailView, PostsByTagView, load_more_posts
from .feeds import BlogPostsFeed, CategoryFeed

app_name = 'blog'

urlpatterns = [
    path('', PostListView.as_view(), name='post_list'),
    path('load-more/', load_more_posts, name='load_more'),
    path('feed/', BlogPostsFeed(), name='rss_feed'),
    path('feed/categoria/<slug:slug>/', CategoryFeed(), name='category_feed'),
    path('tag/<slug:slug>/', PostsByTagView.as_view(), name='tag'),
    path('<slug:slug>/', PostDetailView.as_view(), name='post_detail'),
]
