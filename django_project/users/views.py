from django.shortcuts import render, redirect
from .forms import UserRegistrationForm, UpdateUser, UpdateProfile
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import User
from blog.models import Post
from django.core.paginator import Paginator


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Created account for {username}.')
            return redirect('login')
    else:
        form = UserRegistrationForm()

    context = {
        'form': form
    }
    return render(request, 'users/register.html', context)


@login_required
def profile(request, uid):
    user = User.objects.filter(pk=uid).first()
    posts = Post.objects.filter(author_id=uid).order_by('-date_posted')
    paginate = Paginator(posts, per_page=4)
    page = request.GET.get('page')
    page_obj = paginate.get_page(page)

    context = {
        'puser': user,
        'page_obj': page_obj,
    }
    return render(request, 'users/profile.html', context)


@login_required
def profile_update(request, uid):
    user = User.objects.filter(pk=uid).first()
    posts = Post.objects.filter(author_id=uid)
    if request.method == 'POST':
        u_form = UpdateUser(request.POST, instance=user)
        p_form = UpdateProfile(request.POST, request.FILES, instance=user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Information Updated successfully for {request.user.username}')
            return redirect('profile', user.id)
    else:
        u_form = UpdateUser(instance=user)
        p_form = UpdateProfile(instance=user.profile)

    context = {
        'posts':posts,
        'puser': user,
        'u_form': u_form,
        'p_form': p_form,
    }
    return render(request, 'users/profile_update_page.html', context)
