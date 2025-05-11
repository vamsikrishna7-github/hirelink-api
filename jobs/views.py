from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters import rest_framework as filters
from .models import JobPost, Bid, DirectApplication
from .serializers import JobPostSerializer, BidSerializer, DirectApplicationSerializer

class JobPostFilter(filters.FilterSet):
    min_salary = filters.NumberFilter(field_name="min_salary", lookup_expr='gte')
    max_salary = filters.NumberFilter(field_name="max_salary", lookup_expr='lte')
    
    class Meta:
        model = JobPost
        fields = {
            'job_type': ['exact'],
            'experience_level': ['exact'],
            'work_mode': ['exact'],
            'location': ['icontains'],
            'industry': ['icontains'],
            'skills_required': ['icontains'],
        }

class JobPostViewSet(viewsets.ModelViewSet):
    queryset = JobPost.objects.filter(is_published=True)
    serializer_class = JobPostSerializer
    filterset_class = JobPostFilter
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def perform_create(self, serializer):
        serializer.save(posted_by=self.request.user)
    
    @action(detail=True, methods=['post'])
    def apply(self, request, pk=None):
        job = self.get_object()
        serializer = DirectApplicationSerializer(data={
            'job': job.id,
            'candidate': request.user.candidate_profile.id,
            'cover_letter': request.data.get('cover_letter', '')
        })
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BidViewSet(viewsets.ModelViewSet):
    queryset = Bid.objects.all()
    serializer_class = BidSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'employer_profile'):
            return Bid.objects.filter(job__posted_by=user)
        elif hasattr(user, 'consultancy_profile'):
            return Bid.objects.filter(consultancy=user.consultancy_profile)
        return Bid.objects.none()
    
    def perform_create(self, serializer):
        serializer.save(consultancy=self.request.user.consultancy_profile)
    
    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        bid = self.get_object()
        if request.user != bid.job.posted_by:
            return Response(
                {"detail": "Only the job poster can approve bids"},
                status=status.HTTP_403_FORBIDDEN
            )
        bid.status = 'approved'
        bid.save()
        return Response(BidSerializer(bid).data)
    
    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        bid = self.get_object()
        if request.user != bid.job.posted_by:
            return Response(
                {"detail": "Only the job poster can reject bids"},
                status=status.HTTP_403_FORBIDDEN
            )
        bid.status = 'rejected'
        bid.save()
        return Response(BidSerializer(bid).data)

class DirectApplicationViewSet(viewsets.ModelViewSet):
    queryset = DirectApplication.objects.all()
    serializer_class = DirectApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'employer_profile'):
            return DirectApplication.objects.filter(job__posted_by=user)
        elif hasattr(user, 'candidate_profile'):
            return DirectApplication.objects.filter(candidate=user.candidate_profile)
        return DirectApplication.objects.none()
    
    def perform_create(self, serializer):
        serializer.save(candidate=self.request.user.candidate_profile)
    
    @action(detail=True, methods=['post'])
    def update_status(self, request, pk=None):
        application = self.get_object()
        if request.user != application.job.posted_by:
            return Response(
                {"detail": "Only the job poster can update application status"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        new_status = request.data.get('status')
        if new_status not in dict(DirectApplication.STATUS_CHOICES):
            return Response(
                {"detail": "Invalid status"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        application.status = new_status
        application.save()
        return Response(DirectApplicationSerializer(application).data)
