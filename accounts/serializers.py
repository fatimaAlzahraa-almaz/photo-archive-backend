from rest_framework.serializers import ModelSerializer,serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
User=get_user_model()

class RegisterSerializer(ModelSerializer):
    password_confirm=serializers.CharField(write_only=True,required=True)
    class Meta:
        model=User
        fields=['name','email','password','password_confirm']
        extra_kwargs={
          'password':{'write_only':True}
        }
    def validate_password(self,password):
        validate_password(password)
        return password
    def validate(self,attrs):
        if attrs['password']!=attrs['password_confirm']:
            raise serializers.ValidationError({"password":"Password fields didn't match."})
        return attrs
    def create(self,validated_data):
        validated_data.pop('password_confirm')
        user=User.objetcs.create_user(**validated_data)
        return user
      
class UserSerializer(ModelSerializer):
    class Meta:
        model=User
        fields=['name','email']
        extra_kwargs={
          'email':{'read_only':True}
        }
    