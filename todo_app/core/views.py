from core.forms import SignUpForm
from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login
from django.http import HttpRequest
from django.shortcuts import redirect, render

User = get_user_model()


def front_page(request: HttpRequest):
    return render(request, 'core/front_page.html')


def sign_up(request: HttpRequest):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()  # user is created

            login(request, user)
            return redirect('/')
    else:
        form = SignUpForm()

    print(form.errors)
    context = {'form': form}
    return render(request, 'core/sign_up.html', context=context)


def login_view(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Check if the user exists
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            messages.error(request, 'The username does not exist')
            return render(request, 'core/login.html')

        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')  # Redirect to a success page
        else:
            messages.error(request, 'Invalid password')

    return render(request, 'core/login.html')
