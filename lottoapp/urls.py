from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path('check_entry/<int:entry_id>/', views.check_entry, name='check_entry'),

    path('next_round/', views.next_round, name="next_round"),  # 관리자용 회차 전환

    path('admin_page/', views.admin_page, name='admin_page'),
    path('admin_page/close/', views.close_round, name='close_round'),
   
]