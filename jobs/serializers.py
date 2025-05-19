from rest_framework import serializers
from .models import JobPost, Bid, DirectApplication, SavedJob
from accounts.serializers import UserSerializer

class JobPostSerializer(serializers.ModelSerializer):
    posted_by = UserSerializer(read_only=True)
    
    class Meta:
        model = JobPost
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')
        


class UpdateBidSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bid
        fields = ['proposal', 'fee', 'id', 'job', 'consultancy']
        read_only_fields = ('id', 'job', 'consultancy')

class BidSerializer(serializers.ModelSerializer):
    consultancy_name = serializers.CharField(source='consultancy.company_name', read_only=True)
    
    class Meta:
        model = Bid
        fields = ['id', 'job', 'consultancy', 'consultancy_name', 'proposal', 'fee', 'status', 'created_at', 'updated_at']
        read_only_fields = ('created_at', 'updated_at', 'status', 'consultancy')
    
    def create(self, validated_data):
        # Get the consultancy profile from the authenticated user
        request = self.context.get('request')
        if request and hasattr(request.user, 'consultancy_profile'):
            validated_data['consultancy'] = request.user.consultancy_profile
        return super().create(validated_data)

class DirectApplicationSerializer(serializers.ModelSerializer):
    candidate_name = serializers.CharField(source='candidate.get_full_name', read_only=True)
    
    class Meta:
        model = DirectApplication
        fields = '__all__'
        read_only_fields = ('applied_at', 'updated_at', 'status')


class SavedJobSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavedJob
        fields = ['id', 'job', 'candidate', 'created_at']
        read_only_fields = ('created_at', 'candidate')
