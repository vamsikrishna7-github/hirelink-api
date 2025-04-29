from django.urls import path, include
from accounts.views import EmployerProfileUpdateView, ConsultancyProfileUpdateView, CandidateProfileUpdateView, get_user_profile, send_reset_password_email, reset_password, GoogleLoginAPIView, EmailOTPSendView, VerifyEmailOTPView

urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),


    #social logins
    path('auth/google-login/', GoogleLoginAPIView.as_view(), name='google-login'),


    #profile urls
    path('employer/profile/', EmployerProfileUpdateView.as_view(), name='employer-profile-update'),
    path('consultancy/profile/', ConsultancyProfileUpdateView.as_view(), name='consultancy-profile-update'),
    path('candidate/profile/', CandidateProfileUpdateView.as_view(), name='candidate-profile-update'),
    path('get/profile/', get_user_profile, name='get-profile'),

    #password reset urls
    path('auth/request-reset-password/', send_reset_password_email),
    path('auth/reset-password/<uidb64>/<token>/', reset_password),

    #email otp urls
    path('send-otp/', EmailOTPSendView.as_view(), name='send_otp'),
    path('verify-otp/', VerifyEmailOTPView.as_view(), name='verify_otp'),
]
