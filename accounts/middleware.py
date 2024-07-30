from django.shortcuts import redirect
from django.urls import reverse


class PreventBackAfterLogoutMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Define open paths
        open_paths = [
            reverse("home"),
            reverse("account_login"),
            reverse("account_signup"),
            reverse("password_reset"),
            reverse("password_reset_done"),
            # reverse(
            #     "password_reset_confirm",
            #     kwargs={"uidb64": "uid", "token": "token"},
            # ),
            # Include kwargs for pattern matching
            reverse("account_reset_password_from_key_done"),
        ]

        # Allow access to open paths
        if not request.user.is_authenticated:
            if any(request.path.startswith(path) for path in open_paths):
                pass  # Allow access to open paths
            else:
                return redirect(reverse("account_login"))
        else:
            request.session["logged_in"] = True

        response = self.get_response(request)

        # Flush session on logout
        if request.path == reverse("account_logout"):
            request.session.flush()

        return response
