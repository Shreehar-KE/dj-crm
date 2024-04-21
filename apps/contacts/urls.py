from django.urls import path

from . import views

app_name = 'contacts'
urlpatterns = [
    path('', views.TestView.as_view(), name='test'),
    path('lead-create/', views.LeadCreateView.as_view(), name='lead-create'),
    path('leads/', views.LeadListView.as_view(), name='lead-list'),
    path('lead/<int:pk>/detail/', views.LeadDetailView.as_view(), name='lead-detail'),
    path('lead/<int:pk>/update/', views.LeadUpdateView.as_view(), name='lead-update'),
    path('lead/<int:pk>/promote/', views.lead_promote_view, name='lead-promote'),
    path('prospect-create/', views.ProspectCreateView.as_view(),
         name='prospect-create'),
    path('prospects/', views.ProspectListView.as_view(), name='prospect-list'),
    path('prospect/<int:pk>/detail/',
         views.ProspectDetailView.as_view(), name='prospect-detail'),
    path('prospect/<int:pk>/update/',
         views.ProspectUpdateView.as_view(), name='prospect-update'),
    path('prospect/<int:pk>/promote/',
         views.prospect_promote_view, name='prospect-promote'),
    path('customer-create/', views.CustomerCreateView.as_view(),
         name='customer-create'),
    path('customers/', views.CustomerListView.as_view(), name='customer-list'),
    path('customer/<int:pk>/detail/',
         views.CustomerDetailView.as_view(), name='customer-detail'),
    path('customer/<int:pk>/update/',
         views.CustomerUpdateView.as_view(), name='customer-update'),
]
