from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters import rest_framework as filters
from .models import JobPost, Bid, DirectApplication, SavedJob
from accounts.models import User, CandidateProfile, Education, Experience, ConsultancyProfile
from accounts.serializers import CandidateProfileSerializer, EducationSerializer, ExperienceSerializer, ConsultancyProfileSerializer
from .serializers import JobPostSerializer, BidSerializer, DirectApplicationSerializer, SavedJobSerializer, UpdateBidSerializer
from .permissions import IsEmployerOrReadOnly, IsCandidateOrReadOnly, IsConsultancyOrReadOnly
from django.db import models
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework.exceptions import ValidationError

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
    permission_classes = [permissions.IsAuthenticated, IsEmployerOrReadOnly]
    
    def get_permissions(self):
        """
        Override to set different permissions based on the action
        """
        if self.action == 'apply':
            return [permissions.IsAuthenticated(), IsCandidateOrReadOnly()]
        return super().get_permissions()
    
    def perform_create(self, serializer):
        serializer.save(posted_by=self.request.user)
    
    def get_queryset(self):
        """
        Filter queryset based on user type
        """
        user = self.request.user
        if hasattr(user, 'employer_profile'):
            # Employers can see all published jobs plus their own unpublished ones
            return JobPost.objects.filter(
                models.Q(is_published=True) | 
                models.Q(posted_by=user)
            )
        # Candidates and consultancies can only see published jobs
        return JobPost.objects.filter(is_published=True)
    
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
    
    def create(self, request, *args, **kwargs):
        # Only allow consultancy profiles to create bids
        if not hasattr(request.user, 'consultancy_profile'):
            raise PermissionDenied("Only consultancies can submit bids")
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        except ValidationError as e:
            error_message = str(e)
            if "A consultancy can only submit 3 bids per job" in error_message:
                return Response(
                    {"detail": "You have reached the maximum limit of 3 bids for this job. Please review your existing bids."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            elif "You have already submitted this proposal for this job" in error_message:
                return Response(
                    {"detail": "You have already submitted this exact proposal for this job. Please modify your proposal."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            return Response(
                {"detail": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    def perform_create(self, serializer):
        serializer.save(consultancy=self.request.user.consultancy_profile)
    
    def update(self, request, *args, **kwargs):
        # Only allow employers to update bid status
        if 'status' in request.data and not hasattr(request.user, 'employer_profile'):
            raise PermissionDenied("Only employers can update bid status")
        return super().update(request, *args, **kwargs)
    
    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        bid = self.get_object()
        if not hasattr(request.user, 'employer_profile'):
            return Response(
                {"detail": "Only employers can approve bids"},
                status=status.HTTP_403_FORBIDDEN
            )
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
        if not hasattr(request.user, 'employer_profile'):
            return Response(
                {"detail": "Only employers can reject bids"},
                status=status.HTTP_403_FORBIDDEN
            )
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


class SavedJobViewSet(viewsets.ModelViewSet):
    queryset = SavedJob.objects.all()
    serializer_class = SavedJobSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'candidate_profile'):
            return SavedJob.objects.filter(candidate=user.candidate_profile)
        return SavedJob.objects.none()

    def perform_create(self, serializer):
        if not hasattr(self.request.user, 'candidate_profile'):
            raise permissions.PermissionDenied("Only candidates can save jobs")
        
        # Check if job already exists in saved jobs
        job_id = serializer.validated_data['job'].id
        if SavedJob.objects.filter(
            job_id=job_id,
            candidate=self.request.user.candidate_profile
        ).exists():
            raise serializers.ValidationError("This job is already saved")
            
        serializer.save(candidate=self.request.user.candidate_profile)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.candidate != request.user.candidate_profile:
            raise permissions.PermissionDenied("You can only unsave jobs that you have saved")
        return super().destroy(request, *args, **kwargs)

#get Candidate Profile
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def get_user_profile(request):
    request_user = request.user
    if request_user.user_type == "candidate" or request_user.user_type == "consultancy":
        return Response({"error": "You are not authorized to access this View"}, status=400)
    id = request.data.get("id")
    candidate_profile = CandidateProfile.objects.get(id=id)
    user = User.objects.get(id=candidate_profile.user.id)
    user_data = {
        "id": user.id,
        "email": user.email,
        "name": user.name,
        "phone": user.phone,
        "user_type": user.user_type
    }

    try:
        if user.user_type == 'candidate':
            profile = user.candidate_profile
            profile_serializer = CandidateProfileSerializer(profile)
            education_serializer = EducationSerializer(Education.objects.filter(user=user), many=True)
            experience_serializer = ExperienceSerializer(Experience.objects.filter(user=user), many=True)
        else:
            return Response({"error": "Invalid user type."}, status=400)

        return Response({
            "user": user_data,
            "profile": profile_serializer.data,
            "education": education_serializer.data,
            "experience": experience_serializer.data
        })

    except (CandidateProfile.DoesNotExist):
        return Response({"user": user_data, "profile": None, "message": "Profile not found."}, status=404)


#update bid
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_bid(request, pk):
    try:
        bid = Bid.objects.get(id=pk)
        # Compare the IDs directly
        if bid.consultancy.id == request.user.consultancy_profile.id:
            if 'status' in request.data:
                return Response({"detail": "You are not authorized to update this bid status or consultancy or job or id"}, status=status.HTTP_403_FORBIDDEN)
            serializer = UpdateBidSerializer(bid, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        else:
            return Response({"detail": "You are not authorized to update this bid"}, status=status.HTTP_403_FORBIDDEN)
    except Bid.DoesNotExist:
        return Response({"detail": "Bid not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

#delete bid
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_bid(request, pk):
    try:
        bid = Bid.objects.get(id=pk)
        if bid.consultancy.id == request.user.consultancy_profile.id:
            bid.delete()
            return Response({"detail": "Bid deleted successfully"}, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "You are not authorized to delete this bid"}, status=status.HTTP_403_FORBIDDEN)
    except Bid.DoesNotExist:
        return Response({"detail": "Bid not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    
    
#get consultancy profile only by employer
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_consultancy_profile(request, pk):
    if request.user.user_type != "employer":
        return Response({"detail": "You are not authorized to access this view"}, status=status.HTTP_403_FORBIDDEN)
    consultancy_profile = ConsultancyProfile.objects.get(id=pk)
    return Response(ConsultancyProfileSerializer(consultancy_profile).data)