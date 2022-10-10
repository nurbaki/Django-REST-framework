from rest_framework import serializers
from .models import Student, Path
        

# 1. Yöntem

# class StudentSerializer(serializers.Serializer):
#     first_name = serializers.CharField(max_length=30)
#     last_name = serializers.CharField(max_length=30)
#     number = serializers.IntegerField(required=False)

#     def create(self, validated_data):
#         return Student.objects.create(**validated_data)

#     def update(self, instance, validated_data):
#         instance.first_name = validated_data.get('first_name', instance.first_name) 
#         instance.last_name = validated_data.get('last_name', instance.last_name) 
#         instance.number = validated_data.get('number', instance.number)
#         instance.save()
#         return instance


# 2. Yöntem

class StudentSerializer(serializers.ModelSerializer):
    
    full_name = serializers.SerializerMethodField() # Özel data çağırma
    def get_full_name(self, obj):
        return f'{obj.first_name} {obj.last_name}'

    # fullname = serializers.SerializerMethodField(method_name='full_name')
    # def full_name(self, obj):
    #   return f'{obj.first_name} {obj.last_name}'
    
    # İlişkili tablodan veri al:
    path = serializers.StringRelatedField()

    id = serializers.IntegerField(required=False) # Veri işlemlerinde gönderimi mecburi olmasını istemiyorum.
    path_id = serializers.IntegerField() # Modelden otomatik gelmiyor. Kayıt işlemleri için gerekli

    class Meta: 
        model = Student
        fields = ["id", "first_name", "last_name", "number", "path_id", "full_name", "path"]
        # fields = '__all__'
        # exclude = ['number']

class PathSerializer(serializers.ModelSerializer):
    # students = serializers.PrimaryKeyRelatedField(read_only=True, many=True) # Sadece ID'leri getir
    students = StudentSerializer(many=True, required=False) # Öğrenci verilerini getir

    class Meta: 
        model = Path 
        fields = ["id", "path_name", "students"]