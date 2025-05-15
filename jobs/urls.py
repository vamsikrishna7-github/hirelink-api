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
]
