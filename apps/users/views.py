from django.shortcuts import render

from django.contrib import messages
from allauth.account.views import SignupView
from allauth.account.app_settings import AppSettings


# Create your views here.
class StandardSignupView(SignupView):
    def form_valid(self, form):
        # form # You can do something up here if you want
        response = super().form_valid(form)

        if (
            AppSettings.EMAIL_VERIFICATION
            == AppSettings.EmailVerificationMethod.MANDATORY
        ):
            messages.info(
                self.request,
                "We have sent you an account verification email. Please verify before continuing.",
            )
        else:
            messages.success(self.request, "Your account was successfully created!")

        return response
