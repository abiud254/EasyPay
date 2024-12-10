from django.contrib import messages
from django.contrib.auth.models import User
from django.core.cache import cache
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.http import urlsafe_base64_decode

from management.models import Employee
from management.utils import get_client_ip, log_activity

from .utils import send_otp, send_password_reset, verify_otp


def verify_employee(request):
    if request.method == "POST":
        id_number = request.POST.get("id_number")
        try:
            employee = Employee.objects.get(id_number=id_number)

            # Check if the employee is already verified
            if employee.verified:
                if employee.user:  # Check if the employee has a user associated
                    messages.info(request, "You have already verified. Please log in.")
                    return redirect("login_employee")
                else:
                    messages.info(
                        request, "You have already verified. Please create an account."
                    )
                    request.session["id_number"] = (
                        id_number  # Save ID number in session
                    )
                    return redirect("create_account")
            else:
                # Generate OTP
                send_otp(employee)  # Using the new send_otp function
                request.session["id_number"] = id_number  # Save ID number in session
                messages.success(
                    request, "A one-time code has been sent to your email."
                )
                return redirect("verify_code")  # Redirect to OTP verification form
        except Employee.DoesNotExist:
            messages.error(request, "ID Number not found. Contact an administrator.")
            return redirect("verify_employee")  # Redirect to verification form

    return render(request, "verify_employee.html")


def verify_code(request):
    id_number = request.session.get("id_number")  # Get the ID number from the session
    if not id_number:
        messages.error(request, "Employee not found. Please verify your ID.")
        return redirect("verify_employee")

    if request.method == "POST":
        otp_input = "".join(
            [
                request.POST.get("code1", ""),
                request.POST.get("code2", ""),
                request.POST.get("code3", ""),
                request.POST.get("code4", ""),
                request.POST.get("code5", ""),
                request.POST.get("code6", ""),
            ]
        )

        try:
            employee = Employee.objects.get(id_number=id_number)
            verification_result = verify_otp(
                employee, otp_input
            )  # Use the new OTP verification function

            if verification_result == "Employee successfully verified.":
                request.session["id_number"] = id_number  # Save ID for account creation
                messages.success(request, "Code verified successfully!")
                return redirect("create_account")
            else:
                messages.error(request, verification_result)
        except Employee.DoesNotExist:
            messages.error(request, "Employee not found. Please verify your ID.")

    return render(request, "verify_code.html", {"id_number": id_number})


def resend_otp(request, id_number):
    try:
        # Get the employee by ID number
        employee = Employee.objects.get(id_number=id_number)

        # Resend OTP
        send_otp(employee)  # Using the new send_otp function

        # Success message
        messages.success(request, "OTP has been resent successfully.")
    except Employee.DoesNotExist:
        # Handle case where employee is not found
        messages.error(request, "Employee not found.")

    # Redirect to verify_code with id_number as a query parameter
    return redirect(f"{reverse('verify_code')}?id_number={id_number}")


def request_password_reset(request):
    if request.method == "POST":
        email = request.POST.get("email")
        try:
            user = User.objects.get(email=email)

            # Call the function to send the password reset email
            send_password_reset(request, user)

            messages.success(
                request,
                "If your email is registered, a password reset link has been sent.",
            )
        except User.DoesNotExist:
            # Do not reveal user existence
            messages.success(
                request,
                "If your email is registered, a password reset link has been sent.",
            )
        return redirect("request_password_reset")

    return render(request, "request_password_reset.html")


def reset_password_form(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)

        # Check if token is valid
        cached_user_id = cache.get(token)
        if cached_user_id != user.pk:
            messages.error(request, "Invalid or expired password reset link.")
            return redirect("request_password_reset")
    except (User.DoesNotExist, ValueError):
        messages.error(request, "Invalid password reset link.")
        return redirect("request_password_reset")

    if request.method == "POST":
        password = request.POST.get("new_password1")
        password_confirm = request.POST.get("new_password2")

        if password != password_confirm:
            messages.error(request, "Passwords do not match.")
        else:
            user.set_password(password)
            user.save()
            cache.delete(token)  # Invalidate the token
            messages.success(request, "Password reset successfully.")
            # Log the activity
            log_activity(
                user=user,
                action="Password Reset",
                ip_address=get_client_ip(request),
            )
            return redirect("login_employee")

    return render(
        request, "reset_password_form.html", {"uidb64": uidb64, "token": token}
    )
