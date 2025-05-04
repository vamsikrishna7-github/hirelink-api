import mimetypes
from rest_framework.generics import RetrieveUpdateAPIView
from .models import EmployerProfile, ConsultancyProfile, CandidateProfile, User, EmailOTP
from .serializers import EmployerProfileSerializer, ConsultancyProfileSerializer, CandidateProfileSerializer, EmployerProfileDocumentUploadSerializer, CandidateProfileDocumentUploadSerializer, ConsultancyProfileDocumentUploadSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .utils import generate_otp, send_otp_via_email
from threading import Thread
from rest_framework import status
from rest_framework.views import APIView
from cloudinary.uploader import upload as cloudinary_upload



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




# views.py
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

class GoogleLoginAPIView(APIView):
    def post(self, request):
        access_token = request.data.get("token")

        if not access_token:
            return Response({"error": "Token is required"}, status=status.HTTP_400_BAD_REQUEST)

        # Get user info from Google
        user_info_url = "https://www.googleapis.com/oauth2/v3/userinfo"
        response = requests.get(user_info_url, headers={"Authorization": f"Bearer {access_token}"})

        if response.status_code != 200:
            return Response({"error": "Failed to fetch user info from Google"}, status=400)

        user_data = response.json()
        email = user_data.get("email")
        name = user_data.get("name")

        if not email:
            return Response({"error": "Email not found in Google response"}, status=400)


        try:
            user = User.objects.get(email=email)
            # Issue JWT
            refresh = RefreshToken.for_user(user)
            return Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "user_type": user.user_type
            })
        except User.DoesNotExist:
            user_data["error"] = "User not found"
            # print("google login user data: ",user_data);
            return Response(user_data, status=404)



#email otp send view
class EmailOTPSendView(APIView):
    def post(self, request):
        email = request.data.get('email')
        

        if User.objects.filter(email=email).exists():
            return Response({'error': 'Email already exists'}, status=400)

        otp = generate_otp()
        EmailOTP.objects.create(email=email, otp=otp)
        email_thread = Thread(
            target=send_otp_via_email, args=(email, otp)
            )
        email_thread.start()


        return Response({'message': 'OTP sent to email'}, status=200)

# views.py
class VerifyEmailOTPView(APIView):
    def post(self, request):
        email = request.data.get('email')
        otp = request.data.get('otp')

        try:
            record = EmailOTP.objects.filter(email=email).latest('created_at')
            if record.otp == otp and not record.is_expired():
                # user = User.objects.get(email=email)
                # user.is_email_verified = True
                # user.save()
                record.delete()  # Clean up
                return Response({'message': 'Email verified successfully'}, status=200)
            else:
                return Response({'error': 'Invalid or expired OTP'}, status=400)
        except EmailOTP.DoesNotExist:
            return Response({'error': 'OTP not found'}, status=404)


# Employer Profile Document Upload View
class UploadEmployerDocumentsView(APIView):
    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response({'error': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        
        if user.user_type == 'employer':
            profile, _ = EmployerProfile.objects.get_or_create(user=user)
        elif user.user_type == 'consultancy':
            profile, _ = ConsultancyProfile.objects.get_or_create(user=user)
        elif user.user_type == 'candidate':
            profile, _ = CandidateProfile.objects.get_or_create(user=user)


        
        data = {}
        if user.user_type == 'employer' or user.user_type == 'consultancy':
            for field in ['msme_or_incorporation_certificate', 'gstin_certificate', 'pan_card', 'poc_document']:
                file = request.FILES.get(field)
                content_type, _ = mimetypes.guess_type(file.name)
                if content_type in ["application/pdf", "application/msword", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"]:
                    resource_type = "raw"
                else:
                    resource_type = "image"
                print("resource_type: ",resource_type)
                if file:
                    upload_result = cloudinary_upload(file, folder=field, resource_type=resource_type)
                    data[field] = upload_result.get('secure_url')
        elif user.user_type == 'candidate':
            for field in ['resume']:
                file = request.FILES.get(field)
                content_type, _ = mimetypes.guess_type(file.name)
                if content_type in ["application/pdf", "application/msword", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"]:
                    resource_type = "raw"
                else:
                    resource_type = "image"
                if file:
                    upload_result = cloudinary_upload(file, folder=field, resource_type=resource_type)
                    data[field] = upload_result.get('secure_url')

        if user.user_type == 'employer':
            serializer = EmployerProfileDocumentUploadSerializer(profile, data=data, partial=True)
        elif user.user_type == 'consultancy':
            serializer = ConsultancyProfileDocumentUploadSerializer(profile, data=data, partial=True)
        elif user.user_type == 'candidate':
            serializer = CandidateProfileDocumentUploadSerializer(profile, data=data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

