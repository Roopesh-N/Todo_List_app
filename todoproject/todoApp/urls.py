from django.urls import path
from . import views
urlpatterns = [
    path('homepageview/<slug:slug>/', views.homepage_view,name='homepage'),
    path('',views.login_view,name='login'),
    path('signup/',views.signup_view,name='signup'),
    path('addtask/<slug:slug>/',views.addtask_view,name='addtask'),
    path('updatetask/<slug:slug>/<str:title>',views.updatetask_view,name='updatetask'),
    path('removetask/<slug:slug>/<str:title>',views.remove_view,name='remove'),
]
