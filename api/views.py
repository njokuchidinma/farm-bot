import uuid
import random
import openai
from django.http import JsonResponse
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password, check_password
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from notifications.signals import notify
from rest_framework import viewsets, generics, permissions, status
from rest_framework.views import APIView, View
from rest_framework.response import Response
from rest_framework.generics import RetrieveAPIView
from .serializers import UserSerializer, FarmerSerializer, BlogPostSerializer, ProduceListingSerializer, ChatMessageSerializer, ComplaintSerializer, AdminReplySerializer, FarmerReplySerializer, AdminProfileSerializer, OTPSerializer
from .models import User, Farmer, BlogPost, ProduceListing, ChatMessage, Complaint, AdminReply, FarmerReply, AgricKnowledge, AdminProfile, OTP
from .weather import get_weather
from .pest_alerts import current_weather, check_pest_alert
from django_filters.rest_framework import filters, DjangoFilterBackend
from django.core.management import call_command
# from openai import ChatGPT

openai_key = "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"
# ChatGPT instance
# chatgpt = ChatGPT(auth_token='API_KEY')

class UserSignupView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class FarmerSignupView(APIView):
    def post(self, request, *args, **kwargs):
        farmer_serializer = FarmerSerializer(data=request.data)

        if farmer_serializer.is_valid():
            farmer_serializer.save()
            return Response(farmer_serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(farmer_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FarmerListView(APIView):
    def get(self, request, *args, **kwargs):
        farmers = Farmer.objects.all()
        serializer = FarmerSerializer(farmers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class FarmerDetailView(RetrieveAPIView):
    queryset = Farmer.objects.all()
    serializer_class = FarmerSerializer
    lookup_field = 'pk'


class FarmerViewSet(viewsets.ModelViewSet):
    queryset = Farmer.objects.all()
    serializer_class = FarmerSerializer

class AdminSignupView(APIView):
    def post(self, request, *args, **kwargs):
        admin_serializer = AdminProfileSerializer(data=request.data)

        if admin_serializer.is_valid():
            admin_serializer.save()
            return Response(admin_serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(admin_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class ForgetPassword(APIView):
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        try:
            farmer = Farmer.objects.get(email=email)
        except Farmer.DoesNotExist:
            return Response({'error': 'Farmer not found'}, status=status.HTTP_404_NOT_FOUND)
        # creates otp
        otp = get_random_string(6, '1234567890')

        # saves otp to db
        otp_data = {'farmer': farmer, 'otp': make_password(otp)}
        otp_serializer = OTPSerializer(data=otp_data)
        if otp_serializer.is_valid():
            otp_serializer.save()
        else:
            return Response({'error': 'Failed to generate OTP'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        # send otp to user via mail
        send_mail(
            'Your One-Time Password for Password Reset',
            f'Your OTP is: {otp}',
            {email},
            fail_silently=False
        )

        return Response({'message': 'OTP sent successfully'}, status=status.HTTP_200_OK)
    
class ResetPasswordView(APIView):
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        otp = request.data.get('otp')
        new_password = request.data.get('new_password')

        try:
            farmer = Farmer.objects.get(email=email)
        except Farmer.DoesNotExist:
            return Response({'error': 'Farmer not found'}, status=status.HTTP_404_NOT_FOUND)

        # Retrieve OTP from database
        try:
            otp_instance = OTP.objects.get(farmer=farmer)
        except OTP.DoesNotExist:
            return Response({'error': 'OTP not found'}, status=status.HTTP_404_NOT_FOUND)

        # if the provided OTP matches the stored OTP
        if not check_password(otp, otp_instance.otp_code):
            return Response({'error': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)

        # Update user password
        farmer.user.set_password(new_password)
        farmer.user.save()

        # Delete OTP record
        otp_instance.delete()

        return Response({'message': 'Password reset successful'}, status=status.HTTP_200_OK)

class FarmerLoginView(APIView):
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            return Response({'message': 'Login Successful'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        
class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        logout(request)
        return Response({'message': 'You have been successfully logged out'}, status=status.HTTP_200_OK)

class BlogPostListCreateView(generics.ListCreateAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer

class BlogPostRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer

class FarmerProfileView(generics.RetrieveUpdateAPIView):
    queryset = Farmer.objects.all()
    serializer_class = FarmerSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
         # Ensure that the authenticated user has a related Farmer profile
        obj, created = Farmer.objects.get_or_create(user=self.request.user)
        return obj


class ProduceListingsView(APIView):
    def get(self, request):
        produce_listings = ProduceListing.objects.all()
        serializer = ProduceListingSerializer(produce_listings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class FarmerProduceListingsView(APIView):
    def get(self, request, farmer_id):
        produce_listings = ProduceListing.objects.filter(farmer__id=farmer_id)
        serializer = ProduceListingSerializer(produce_listings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ChatBotViewSet(viewsets.ModelViewSet):
    queryset = ChatMessage.objects.all()
    serializer_class = ChatMessageSerializer

    def create(self, request):
        sender = request.user.username
        message = request.data.get('message')
        conversation_id = request.data.get('conversation_id', uuid.uuid4())

        # Check if the message is related to agriculture
        is_agricultural_query = is_agricultural_question(message)

        if is_agricultural_query:
            # Send agricultural query to ChatGPT
            response = openai.Completion.create(
                engine="text-davinci-002",  # Use the appropriate engine
                prompt=message,
                max_tokens=150  # Adjust as needed
            )
            bot_response = response['choices'][0]['text']
        else:
            # Respond with a generic message for unrelated queries
            bot_response = "Sorry, I can't respond to this in this moment."

        # Store messages in the database
        chat_message = ChatMessage.objects.create(sender=sender, message=message, conversation_id=conversation_id)
        response_message = ChatMessage.objects.create(sender='ChatBot', message=bot_response, conversation_id=conversation_id)

        # Return the bot's response
        return Response({'bot_response': bot_response})


def is_agricultural_question(message):
    # Implement your logic to determine if the message is an agricultural question
    # You might use keywords, patterns, or a machine learning model for this check
    # For simplicity, let's assume any message containing "agriculture" is relevant
    return "agriculture" in message.lower()
        
    
        
class ComplaintListCreateView(generics.ListCreateAPIView):
    queryset = Complaint.objects.all()
    serializer_class = ComplaintSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        complaint = serializer.save(farmer=self.request.user)
        notify.send(
            complaint.admin,  # Send notification to the admin
            verb='New complaint',
            description=f'New complaint from {complaint.farmer.name}',
            target=complaint
        )


class AdminReplyCreateView(generics.CreateAPIView):
    queryset = AdminReply.objects.all()
    serializer_class = AdminReplySerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        reply = serializer.save(admin=self.request.user)
        notify.send(
            reply.complaint.farmer,  # Send notification to the farmer
            verb='Complaint replied',
            description=f'Your complaint has been replied by {reply.admin.name}',
            target=reply.complaint
        )

class FarmerReplyCreateView(generics.CreateAPIView):
    queryset = ProduceListing.objects.all()
    serializer_class = ProduceListingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(farmer=self.request.user)

@receiver(post_save, sender=Complaint)
def complaint_post_save(sender, instance, **kwargs):
    notify.send(
        instance.farmer,  # Send notification to the farmer when a complaint is created
        verb='New complaint',
        description='Your complaint has been submitted successfully',
        target=instance
    )


@receiver(post_save, sender=AdminReply)
def admin_reply_post_save(sender, instance, **kwargs):
    notify.send(
        instance.complaint.farmer,  # Send notification to the farmer when a reply is added
        verb='Complaint replied',
        description=f'Your complaint has been replied by {instance.admin.name}',
        target=instance.complaint
    )

class AdminRepliesListView(generics.ListAPIView):
    serializer_class = AdminReplySerializer

    def get_queryset(self):
        Complaint_id = self.kwargs['complaint_id']
        return AdminReply.objects,filter(Complaint__id=Complaint_id)

class FarmerRepliesListView(generics.ListAPIView):
    serializer_class = FarmerReplySerializer

    def get_queryset(self):
        complaint_id = self.kwargs['complaint_id']
        return FarmerReply.objects.filter(complaint__id=complaint_id)
    
class WeatherForecast(View):
    def get(self, request, city):
        api_key = "api_key"
        weather_data = get_weather(api_key, city)

        temperature = weather_data.get("current", {}).get("temperature", "N/A")
        return Response({"temperature": temperature}, status=status.HTTP_200_OK)
    
class PestAlertView(View):
    def get(self, request, *args, **kwargs):
        city = request.GET.get('city')
        produces = request.GET.get('produces')
        produces_list = produces.split(',')
        current_temp = current_weather(city)

        pest_alerts = check_pest_alert(produces_list, current_temp)

        return JsonResponse({'alerts': pest_alerts})
    
class AgriculturalKnowledgeView(View):
    def get(self, request, *args, **kwargs):
        random_facts = self.get_random_agricultural_facts(5)
        return JsonResponse({'random_facts': random_facts})

    def get_random_agricultural_facts(self, num_facts):
        total_facts = AgricKnowledge.objects.count()

        if total_facts == 0:
            call_command('fetch_facts')

        random_fact_ids = random.sample(range(1, total_facts + 1), min(num_facts, total_facts))
        random_facts = AgricKnowledge.objects.filter(pk__in=random_fact_ids)

        formatted_facts = [{'title': fact.title, 'content': fact.content} for fact in random_facts]

        return formatted_facts
    
class AdminProfileView(APIView):
    def get(self, request, *args, **kwargs):
        admin_profile = AdminProfile.objects.get(user=request.user)
        serializer = AdminProfileSerializer(admin_profile)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        admin_profile_serializer = AdminProfileSerializer(data=request.data)

        if admin_profile_serializer.is_valid():
            admin_profile_serializer.validated_data['user'] = request.user

            admin_profile, created = AdminProfile.objects.update_or_create(
                user=request.user,
                defaults=admin_profile_serializer.validated_data
            )

            return Response(AdminProfileSerializer(admin_profile).data, status=status.HTTP_201_CREATED)

        return Response(admin_profile_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
