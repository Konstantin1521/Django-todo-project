from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import IntegrityError, DatabaseError
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from django.views import View
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from todo_list.models import TelegramProfile
from todo_list.serializers import CodeCheckSerializer


class TelegramProfileView(LoginRequiredMixin, View):
    template_name = 'todo_list/index.html'
    login_url = '/login/'

    def post(self, request):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('todo_list:index') + '?error=not_authenticated')

        try:
            user = request.user

            tg_profile, created = TelegramProfile.objects.get_or_create(
                user=user,
                defaults={
                    'verified_code': TelegramProfile.generate_verification_code(TelegramProfile()),
                    'verification_time': timezone.now() + timezone.timedelta(minutes=5)
                }
            )

            if not created:
                tg_profile.verified_code = TelegramProfile.generate_verification_code(tg_profile)
                tg_profile.verification_time = timezone.now() + timezone.timedelta(minutes=5)
                tg_profile.save()
            else:
                pass
            print(f"""
            User: {user.id} ({user.username})
            Telegram Profile: {tg_profile.id}
            Verification Code: {tg_profile.verified_code}
            Verification Time: {tg_profile.verification_time}
            Created: {created}
            """)

            tg_bot_url = f"https://t.me/GorTestKsBot?start={tg_profile.verified_code}"

            return HttpResponseRedirect(tg_bot_url)

        except IntegrityError as e:
            return HttpResponseRedirect(reverse('todo_list:index') + '?error=profile_creation_failed')
        except DatabaseError as e:
            return HttpResponseRedirect(reverse('todo_list:index') + '?error=database_error')
        except Exception as e:
            return HttpResponseRedirect(reverse('todo_list:index') + '?error=unexpected_error')


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
