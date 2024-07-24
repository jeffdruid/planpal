from django.shortcuts import redirect
from django.urls import reverse


class PreventBackAfterLogoutMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated:
            if not request.user.is_authenticated:
                if request.path not in [
                    reverse("account_login"),
                    reverse("account_signup"),
                ]:
                    return redirect(reverse("account_login"))
        else:
            request.session["logged_in"] = True

        response = self.get_response(request)

        if request.path == reverse("account_logout"):
            request.session.flush()

        return response
