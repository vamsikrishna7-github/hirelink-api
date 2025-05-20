from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'jobs', views.JobPostViewSet, basename='job')
router.register(r'bids', views.BidViewSet, basename='bid')
router.register(r'applications', views.DirectApplicationViewSet, basename='application')
router.register(r'saved-jobs', views.SavedJobViewSet, basename='saved-job')

urlpatterns = [
    path('', include(router.urls)),
    path('candidateprofile/', views.get_user_profile, name='candidateprofile'),
    path('update-bid/<int:pk>/', views.update_bid, name='update-bid'),
    path('delete-bid/<int:pk>/', views.delete_bid, name='delete-bid'),
    path('consultancy-profile/<int:pk>/', views.get_consultancy_profile, name='consultancy-profile'),
]
