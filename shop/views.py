from django.shortcuts import render,redirect
from .forms import RegistrationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


@login_required
def home(request):
    return render(request, 'shop/home.html')

def register(request):

    if request.method == 'POST':

        form = RegistrationForm(request.POST)

        if form.is_valid():

            name = form.cleaned_data['name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=name
            )

            return redirect('login')

    else:
        form = RegistrationForm()

    return render(
        request,
        'shop/register.html',
        {'form': form}
    )
def login_view(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = None

        # Check whether input is an email
        if '@' in username:

            try:
                user_object = User.objects.get(email=username)

                user = authenticate(
                    request,
                    username=user_object.username,
                    password=password
                )

            except User.DoesNotExist:

                user = None

        else:

            user = authenticate(
                request,
                username=username,
                password=password
            )

        if user is not None:

            login(request, user)

            return redirect('home')

        else:

            error = "Invalid username/email or password."

            return render(
                request,
                'shop/login.html',
                {'error': error}
            )

    return render(request, 'shop/login.html')


def logout_view(request):

    logout(request)

    return redirect('login')

   