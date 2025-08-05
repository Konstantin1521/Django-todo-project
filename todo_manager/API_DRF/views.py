from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import CodeCheckSerializer

class TelegramProfileChekCodeView(APIView):
    def post(self, request):
        serializer = CodeCheckSerializer(data=request.data)

        if serializer.is_valid():
            profile = serializer.validated_data['profile']
            telegram_id = serializer.validated_data['tg_id']
            profile.tg_id = telegram_id
            profile.verified = True
            profile.save()

            return Response({"status": "ok"}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
