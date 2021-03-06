from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Post, Comment, Category, SiteConfiguration
from .forms import CommentForm,TagForm
from django.core.mail import send_mail, BadHeaderError
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
import os

# Create your views here.
def blog_index(request):
    posts = Post.objects.all().order_by('-date_created')
    paginator = Paginator(posts, 5)
    page_number = request.GET.get('page',1)
    page = paginator.get_page(page_number)
    if page.has_next():
        next_url = f'?page={page.next_page_number()}'
    else:
        next_url = ''
    if page.has_previous():
        prev_url = f'?page={page.previous_page_number()}'
    else:
        prev_url = ''

    context = {
        'posts': posts,
        "page": page,
        'next_page_url': next_url,
        'prev_page_url': prev_url,

    }
    return render(request, "blog/index.html", context)

def blog_detail(request, pk):
    post = Post.objects.get(pk=pk)
    posts = Post.objects.all().order_by('-date_created')
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = Comment(
                author=form.cleaned_data["author"],
                body=form.cleaned_data["body"],
                post=post
            )
            comment.save()
    comments = Comment.objects.filter(post=post)
    form = CommentForm()
    context = {
        "post": post,
        "comments": comments,
        "form": form,
        "posts": posts,
    }
    return render(request, "blog/detail.html", context)

def blog_category(request, category='all'):
    selected=[]
    search = ''
    if request.method == 'POST':
        if not(request.POST.get('search')):
            form = TagForm(request.POST)
            if form.is_valid():
                tags = form.cleaned_data["tag"]
                if tags:
                    for item in tags:
                        selected.append(item.name)

    if category == 'custom':
        if request.POST.get('search'):
            search = request.POST.get('search')
            posts = Post.objects.filter(Q(title__icontains=search) |
                Q(body1__icontains=search) | Q(body2__icontains=search) |
                Q(body3__icontains=search) | Q(body4__icontains=search))
        else:
            if len(selected) > 0:
                posts = Post.objects.filter(
                    categories__name__in=selected
                ).order_by(
                    '-date_created'
                ).distinct()
            else:
                posts = Post.objects.all().order_by('-date_created')
                selected = None
    elif category == 'all':
        posts = Post.objects.all().order_by('-date_created')
    else:
        posts = Post.objects.filter(
            categories__name__contains=category
        ).order_by(
            '-date_created'
        )
    tagform = TagForm()
    categories = Category.objects.all()
    paginator = Paginator(posts, 5)
    page_number = request.GET.get('page',1)
    page = paginator.get_page(page_number)
    if page.has_next():
        next_url = f'?page={page.next_page_number()}'
    else:
        next_url = ''
    if page.has_previous():
        prev_url = f'?page={page.previous_page_number()}'
    else:
        prev_url = ''
    context = {
        "selected":selected,
        "category": category,
        "posts": posts,
        "categories" : categories,
        "tagform": tagform,
        "page": page,
        'next_page_url': next_url,
        'prev_page_url': prev_url,
        'search': search,
    }
    return render(request, "blog/archive.html", context)

def blog_contact(request):
    posts = Post.objects.all().order_by('-date_created')
    context = {
        "posts": posts,
    }
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        msg = request.POST['msg']
        config = SiteConfiguration.objects.get()
        message = f'Name: {name},\n\n' \
        f'Email: {email},\n\n' \
		f'Message: {msg}'
        subject = "Private Message"
        try:
            send_mail(subject, message, email, [config.contact_mail])
        except BadHeaderError:
            messages.info(request, 'Invalid header found.')
            return render(request, "contact.html")
        messages.info(request, 'Your message has been sent successfully!')
        return render(request, "blog/contact.html", context)
    return render(request, "blog/contact.html", context)

def blog_about(request):
    posts = Post.objects.all().order_by('-date_created')
    config = SiteConfiguration.objects.get()
    context = {
        "posts": posts,
        "config": config,
    }
    return render(request, "blog/about.html", context)
