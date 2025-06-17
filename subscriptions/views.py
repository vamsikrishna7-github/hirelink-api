from rest_framework import generics, status
from rest_framework.response import Response
from .models import SubscriptionPlan, UserSubscription
from .serializers import SubscriptionPlanSerializer, UserSubscriptionSerializer
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404


class SubscriptionPlanListRetrieveView(generics.ListAPIView):
    queryset = SubscriptionPlan.objects.all()
    serializer_class = SubscriptionPlanSerializer


class UserSubscriptionRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSubscriptionSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        try:
            return UserSubscription.objects.filter(user=self.request.user, active=True).first()
        except UserSubscription.DoesNotExist:
            return None

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        if not instance:
            return Response({
                "message": "No active subscription found",
                "has_subscription": False
            }, status=status.HTTP_200_OK)
        serializer = self.get_serializer(instance)
        return Response({
            **serializer.data,
            "has_subscription": True
        })

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        if not instance:
            return Response({
                "message": "No active subscription found",
                "has_subscription": False
            }, status=status.HTTP_404_NOT_FOUND)
        return super().put(request, *args, **kwargs)


class UserSubscriptionCreateView(generics.CreateAPIView):
    serializer_class = UserSubscriptionSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        plan_id = request.data.get('plan')
        if not plan_id:
            return Response(
                {'error': 'Plan ID is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            plan = SubscriptionPlan.objects.get(id=plan_id)
        except SubscriptionPlan.DoesNotExist:
            return Response(
                {'error': 'Invalid plan ID'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Check if user already has an active subscription
        if UserSubscription.objects.filter(user=request.user, active=True).exists():
            return Response(
                {'error': 'User already has an active subscription'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Create new subscription
        subscription = UserSubscription.objects.create(
            user=request.user,
            plan=plan,
            active=True
        )

        serializer = self.get_serializer(subscription)
        return Response(serializer.data, status=status.HTTP_201_CREATED)