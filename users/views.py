from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework import status
from knox.models import AuthToken
from .models import User
from .serializers import UserSerializer, RegisterSerializer, LoginSerializer, UpdateSerializer, ResetPasswordSerializer, SendCvSerializer
from rest_framework.parsers import MultiPartParser, FormParser , JSONParser
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
import smtplib
from email.message import EmailMessage
import os


USERNAME = os.environ.get("DB_USERNAME")
PASSWORD = os.environ.get("DB_SECRET_KEY")

#print(PASSWORD)

# Register API
class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    parser_classes = (MultiPartParser, FormParser)
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data["username"]
        email = serializer.validated_data["email"]
        html_content = render_to_string("users/email.html", { "username" : username })
        user = serializer.save()
        msg = EmailMessage()
        msg["subject"] = "TalentIndividuals Sign up"
        msg["from"] = "Info@talentindividuals.co.uk"
        msg["To"] = email
        msg.set_content("")
        msg.add_alternative(html_content,subtype="html")
            
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(USERNAME, PASSWORD)
            smtp.send_message(msg)
        return Response({
        "user": UserSerializer(user, context=self.get_serializer_context()).data,
        "token": AuthToken.objects.create(user)[1]
        })

# Login API
class LoginAPI(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        _, token = AuthToken.objects.create(user)
        return Response({
        "user": UserSerializer(user, context=self.get_serializer_context()).data,
        "token": token
        })

# Get User API
class UserAPI(generics.RetrieveAPIView):
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user
    
    
    
class UpdateAPI(APIView):
    serializer_class = UpdateSerializer
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    
    def put(self, request, *args, **kwargs):
        serializer = self.serializer_class(request.user,data=request.data,partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    
class ResetPasswordVIew(APIView):

    serializer_class = ResetPasswordSerializer

    def post(self, request, pk=None):
        user = get_object_or_404(User, username=request.user.username)
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid()
        oldpassword = serializer.validated_data['oldpassword']
        newpassword = serializer.validated_data['newpassword']
        if not user.check_password(oldpassword):
            return Response({'oldpassword': ['Wrong password']}, status=status.HTTP_400_BAD_REQUEST)
        
        user.set_password(newpassword)
        user.save()
        response = {
            'status': 'success',
            'code':status.HTTP_200_OK,
            'message':'Password updated successfully'
        }
        return Response(response)
    
    
class SendMailView(APIView):
    serializer_class = SendCvSerializer
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    
    def post(self,request,*args, **kwags):
        serializer = self.serializer_class(data=request.data)
        print(request.data)
        if serializer.is_valid(raise_exception=True):
            file = serializer.validated_data['file']
            
            msg = EmailMessage()
            msg["subject"] = "cv upload from talentindividual"
            msg["from"] = "Info@talentindividuals.co.uk"
            msg["To"] = "Info@talentindividuals.co.uk"
            msg.set_content("")
        
            msg.add_attachment(file.read(),maintype="application", subtype="octet-stream",filename=file.name)
            
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
                smtp.login(USERNAME, PASSWORD)
                smtp.send_message(msg)
            return Response({"status": "200 ok"})
        
        else: 
            return Response({"status": "400 BAD"})
            
            
            
            
