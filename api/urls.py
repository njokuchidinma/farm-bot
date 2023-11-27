from django.urls import path
from .views import UserSignupView, FarmerListView, FarmerDetailView, FarmerProfileView, AdminProfileView, BlogPostListCreateView, BlogPostRetrieveUpdateDestroyView,ProduceListingsView, FarmerProduceListingsView, ChatBotViewSet, ComplaintListCreateView, AdminReplyCreateView, FarmerReplyCreateView, AdminRepliesListView, FarmerRepliesListView, WeatherForecast, PestAlertView, FarmerSignupView, AgriculturalKnowledgeView, AdminSignupView, ForgetPassword, ResetPasswordView, FarmerLoginView


# google api key = AIzaSyDRqWnUcK9wSjTsrqxUIvHGKNe_bzRo8SI

urlpatterns = [
    path('user/signup/', UserSignupView.as_view(), name='user-signup'),
    path('signup/farmer/', FarmerSignupView.as_view(), name='farmer-signup'),
    path('login/', FarmerLoginView.as_view(), name='farmer-login'),
    path('farmers/', FarmerListView.as_view(), name='farmer-list'),
    path('farmers/<int:pk>/', FarmerDetailView.as_view(), name='farmer-detail'),
    path('profile/', FarmerProfileView.as_view(), name='farmer-profile'),
    path('admin/profile/', AdminProfileView.as_view(), name='admin-profile'),
    path('admin-signup/', AdminSignupView.as_view(), name='admin-signup'),
    path('forget-password/', ForgetPassword.as_view(), name='forget-password'),
    path('reset-password/', ResetPasswordView.as_view(), name='reset-password'),
    path('blogposts/', BlogPostListCreateView.as_view(), name='blog-post-list-create'),
    path('blog-posts/<int:pk>/', BlogPostRetrieveUpdateDestroyView.as_view(), name='blog-post-detail'),
    path('produce-listings/', ProduceListingsView.as_view(), name='produce-listings'),
    path('farmer-produce-listings/<int:farmer_id>/', FarmerProduceListingsView.as_view(), name='farmer-produce-listings'),
    path('farmbot/', ChatBotViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('farmbot/<uuid:pk>/', ChatBotViewSet.as_view({'get': 'retrieve'})),
    path('complaints/', ComplaintListCreateView.as_view(), name='complaint-list-create'),
    path('admin-reply/', AdminReplyCreateView.as_view(), name='admin-reply-create'),
    path('farmer-reply/', FarmerReplyCreateView.as_view(), name='farmer-reply-create'),
    path('complaints/<int:complaint_id>/admin-replies/', AdminRepliesListView.as_view(), name='complaint-admin-replies-list'),
    path('complaints/<int:complaint_id>/farmer-replies/', FarmerRepliesListView.as_view(), name='complaint-farmer-replies-list'),
    path('weather/<str:city>/', WeatherForecast.as_view(), name='weather_forecast_api'),
    path('pest-alert/<str:city>/<str:produces>/', PestAlertView.as_view(), name='pest-alert'),
    path('agricultural-knowledge/', AgriculturalKnowledgeView.as_view(), name='agricultural-knowledge'),
]