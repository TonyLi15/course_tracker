from django.shortcuts import render, redirect # For rendering pages
from django.utils.text import slugify # For slugifying the post
from django.views.generic import TemplateView # For template tag
from django.db.models import Avg # For calculating average score of each course
from django.contrib.auth import authenticate, login, logout # For user login and logout
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseForbidden # For redirecting to another page
from django.urls import reverse # For redirecting to another page
from django.contrib.auth.decorators import login_required # For login required pages
from .forms import * # Import all forms
from .models import * # Import all models

# Welcome Page
def welcome(request):
    return render(request, 'welcome.html')

# Login Page
def Login(request):
    if request.method == 'POST':
        ID = request.POST.get('userid')
        Pass = request.POST.get('password')

        # User Authentication
        user = authenticate(username=ID, password=Pass)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("This account is not valid")

        else:
            return HttpResponse("Incorrect login ID or password")
        
    # GET
    else:
        return render(request, 'login.html')
    
#Logout -> Redirect to login page
@login_required
def Logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('Login'))

#Index Page -> After Login
@login_required
def index(request):
    courses = Course.objects.all().annotate(average_score=Avg('comments__score'))
    favorite_courses = request.user.account.favorite_courses.all().annotate(average_score=Avg('comments__score'))
    total_credits = sum(course.credit for course in favorite_courses)
    context = {"UserID":request.user.account,
               'courses':courses, 
               'favorite_courses':favorite_courses,
               'total_credits': total_credits,
    }

    return render(request, "index.html", context)

# Course creation page
@login_required
def create_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save(commit=False)
            course.slug = slugify(course.title)  # Generate the slug based on the title
            # Check for duplicate courses
            if Course.objects.filter(title=course.title).exists():
                # Handle duplicate course error
                form.add_error('title', 'A course with this title already exists.')
            else:
                course.save()
                return redirect('index')
    else:
        form = CourseForm()

    context = {
        'form': form,
    }

    return render(request, 'create_course.html', context)

# Course edit page
@login_required
def edit_course(request, slug):
    course = Course.objects.get(slug=slug)

    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            return redirect('course_detail', slug=course.slug)
    else:
        form = CourseForm(instance=course)

    context = {
        'form': form,
        'course':course,
    }

    return render(request, 'edit_course.html', context)

# Comment edit page
@login_required
def edit_comment(request, comment_id):
    comment = Comment.objects.get(id=comment_id)

    # Debug
    print(f"request.user.account: {str(request.user.account)}")
    print(f"comment.name: {comment.name}")

    # Check if the user is the author of the comment
    if str(request.user.account) != comment.name:
        return HttpResponseForbidden("You are not authorized to edit this comment.")

    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('course_detail', slug=comment.course.slug)
    else:
        form = CommentForm(instance=comment)

    context = {
        'form': form,
        'comment':comment,
    }

    return render(request, 'edit_comment.html', context)

# Course Detail Page
@login_required
def course_detail(request, slug):
    course = Course.objects.get(slug=slug)

    if request.method == 'POST':
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.name = request.user.account
            comment.course = course
            comment.save()

            return redirect('course_detail', slug=course.slug)
        
    else:
        form = CommentForm()

    context = {'course': course, 
               'form': form, 
               'UserID': request.user.account
               }

    return render(request, 'course_detail.html', context)

# Add favorite course
@login_required
def add_favorite(request, slug):
    course = Course.objects.get(slug=slug)
    request.user.account.favorite_courses.add(course)
    return redirect('index')

# Remove favorite course
@login_required
def remove_favorite(request, slug):
    course = Course.objects.get(slug=slug)
    request.user.account.favorite_courses.remove(course)
    return redirect('index')

# My Page
@login_required
def mypage(request):
    courses = Course.objects.all().annotate(average_score=Avg('comments__score'))
    favorite_courses = request.user.account.favorite_courses.all().annotate(average_score=Avg('comments__score'))
    total_credits = sum(course.credit for course in favorite_courses)
    context = {"UserID":request.user.account,
               'courses':courses, 
               'favorite_courses':favorite_courses,
               'total_credits': total_credits,
    }
    return render(request, "mypage.html", context)

# Search
@login_required
def search(request):
    query = request.GET.get('q')  # Get the search query from the request

    if query:
        # Perform the search operation
        results = Course.objects.filter(title__icontains=query)
    else:
        results = []  # Empty list if no query is provided

    context = {
        'query': query,
        'results': results,
    }

    return render(request, 'search.html', context)

# New Account Registration
class AccountRegistration(TemplateView):

    def __init__(self):
        self.params = {
        "AccountCreate":False,
        "account_form": AccountForm(),
        "add_account_form":AddAccountForm(),
        }
    
    # Get Method
    def get(self,request):
        self.params["account_form"] = AccountForm()
        self.params["add_account_form"] = AddAccountForm()
        self.params["AccountCreate"] = False
        return render(request,"register.html",context=self.params)
    
    # Post Method
    def post(self,request):
        self.params["account_form"] = AccountForm(data=request.POST)
        self.params["add_account_form"] = AddAccountForm(data=request.POST)

        # Check if the contents of form is valid
        if self.params["account_form"].is_valid() and self.params["add_account_form"].is_valid():
            # Save account information to database
            account = self.params["account_form"].save()

            # Hash the password
            account.set_password(account.password)

            # Update the hashed password
            account.save()

            # Additional Information Below
            # No commit
            add_account = self.params["add_account_form"].save(commit=False)
            # AccountForm & AddAccountForm 1vs1 紐付け
            add_account.user = account

            # Save Model
            add_account.save()

            # Update the information of accounts
            self.params["AccountCreate"] = True

        else:
            # Print corresponding errors if form is not valid
            print(self.params["account_form"].errors)

        return render(request,"register.html",context=self.params)