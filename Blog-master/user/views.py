from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from user.forms import ProfileUpdateForm, UserUpdateForm

from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib import auth


# def register(request):
#     if request.method == 'POST':
#         form = UserRegisterForm(request.POST)
#         if form.is_valid():
#             form.save()
#             username = form.cleaned_data.get('username')
#             messages.success(request, f'Account created for {username}!')
#             return redirect('blog-home')
#     else:
#         form = UserRegisterForm()
#     return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'users/profile.html', context)


def loginT(request):
    if request.method == 'POST':
        username1 = request.POST['email']
        password1 = request.POST['password']

        try:
            user = auth.authenticate(username=User.objects.get(email=username1), password=password1)

        except:
            user = auth.authenticate(username=username1, password=password1)

        if user is not None:
            auth.login(request, user)
            messages.add_message(request, messages.SUCCESS, f'Welcome {user.username}')
            return redirect('/')
        else:
            return render(request, 'users/loginT.html')

    else:
        return render(request, 'users/loginT.html')


def registerT(request):
    if request.method == 'POST':
        user_name1 = request.POST['username']
        first_name1 = request.POST['firstname']
        last_name1 = request.POST['lastname']
        email1 = request.POST['email']
        password1 = request.POST['password']

        user = User.objects.create_user(username=user_name1, email=email1, password=password1)
        user.first_name = first_name1
        user.last_name = last_name1
        user.is_active = True
        user.save()
        return render(request, 'users/loginT.html')

    else:
        return render(request, 'users/registerT.html')



