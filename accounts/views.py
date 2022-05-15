from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from .models import Account
from .forms import RegistrationForm

# User Verefication Email
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.core.mail import send_mail
from StoreProject import settings


def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            phone_number = form.cleaned_data['phone_number']
            username = first_name + last_name
            user = Account.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                email=email,
                username=username,
                password=password,
            )
            user.phone_number = phone_number
            user.save()

            # USer Activation
            current_site = get_current_site(request)
            mail_subject = "Please activate your Account"
            message = render_to_string('accounts/account_verification_email.html',
                                       {
                                           'user': user,
                                           'domain': current_site,
                                           'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                                           'token': default_token_generator.make_token(user),
                                       })
            to_email = email
            send_email = EmailMessage(
                subject=mail_subject, body=message, to=[to_email])
            send_email.send(fail_silently=False)
            # send_mail(mail_subject, message,
            #           from_email='AbdElMegeedX7@gmail.com',
            #           recipient_list=[to_email])

            # messages.success(
            #     request, "Thank you for your registration, We have send the verification email")
            return redirect('/accounts/login/command=verification&email='+email+'/')
            # return redirect('login')

    else:
        form = RegistrationForm()

    context = {'form': form, }
    return render(request, 'accounts/register.html', context)


def login(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email, password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, "You are LogidIn")
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid Login credintial")
            return redirect('login')

    return render(request, 'accounts/login.html')


@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    messages.success(request, "You are Logged out")
    return redirect('login')


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account.default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Your account is activated")
        return redirect('login')
    else:
        messages.error(request, "Invalid Account link")
        return redirect("register")


@login_required(login_url="login")
def dashboard(request):
    return render(request, 'accounts/dashboard.html')
