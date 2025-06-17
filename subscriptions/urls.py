from django.urls import path
from .views import (
    SubscriptionPlanListRetrieveView,
    UserSubscriptionRetrieveUpdateView,
    UserSubscriptionCreateView
)

urlpatterns = [
    path('plans/', SubscriptionPlanListRetrieveView.as_view(), name='subscription-plan-list'),
    path('subscribe/', UserSubscriptionRetrieveUpdateView.as_view(), name='user-subscription-retrieve-update'),
    path('subscribe/create/', UserSubscriptionCreateView.as_view(), name='user-subscription-create'),
]