from django.urls import path
from .views import NewsList, PostDetail, PostCreate, PostUpdate, PostDelete, CategoryListView, SubscribeView

app_name = 'news'

urlpatterns = [
    path('', NewsList.as_view(), name='news_list'),
    path('post/<int:pk>/', PostDetail.as_view(), name='about_new'),
    path('post/create/', PostCreate.as_view(), {'is_article': False}, name='create_news'),
    path('post/<int:pk>/edit/', PostUpdate.as_view(), name='edit_news'),
    path('post/<int:pk>/delete/', PostDelete.as_view(), name='delete_news'),
    

    # path('news/<int:pk>/edit/', PostUpdate.as_view(), name='edit_news'),
    # path('news/<int:pk>/delete/', PostDelete.as_view(), name='delete_news'),
    # path('articles/create/', PostCreate.as_view(), {'is_article': True}, name='create_article'),
    # path('articles/<int:pk>/edit/', PostUpdate.as_view(), name='edit_article'),
    # path('articles/<int:pk>/delete/', PostDelete.as_view(), name='delete_article'),
    path('categories/', CategoryListView.as_view(), name='category_list'),
    path('subscribe/<int:category_id>/', SubscribeView.as_view(), name='subscribe'),
]