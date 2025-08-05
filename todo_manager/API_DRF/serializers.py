from rest_framework import serializers

class CodeCheckSerializer(serializers.Serializer):
    verified_code = serializers.CharField(max_length=5)
    tg_id = serializers.IntegerField()

    def validate(self, data):
        from todo_list.models import TelegramProfile
        from django.utils import timezone

        code = data['verified_code']

        try:
            profile = TelegramProfile.objects.get(verified_code=code)
        except TelegramProfile.DoesNotExist:
            raise serializers.ValidationError('Code not found')

        if profile.verified:
            raise serializers.ValidationError('Code already verified')

        if timezone.now() > profile.verification_time:
            raise serializers.ValidationError('Code expired')

        data['profile'] = profile

        return data

