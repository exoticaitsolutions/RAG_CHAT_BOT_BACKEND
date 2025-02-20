from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.urls import reverse
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt


CustomUser = get_user_model()


class ForgetPasswordController:

    @csrf_exempt  # ⚠️ Remove this after testing for security reasons
    def forget_password_page(self, request):
        if request.method == "POST":
            email = request.POST.get("email")
            user = CustomUser.objects.filter(email=email).first()

            if user:
                # Generate token
                token = default_token_generator.make_token(user)
                uid = urlsafe_base64_encode(force_bytes(user.pk))

                # Generate reset link
                reset_link = request.build_absolute_uri(reverse('reset_password', kwargs={'uidb64': uid, 'token': token}))

                # Debugging print to check the generated link
                print(f"Generated reset link: {reset_link}")

                # Send email
                send_mail(
                    subject="Password Reset Request",
                    message=f"Click the link to reset your password: {reset_link}",
                    from_email="pythonweb@exoticaitsolutions.com",  # ✅ Ensure this is a valid email
                    recipient_list=[email],  # ✅ Ensure recipient email is correct
                    fail_silently=False,
                )

                messages.success(request, "Password reset link sent to your email.")

                # ✅ Redirect user to the reset password page
                return redirect(reset_link)  
            else:
                messages.error(request, "Your email is incorrect, please try again!!!")
                return redirect("/forget-password/")

        return render(request, 'admin/auth/forgetpasswordpage.html')
