from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BranchDetailsView, BanksView, CityBranchesView
from .views import banks_upload

urlpatterns=[
    path('upload-csv/', banks_upload, name='banks-upload' ),
    path('banks/',BanksView.as_view(), name='bank-details'),
    path('branch/<str:code>/',BranchDetailsView.as_view(), name='bank-details'),
    path('branches/',CityBranchesView.as_view(), name='branch-details'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')
    )
]