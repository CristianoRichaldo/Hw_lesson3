from rest_framework import serializers
from django.utils import timezone
from .models import Task

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            'id',
            'title',
            'description',
            'status',
            'priority',
            'due_date',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id','created_at','updated_at']
        def validate_title(self,value):
            value = value.strip()

            if len(value) < 5:
                raise serializers.ValidationError(
                'Название должно содержать минимум 5 символов.'
            )

            if value.isdigit():
                raise serializers.ValidationError(
                'Название не должно состоять только из цифр.'
            )

            return value

    def validate_priority(self, value):
        if not 1 <= value <= 5:
            raise serializers.ValidationError(
                'Приоритет должен быть от 1 до 5.'
            )
        return value

    def validate(self, data):
        due_date = data.get('due_date')

        if due_date is not None and due_date < timezone.now():
            raise serializers.ValidationError({
                'due_date': 'Дедлайн не может быть в прошлом.'
            })
        return data
            
