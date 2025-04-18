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


# yourapp/views.py

from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from accounts.utils import send_password_reset_email

User = get_user_model()
token_generator = PasswordResetTokenGenerator()

@api_view(['POST'])
def send_reset_password_email(request):
    email = request.data.get("email")
    try:
        user = User.objects.get(email=email)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = token_generator.make_token(user)
        send_password_reset_email(user, uid, token)
        return Response({"message": "Password reset link sent!"})
    except User.DoesNotExist:
        return Response({"error": "User not found."}, status=404)

@api_view(['POST'])
def reset_password(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)

        if not token_generator.check_token(user, token):
            return Response({"error": "Invalid or expired token."}, status=400)

        password = request.data.get("password")
        if not password:
            return Response({"error": "Password is required."}, status=400)

        user.set_password(password)
        user.save()
        return Response({"message": "Password reset successful!"})

    except (User.DoesNotExist, ValueError, TypeError):
        return Response({"error": "Invalid token or user."}, status=400)
