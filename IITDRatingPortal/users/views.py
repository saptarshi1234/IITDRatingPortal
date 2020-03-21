from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.generic import View
from .tokens import account_activation_token
from django.core.mail import EmailMessage

from .forms import UserForm


def show_user_profile(request):
    return render(request, 'users/profile.html', {})


class UserFormView(View):
    form_class = UserForm
    template_name = 'registration/signIn_form.html'

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            confirm_pass = form.cleaned_data['confirm_pass']
            to_email = form.cleaned_data['email']

            if not to_email.endswith('iitd.ac.in'):
                return render(request, self.template_name, {'form': form, 'error': 'please enter iitd email'})

            if password != confirm_pass:
                return render(request, self.template_name, {'form': form, 'error': 'passwords do not match'})

            if to_email.split('@')[0] in [curr_user.email.split('@')[0] for curr_user in User.objects.all()]:
                return render(request, self.template_name, {'form': form, 'error': 'email address already in use'})
            user.set_password(password)

            user.is_active = False
            user.save()

            current_site = get_current_site(request)
            mail_subject = 'Activate your rating portal account account.'
            message = render_to_string('users/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            print(message)
            email.send()
            return HttpResponse('Please confirm your email address to complete the registration')

        else:
            return render(request, self.template_name, {'form': form, 'error': 'incorrect data'})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('users:show_profile')
    else:
        return HttpResponse('Activation link is invalid!')
