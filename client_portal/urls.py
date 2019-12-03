from django.contrib import admin
from django.urls import path
from .views import LoginView,DashboardView,RegisterView
from .views import ProjectList,ProjectCreation
from .views import MemberList,MemberUpdate,MemberDetail,MemberDelete,MemberCreation
from .views import ProjectDetail,ProjectUpdate,ProjectDelete
from .views import MemberCreate



app_name='client_portal'
urlpatterns = [
    path('login/', LoginView.as_view(), name='login-view'),
    path('dashboard/', DashboardView.as_view(), name='dashboard-view'),
    path('register/', RegisterView.as_view(), name='register-view'),
    path('list/',ProjectList.as_view(),name='list'),
    path('create/',ProjectCreation.as_view(),name="index" ),
    path('detail/<int:pk>',ProjectDetail.as_view(),name="detail" ),
    path('project/member/',MemberCreate,name="member-create" ),
    path('update/<int:pk>/',ProjectUpdate.as_view(),name="update" ),
    path('delete/<int:pk>/',ProjectDelete.as_view(),name="delete" ),

    path('memlist/',MemberList.as_view(),name='memlist'),
    path('memdetail/<int:pk>',MemberDetail.as_view(),name='memdetail'),
    path('memupdate/<int:pk>',MemberUpdate.as_view(),name='memupdate'),
    path('memdelete/<int:pk>',MemberDelete.as_view(),name='memdelete'),
    path('memcreate/',MemberCreation.as_view(),name='memindex'),
    # path('membercreateview/',MemberCreateView.as_view(),name='membercreate'),
]
