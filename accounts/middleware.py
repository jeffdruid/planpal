from django.shortcuts import redirect
from django.urls import reverse


class PreventBackAfterLogoutMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        open_paths = [
            reverse("account_login"),
            reverse("account_signup"),
            reverse("account_reset_password"),
        ]

        if not request.user.is_authenticated:
            if request.path not in open_paths:
                return redirect(reverse("account_login"))
        else:
            request.session["logged_in"] = True

        response = self.get_response(request)

        if request.path == reverse("account_logout"):
            request.session.flush()

        return response
