from rest_framework.generics import RetrieveUpdateAPIView
from .models import EmployerProfile, ConsultancyProfile, CandidateProfile, User
from .serializers import EmployerProfileSerializer, ConsultancyProfileSerializer, CandidateProfileSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response



# Employer Profile Update View
class EmployerProfileUpdateView(RetrieveUpdateAPIView):
    queryset = EmployerProfile.objects.all()
    serializer_class = EmployerProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user.employer_profile


# Consultancy Profile Update View
class ConsultancyProfileUpdateView(RetrieveUpdateAPIView):
    queryset = ConsultancyProfile.objects.all()
    serializer_class = ConsultancyProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user.consultancy_profile


# Candidate Profile Update View
class CandidateProfileUpdateView(RetrieveUpdateAPIView):
    queryset = CandidateProfile.objects.all()
    serializer_class = CandidateProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user.candidate_profile


# Get User Data and Profile Data
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_profile(request):
    user = request.user
    user_data = {
        "id": user.id,
        "email": user.email,
        "name": user.name,
        "phone": user.phone,
        "user_type": user.user_type
    }

    try:
        if user.user_type == 'employer':
            profile = user.employer_profile
            profile_serializer = EmployerProfileSerializer(profile)
        elif user.user_type == 'consultancy':
            profile = user.consultancy_profile
            profile_serializer = ConsultancyProfileSerializer(profile)
        elif user.user_type == 'candidate':
            profile = user.candidate_profile
            profile_serializer = CandidateProfileSerializer(profile)
        else:
            return Response({"error": "Invalid user type."}, status=400)

        return Response({
            "user": user_data,
            "profile": profile_serializer.data
        })

    except (EmployerProfile.DoesNotExist, ConsultancyProfile.DoesNotExist, CandidateProfile.DoesNotExist):
        return Response({"user": user_data, "profile": None, "message": "Profile not found."}, status=404)
