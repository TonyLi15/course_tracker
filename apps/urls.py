from django.urls import path
from . import views

urlpatterns = [
    path('', views.welcome, name='welcome'),
    path('register',views.AccountRegistration.as_view(), name='register'),
    path('login',views.Login,name='Login'),
    path("logout",views.Logout,name="Logout"),
    path("index",views.index,name="index"),
    path("create",views.create_course,name='create_course'),
    path("<slug:slug>/", views.course_detail, name='course_detail'),
    path("add_favorite/<slug:slug>/", views.add_favorite, name="add_favorite"),
    path("remove_favorite/<slug:slug>/", views.remove_favorite, name="remove_favorite"),
    path("search",views.search,name="search"),
    path("mypage",views.mypage,name="mypage"),
    path('edit/course/<slug:slug>/', views.edit_course, name='edit_course'),
    path('edit/comment/<int:comment_id>/', views.edit_comment, name='edit_comment'),
]