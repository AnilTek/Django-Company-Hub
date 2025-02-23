from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import login,authenticate,logout,get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm
from django.core.mail import send_mail
from django.conf import settings
from django.utils.http import urlsafe_base64_decode
# Create your views here.
from .tokens import account_activition_token
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes,force_str
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.utils.translation import gettext as _




def activate(request, uidb64 , token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None


    if user is not None and account_activition_token.check_token(user,token):
        user.is_active = True
        user.save()

        messages.success(request, _('Thank you for your email confirmation. Now you can login your account.'))
        return redirect('login')
    else:
        messages.error(request, _('Activation link is invalid!'))


    return redirect('home')


def reset(request, uidb64 , token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None


    if user is not None and account_activition_token.check_token(user,token):
        
        messages.success(request, _('Thank you for your email confirmation. Now you can change your password.'))

        return render(request,'new_password.html' ,{'user_id':user.id})
    else:
        messages.error(request, _('Activation link is invalid!'))


    return redirect('home')

def new_password(request, user_id):
    try:
        user = User.objects.get(pk=user_id)  
    except User.DoesNotExist:
        messages.error(request, _("User not found."))
        return redirect('reset_password')  

    if request.method == 'POST':
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        print(password1)
        print(password2)

        if password1 and password2 and password1 == password2:
            user.set_password(password1)  
            user.save()
            messages.success(request, _('Password changed successfully. You can now log in.'))
            return redirect('login')  
        else:
            messages.error(request, _('Passwords do not match. Please try again.'))

    return render(request, 'new_password.html',{'user_id':user_id})




def passwordEmail(request,user,to_email):
    mail_subject = 'Reset your password'
    message = render_to_string("template_reset_password.html",{
        'user': user.username,
        'domain':get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token':account_activition_token.make_token(user),
        "protocol":'https' if request.is_secure() else 'http'
    })
    email = EmailMessage(mail_subject,message, to=[to_email])
    if email.send():
        
        message = _('Dear {user}, please go to your email {to_email} inbox and click on '
                    ' received  link to reset your password. Note: Check your spam folder.').format(user=user, to_email=to_email)
        messages.success(request, message)
    else:
        message.error(request,f'Problem sending email to {to_email}, chechk if you typed it correctly !')
        

def activateEmail(request,user,to_email):
    mail_subject = 'Activate your user Account.'
    message = render_to_string("template_activate_account.html",{
        'user': user.username,
        'domain':get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token':account_activition_token.make_token(user),
        "protocol":'https' if request.is_secure() else 'http'
    })
    email = EmailMessage(mail_subject,message, to=[to_email])
    if email.send():
        message = _('Dear {user}, please go to your email {to_email} inbox and click on '
                    'received activation link to confirm and complete the registration. Note: Check your spam folder.').format(user=user, to_email=to_email)
        
        messages.success(request,message)
    else:
        message.error(request,f'Problem sending email to {to_email}, chechk if you typed it correctly !')
        
        

def reset_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            print(email)
            print(user)
            passwordEmail(request, user, email)
        except User.DoesNotExist:
            messages.error(request, _("No account is associated with this email address."))
    return render(request, 'reset_password.html')



def login_site(request):

    if request.user.is_authenticated:
        return redirect('home')
    
    print('merhaba')
    if request.method == 'POST':
        print('post method')
        username = request.POST['username']
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, _('User does not exist !'))

        user = authenticate(request,username=username,password=password)

        if user is not None:
            print('giris yaptim')
            login(request,user)
            return redirect('home')
        else:
            messages.error(request, _('Username OR password is incorrect'))
            
    
    return render(request,'login.html')


def register_site(request):
    page = 'register'
    form = CustomUserCreationForm()
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            activateEmail(request,user, form.cleaned_data.get('email'))
            messages.success(request, _('User account was created! Please check your email to verify your account.'))

            login(request, user)
            return redirect('home')

        else:
            messages.error(
                request, _('An error has occurred during registration'))
            
    context = {'page':page,'form':form}

    return render(request,'register.html',context=context)


def logout_site(request):
    logout(request)
    messages.info(request, _('User was logged out !'))
    return redirect('login')
