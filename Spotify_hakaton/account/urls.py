from django.urls import path
from .views import RegistrationView, LoginView, ActivationView, LogoutView, ChangePasswordView, ForgotPasswordView, ForgotPasswordCompleteView
from drf_yasg.views import get_schema_view
from drf_yasg import  openapi
from rest_framework import permissions


schema_view = get_schema_view(
   openapi.Info(
      title="Алияр-Байке",
      default_version='$',
      description="ТИма На ПОМОЩЬ!!!!!!!!!!!!!!!!!!!!!!!!!!!!!1",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="ПИЩУ В МАКЕРС"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('register/', RegistrationView.as_view()),
    path('activate/', ActivationView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('change_password/', ChangePasswordView.as_view()),
    path('forgot_password/',  ForgotPasswordView.as_view()),
    path('forgot_password_complete/', ForgotPasswordCompleteView.as_view())
]