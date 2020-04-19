
from django.conf import settings
from django.shortcuts import render
from django.views.generic import View


class LoginView(View):

    def get(self, request):

        return render(
            request,
            'login.html',
            {'client_id': settings.GOOGLE_OAUTH2_CLIENT_ID})
