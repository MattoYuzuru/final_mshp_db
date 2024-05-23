from django.urls import path
from post_app import views
from django.contrib.auth import views as as_views


urlpatterns = [
    path('main/', views.main_page, name='main'),
    path('main/page/<int:page_num>', views.main_page, name='paginator'),
    path('write/', views.write_page, name='write'),
    path('write/post/', views.post_to_db, name='post_to_db'),
    path("post/rate/<int:post_id>/", views.rate_post, name="rate_post"),
    path('post/<int:post_id>/', views.post_detail_page, name='post_detail'),
    path("post/<int:post_id>/comment/", views.comment, name="comment"),
    path('user/<int:user_id>/', views.user_detail_page, name='user'),
    path('signup/', views.signup, name='signup'),
    path('login/', as_views.LoginView.as_view(), name='login'),
    path('logout/', as_views.LogoutView.as_view(), name='logout'),
]
