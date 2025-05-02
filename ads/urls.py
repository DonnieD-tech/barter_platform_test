from django.urls import path
from . import views

urlpatterns = [
    path('', views.ad_list, name='ad_list'),

    path('ads/create/', views.ad_create, name='ad_create'),
    path('ads/<int:pk>/edit/', views.ad_edit, name='ad_edit'),
    path('ads/<int:pk>/delete/', views.ad_delete, name='ad_delete'),

    path('exchange/create/', views.create_exchange_proposal, name='exchange_create'),
    path('exchange/list/', views.proposal_list, name='proposal_list'),
    path('exchange/<int:pk>/accept/', views.accept_exchange, name='accept_exchange'),
    path('exchange/<int:pk>/decline/', views.decline_exchange, name='decline_exchange'),
]