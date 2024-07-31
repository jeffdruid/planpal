from django.shortcuts import redirect
from django.urls import reverse


class PreventBackAfterLogoutMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        open_paths = [
            reverse("home"),
            reverse("account_login"),
            reverse("account_signup"),
            reverse("send_one_time_login_link_form"),
            reverse(
                "send_one_time_login_link",
                kwargs={"user_email": "dummy@example.com"},
            ),
            reverse(
                "one_time_login",
                kwargs={"uidb64": "dummy", "token": "dummy-token"},
            ),
            reverse("set_new_password"),
        ]

        if not request.user.is_authenticated:
            if any(request.path.startswith(path) for path in open_paths):
                pass
            else:
                return redirect(reverse("account_login"))
        else:
            request.session["logged_in"] = True

        response = self.get_response(request)

        if request.path == reverse("account_logout"):
            request.session.flush()

        return response
