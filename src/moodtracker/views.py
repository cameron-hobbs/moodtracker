from django.shortcuts import render
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from tracker.provider.sms_provider import SMSProvider


def index(request):
    return render(request, "index.html")


class SmsWebhook(APIView):
    authentication_classes = []
    permission_classes = []

    @extend_schema(exclude=True)
    def post(self, request):
        if SMSProvider().webhook_callback(request):
            return Response(status=status.HTTP_200_OK)

        return Response(status=status.HTTP_404_NOT_FOUND)
