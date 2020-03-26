from django.contrib.auth import login,logout
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.generic import View

from courses.models import *
from professors.models import *
from .forms import UserForm, BanForm
from .tokens import account_activation_token


def show_user_profile(request):
    context = dict()
    if request.user.is_superuser:
        all_rating_all_author = list(Prof_Rating.objects.all()) + list(Course_Rating.objects.all())
        all_rating_all_author.sort(reverse=True, key=lambda x: x.datetime)
        context['all_rating'] = all_rating_all_author

        reported_reviews = list(Prof_Rating.objects.all().filter(reported=True)) + list(
            Course_Rating.objects.all().filter(reported=True))
        reported_reviews.sort(reverse=True, key=lambda x: x.last_reported_time)
        context['reported'] = reported_reviews

        context['banned_users'] = list(filter(lambda x: x.userprofile.is_banned, list(User.objects.all())))
    else:
        all_rating_user = list(request.user.prof_rating_set.all()) + list(request.user.course_rating_set.all())
        all_rating_user.sort(reverse=True, key=lambda x: x.datetime)
        context['all_rating'] = all_rating_user

        context['warnings'] = list(request.user.userwarning_set.all())

    return render(request, 'users/profile.html', context)


class UserFormView(View):
    form_class = UserForm
    template_name = 'registration/signIn_form.html'

    def get(self, request):
        logout(request)
        print(get_current_site(request).domain,5)
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

            # if to_email.split('@')[0] in [curr_user.email.split('@')[0] for curr_user in User.objects.all()]:
            #     return render(request, self.template_name, {'form': form, 'error': 'email address already in use'})
            user.set_password(password)

            user.is_active = False
            user.save()

            current_site = get_current_site(request)
            mail_subject = 'Activate your rating portal account account.'
            message = render_to_string('users/account_activation_email.html', {
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
            return HttpResponse('<p>We have sent an email containing the activation link.<br> Please confirm your email address to complete the registration</p>')

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
        login(request, user,backend='django.contrib.auth.backends.ModelBackend')
        return redirect('users:show_profile')
    else:
        return HttpResponse('Activation link is invalid!')


def ban_user(request, user_id):
    user = User.objects.get(pk=user_id)
    if request.POST:
        form = BanForm(request.POST)
        if form.is_valid():
            days = form.cleaned_data['ban_days']
            print(days)

            user.is_active = False
            user.userprofile.is_banned = True
            user.userprofile.banned_on = datetime.now()
            user.userprofile.ban_days = int(days)
            if days == '0':
                msg = 'indefinitely'
                user.userprofile.indefinite_ban = True
            else:
                user.userprofile.indefinite_ban = False
                msg = 'for ' + days + ' days'

            # send email
            current_site = get_current_site(request)
            mail_subject = 'Ban from site'
            message = render_to_string('users/account_ban.html', {
                'user': user,
                'domain': current_site.domain,
                'days': msg
            })
            to_email = user.email
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            print(message)
            # email.send()
            user.save()
            return HttpResponseRedirect(reverse('users:show_profile'))

    else:
        form = BanForm(None)
        return render(request, 'users/ban_form.html', {'form': form})


def remove_ban(request, user_id):
    user = User.objects.get(id=user_id)
    user.is_active = True
    user.userprofile.is_banned = False
    current_site = get_current_site(request)
    mail_subject = 'Removal of Ban from site'
    message = render_to_string('users/account_ban_removal.html', {
        'user': user,
        'domain': current_site.domain,
    })
    to_email = user.email
    email = EmailMessage(
        mail_subject, message, to=[to_email]
    )
    print(message)
    # email.send()
    user.save()
    return HttpResponseRedirect(reverse('users:show_profile'))


def warn(request, user_id):
    user = User.objects.get(id=user_id)
    warning = UserWarning.objects.create(user=user, message='U r being warned', time=datetime.now())
    return HttpResponseRedirect(reverse('users:show_profile'))


from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.exceptions import *

class MySocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        print(dir(sociallogin.account))
        print(request.user)
        if not sociallogin.is_existing and request.user.is_anonymous:
            raise ImmediateHttpResponse(render(request,'users/login_error.html',))




