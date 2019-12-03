from django.contrib import admin
from django.urls import path,include
from .views import NavView,CommentsLoginView,MemberLoginView
app_name='memberauth'
urlpatterns = [
    path('login/', CommentsLoginView.as_view(), name='login'),
    path('dashboard/', NavView.as_view(), name='dashboard'),
    path('memberlogin/',MemberLoginView.as_view(),name='memlogin'),

    # path('',include('client_portal.urls')),
]
