from django.urls import path, include
from .views import BranchDetailsView,AllBranchesView, CityBranchesView


urlpatterns=[
    path('branches/all/', AllBranchesView.as_view(), name='banks-upload' ),
    path('branches/<str:code>/',BranchDetailsView.as_view(), name='branch-details'),
    path('branches/',CityBranchesView.as_view(), name='city-branches-details'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')
    
    )
]