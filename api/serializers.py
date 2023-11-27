from rest_framework import serializers
from .models import Farmer, BlogPost, ProduceListing, ChatMessage, Complaint, AdminReply, AdminProfile, FarmerReply, AgricKnowledge, OTP
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from .models import AdminProfile


User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password']
        extra_kwargs = {'password': {'write_only':True}}

    def create_user(cls, email, password, **extra_fields):
        email = cls.objects.normalize_email(email)
        user = cls(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

class FarmerSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Farmer
        fields = '__all__'
    
    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create_user(**user_data)
        farmer, created = Farmer.objects.update_or_create(user=user, **validated_data)
        return farmer

class AdminProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    
    class Meta:
        model = AdminProfile
        fields = '__all__'

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = UserSerializer.create(UserSerializer(), validated_data=user_data)
        admin_profile, created = AdminProfile.objects.update_or_create(user=user, **validated_data)
        return admin_profile
    
class OTPSerializer(serializers.ModelSerializer):
    class Meta:
        model = OTP
        fields = ['user', 'otp_code']

class BlogPostSerializer(serializers.ModelSerializer):
    author = FarmerSerializer(read_only=True)

    class Meta:
        model = BlogPost
        fields ='__all__'

    def validate_category(self, value):
        predefined_category = ['innovation', 'market_trends']

        if value not in predefined_category:
            return 'custom'
        return value
    
class AgricKnowledgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AgricKnowledge
        fields = ['title', 'content']

class ProduceListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProduceListing
        fields = '__all__'



class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = '__all__'

class ComplaintSerializer(serializers.ModelSerializer):
    class Meta:
        model = Complaint
        fields = '__all__'

class AdminReplySerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminReply
        fields = '__all__'

class FarmerReplySerializer(serializers.ModelSerializer):
    class Meta:
        model = FarmerReply
        fields = '__all__'