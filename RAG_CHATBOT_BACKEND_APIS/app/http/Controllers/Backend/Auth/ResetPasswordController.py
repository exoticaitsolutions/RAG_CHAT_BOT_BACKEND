from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.contrib import messages
from django.urls import reverse

CustomUser = get_user_model()

class ResetPasswordController:
    def reset_password_page(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = CustomUser.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            if request.method == "POST":
                new_password = request.POST.get("password")
                confirm_password = request.POST.get("confirm_password")

                if new_password == confirm_password:
                    user.set_password(new_password)
                    user.save()
                    messages.success(request, "Password reset successfully. Please log in.")

                    # ✅ Redirect to login page after success
                    return redirect(reverse("login"))
                else:
                    messages.error(request, "Passwords do not match.")
                    return render(request, 'admin/auth/resetpasswordpage.html', {"validlink": True, "uid": uidb64, "token": token})

            # ✅ Load reset password page if the request is GET
            return render(request, 'admin/auth/resetpasswordpage.html', {"validlink": True, "uid": uidb64, "token": token})
        
        else:
            messages.error(request, "The password reset link is invalid or expired.")
            return redirect(reverse("forget_password"))  # ✅ Use reverse() for better URL handling
