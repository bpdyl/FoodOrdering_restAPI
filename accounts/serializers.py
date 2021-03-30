from rest_framework import serializers
from accounts.models import NewUser

class RegisterUserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = NewUser
        fields = ('email','username','first_name','last_name','contact_no','password','is_customer','is_seller')
        extra_kwargs = {'password':{'write_only':True}}

    # def get_cleaned_data(self):
    #     return {
    #         'first_name': self.validated_data.get('first_name',''),
    #         'last_name': self.validated_data.get('last_name',''),
    #         'username': self.validated_data.get('username',''),
    #         'email':self.validated_data.get('email',''),

    #     }    
        
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewUser
        fields = ('id','username','email','first_name',
        'last_name','contact_no','profile_image')    

        read_only_fields = ('email',)