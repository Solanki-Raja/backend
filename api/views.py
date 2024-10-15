from django.shortcuts import render
from .models import CustomUser
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import generics,status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .serializers import RegisterSerializer,LoginSerializer
from django.contrib.auth import authenticate

from .serializers import ImageSerializer
from tensorflow.keras.models import load_model
import numpy as np
import cv2
import os
import json

from .location_utils import get_location_coordinates  # Import the new utility



#this is for after accessing jwt token in postman
class HomeView(APIView):
   permission_classes = [IsAuthenticated]
   
   def get(self,request):
      return Response({"Product Home:The app is up and running."})


class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class =RegisterSerializer

class LoginView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = LoginSerializer

    def post(self,request,*args,**kwargs):
        serializer = self.get_serializer(data = request.data)
        serializer.is_valid(raise_exception =True)
        user =authenticate(email =serializer.validated_data['email'],
                           password =serializer.validated_data['password'])
            
        if user:
         refresh =RefreshToken.for_user(user)
         return Response({'refresh':str(refresh),
                       'access':str(refresh.access_token),},
                       status= status.HTTP_200_OK)
        return Response({
           'error': 'Invalid Credentials'
                        },
                        status=status.HTTP_401_UNAUTHORIZED)
        

# class ImagePredictor(APIView):
#     model = load_model('location_identifier_model.keras')
#     label_mapping = {  # Update with your actual label mapping
#         'eiffel_tower': 0,
#         'grand_canyon': 1,
#         # Add other mappings here 1234
#     }

#     def post(self, request):
#         serializer = ImageSerializer(data=request.data)
#         if serializer.is_valid():
#             file = request.FILES['image']
#             img = cv2.imdecode(np.frombuffer(file.read(), np.uint8), cv2.IMREAD_COLOR)
#             img = cv2.resize(img, (224, 224)) / 255.0
#             img = np.expand_dims(img, axis=0)  # Add batch dimension
#             prediction = self.model.predict(img)
#             location_index = np.argmax(prediction)
#             location = list(self.label_mapping.keys())[location_index]  # Get the location label
#             return Response({'location': location}, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# -----------------------------------------------------------------------------------Google API KEY-------------------------------------







class ImagePredictor(APIView):
    model = load_model('location_identifier_model.keras')
    label_mapping = {  # Update with your actual label mapping
        'eiffel_tower': 0,
        'grand_canyon': 1,
        # Add other mappings here
    }

    def post(self, request):
        serializer = ImageSerializer(data=request.data)
        if serializer.is_valid():
            file = request.FILES['image']
            img = cv2.imdecode(np.frombuffer(file.read(), np.uint8), cv2.IMREAD_COLOR)
            img = cv2.resize(img, (224, 224)) / 255.0
            img = np.expand_dims(img, axis=0)  # Add batch dimension
            prediction = self.model.predict(img)
            location_index = np.argmax(prediction)
            location = list(self.label_mapping.keys())[location_index]  # Get the location label

            # Get the latitude and longitude of the predicted location
            lat, lng = get_location_coordinates(location)
            if lat and lng:
                return Response({
                    'location': location,
                    'latitude': lat,
                    'longitude': lng
                }, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Geocoding failed'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
