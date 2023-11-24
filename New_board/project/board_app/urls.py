from django.urls import path
from .views import *
from django.views.decorators.cache import cache_page

urlpatterns = [
    path('', ListPost.as_view(), name='home'),
    path('<int:pk>/', DetailPost.as_view(), name='detail_post'),
    path('create/', CreatePost.as_view(), name='create_posts'),
    path('<int:pk>/edit/', UpdatePost.as_view(), name='update_post_news'),
    path('<int:pk>/delete/', DeletePost.as_view(), name='delete_post_news'),
    path('search/', cache_page(60*1)(ListPostFilter.as_view()), name='list_post_filter'),
    path('done/', DoneView.as_view(), name='done_view'),
    path('update/', upgrade_me, name='update_user_category'),
    path('logout/', logout_view, name='logout'),
    path('<int:pk>/subscribe/', subscribe, name='subscribe'),
    path('response/', user_responses, name='user_responses'),
    path('change_response_status/<int:subscription_id>/<str:new_status>/', change_response_status, name='change_response_status'),
    path('categories/subscribe_done', DoneSubscribeView.as_view(), name='done_subscribe'),
    path('profile/', UserProfileView.as_view(), name='user_profile'),
]
