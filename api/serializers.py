from rest_framework import serializers
from .models import CustomUser


class ImageSerializer(serializers.Serializer):
    image = serializers.ImageField()


class RegisterSerializer(serializers.ModelSerializer):
    password =serializers.CharField(write_only =True)

    class Meta:
        model = CustomUser
        fields= ('email','contact','password')

    def create(self,validated_data):
        user =CustomUser.objects.create_user(email =validated_data['email'],
                                             contact =validated_data['contact'],
                                             password =validated_data['password'])
        return user
    
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password =serializers.CharField(write_only =True)