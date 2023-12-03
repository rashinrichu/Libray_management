from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User,auth
from django.core.mail import send_mail
from django.conf import settings
from . models import *
from django.http import HttpResponseForbidden

from django.contrib.auth import authenticate,login,logout
from django.shortcuts import render
from django.db.models import Q
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest, JsonResponse


from django.shortcuts import render, redirect
from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User,auth
from django.core.mail import send_mail
from django.conf import settings
from . models import *
from django.contrib.auth import authenticate,login,logout
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings


def index(request):
    books = Book.objects.all()
    context = {'books': books}
    return render(request, 'index.html', context)

def contact(request):
    return render (request,'contact.html')

def about(request):
    return render (request,'about.html')

def register(request):
    return render(request,'student_registration.html')

def login(request):
    return render(request,'login.html')

def admin_home(request):
    books = Book.objects.all()
    context = {'books': books}
    return render(request,'admin_home.html',context)

@login_required(login_url='/registration/')
def user_home(request):
    books = Book.objects.all()
    context = {'books': books}
    return render(request,'user_home.html',context)

from datetime import datetime
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages


from django.contrib.auth.models import User

def registration(request):
    if request.method == 'POST':
        # Get the user data from the request
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        address = request.POST.get('address')
        phone_number = request.POST.get('phone_number')
        dob = request.POST.get('dob')
        image = request.FILES.get('image')

        # Check if the passwords match
        if password != confirm_password:
            messages.error(request, 'Passwords do not match')
            return redirect('register')

        # Check if the username or email already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken')
            return redirect('register')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'Email already taken')
            return redirect('register')

        # Create the user object
        user = User.objects.create_user(username=username, email=email, password=password, first_name=first_name, last_name=last_name)

        # Create the member object
        member = Member.objects.create(username=username, email=email, first_name=first_name, last_name=last_name, address=address, phone_number=phone_number, dob=dob, image=image)

        # Send a confirmation email to the user
        subject = 'Welcome to BrightMate'
        message = f'Thank you for joining BrightMate! We hope our website will be a valuable resource for you. To log in, please use the following details: username - {username}.\npassword - {password}. We look forward to seeing you around the site.'
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [email]
        send_mail(subject, message, from_email, recipient_list, fail_silently=False)

        # Redirect to the login page
        messages.success(request, 'Registration successful. Please login to continue.')
        return redirect('login')
    else:
        return render(request, 'student_registration.html')

import time
#member_login


from django.contrib import auth, messages


def member_login(request):
    alert = False
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            messages.success(request, 'Logged in successfully!')
            if user.is_staff:
                return redirect('admin_home')
            else:
                return redirect('user_home')
        else:
            messages.error(request, 'Invalid username or password')
            alert = True
    return render(request, 'login.html', {'alert': alert})

#logout
def logout(request):
	auth.logout(request)
	return redirect('index')
  

#profilepage

@login_required
def member_profile(request):
    if request.user.is_authenticated:
        current_user = request.user
        username=current_user.username
        student=Member.objects.get(username=username)
        return render(request,'profile.html',{'student':student})
    
    
#edit_profile


@login_required
def edit_profile(request):
    member, created = Member.objects.get_or_create(username=request.user)

    if request.method == 'POST':
        member.first_name = request.POST.get('first_name', '')
        member.last_name = request.POST.get('last_name', '')
        member.username = request.POST.get('username', '')
        member.phone_number = request.POST.get('phone_number', '')
        member.email = request.POST.get('email', '')
        member.address = request.POST.get('address', '')
        dob_str = request.POST.get('dob', '')
        if dob_str:
            dob = datetime.strptime(dob_str, '%Y-%m-%d')  # Use datetime instead of datetime.datetime
            member.dob = dob
        member.image = request.FILES.get('image', member.image)

        member.save()
        return redirect('member_profile')    


    context = {'student': member}
    return render(request, 'edit_profile.html', context)


#add_book(admin)


@login_required
def add_book(request):
    categories = Category.objects.all()
    if request.method == 'POST':
        # Get form data from request.POST dictionary
        title = request.POST.get('title')
        author = request.POST.get('author')
        description = request.POST.get('description')
        category_id = request.POST.get('category')
        category = Category.objects.get(id=category_id)
        available_copies = request.POST.get('available_copies')
        language = request.POST.get('language')
        price = request.POST.get('price')
        year_of_publish = request.POST.get('year_of_publish')
        image = request.FILES.get('image')

        # Create a new book object with form data
        book = Book.objects.create(
            title=title,
            author=author,
            description=description,
            category=category,
            available_copies=available_copies,
            language=language,
            price=price,
            year_of_publish=year_of_publish,
            image=image,
        )

        # Add success message
        messages.success(request, 'Book added successfully.')

        return redirect('book_list_all')

    context = {'categories': categories}
    return render(request, 'add_book.html', context)



from django.shortcuts import redirect


from django.contrib import messages

@login_required
def edit_book(request, book_id):
    categories = Category.objects.all() # get all categories from the database
    book = get_object_or_404(Book, id=book_id)

    if request.method == 'POST':
        # Get form data from request.POST dictionary
        title = request.POST.get('title')
        author = request.POST.get('author')
        description = request.POST.get('description')
        category_id = request.POST.get('category') # get category ID from form data
        category = Category.objects.get(id=category_id) # get category object from database
        available_copies = request.POST.get('available_copies')
        language = request.POST.get('language')
        price = request.POST.get('price')
        year_of_publish = request.POST.get('year_of_publish')
        image = request.FILES.get('image')

        # Update the book object with form data
        book.title = title
        book.author = author
        book.description = description
        book.category = category
        book.available_copies = available_copies
        book.language = language
        book.price = price
        book.year_of_publish = year_of_publish
        if image:
            book.image = image
        book.save()
        messages.success(request, 'Book updated successfully.')
        return redirect('book_list', book_id=book.id)

    context = {'books': book, 'categories': categories}
    return render(request, 'edit_book.html', context)

#delete_book
from django.http import JsonResponse

from django.http import Http404

def delete_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    if request.method == 'POST':
        book.delete()
        messages.success(request, f'Book "{book.title}" has been deleted successfully.')
        return redirect('book_list_all')

    context = {'book': book}
    return render(request, 'delete_book.html', context)




def book_list_all(request):
    books = Book.objects.all()
    context = {'books': books}
    return render(request, 'book_list_all.html', context)


@login_required(login_url='/registration/')
def book_list(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    context = {'book': book}
    return render(request, 'book_list.html', context)

#request_book


from django.shortcuts import get_object_or_404, render, redirect



from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from .models import RequestBook

import json
from django.http import JsonResponse


@login_required(login_url='/registration/')
def request_book(request, book_id):
    # Get the book object
    book = get_object_or_404(Book, id=book_id)

    if request.method == 'POST':
        # Create a book request object
        member = Member.objects.get(username=request.user)
        request_book = RequestBook(member=member, book=book)
        request_book.save()

        # Return a JSON response indicating success
        response_data = {'success': True, 'message': f"Book request for '{book.title}' has been made successfully!"}
        return JsonResponse(response_data)

   
    return render(request, 'book_list_student.html', {'book': book})

#add category
def add_category(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        category = Category(name=name, description=description)
        category.save()
        messages.success(request, 'Category has been added successfully.') # Add success message
        return redirect('category_list')
    else:
        return render(request, 'add_category.html')


@login_required(login_url='/registration/')
def book_list_student(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    context = {'book': book}
    return render(request, 'book_list_student.html', context)

#searchbar
def search(request):
    query = request.GET.get('q')

    # Search for books and categories that match the query
    books = Book.objects.filter(Q(title__icontains=query) | Q(author__icontains=query))
    categories = Category.objects.filter(name__icontains=query)

    # If a single category matches the query, get the books in that category
    if len(categories) == 1:
        category = categories.first()
        books = Book.objects.filter(category=category)

    context = {
        'books': books,
        'categories': categories,
        'query': query
    }
    return render(request, 'search_result.html', context)

#admin all requested books
def all_requested_books(request):
    # Get all the book requests from the database
    book_requests = RequestBook.objects.all()

    return render(request, 'all_requested_books.html', {'book_requests': book_requests})

from django.http import HttpResponse

from django.http import JsonResponse
from datetime import datetime, timedelta

def proceed_request(request, request_id):
    issue = get_object_or_404(RequestBook, id=request_id)
    book = issue.book
    if book.available_copies > 0:
        issue_book = IssueBook.objects.create(
            member=issue.member,
            book=book,
            due_date=datetime.now() + timedelta(days=10)
        )
        issue_book.request_status = 'Accepted'
        issue_book.save()
        issue.delete()
        book.available_copies -= 1
        book.save()
        return redirect('book_list_all')
    else:
        messages.error(request, 'No copies of this book are currently available.')
        return redirect('all_requested_books')








#cancel book request


def cancel_book(request, request_id):
    request_book = get_object_or_404(RequestBook, id=request_id)

    if request.method == 'POST':
        # Create a new record of the cancelled book request
        CancelledBook.objects.create(
            member=request_book.member,
            book=request_book.book,
            request=request_book
        )
        
        # Delete the original book request
        request_book.delete()
        
        # Add a success message and redirect to the book requests page
        messages.success(request, 'Book request successfully cancelled.')
        return redirect('all_requested_books')

    context = {'request_book': request_book}
    return render(request, 'all_requested_books.html', context)


@login_required
def issued_books(request):
    # Get the currently logged in user
    user = request.user

    # Get the Member instance for the user
    member = Member.objects.get(username=user)

    # Get the requested books for the member
    requested_books = RequestBook.objects.filter(member=member)

    # Get the issued books for the member
    issued_books = IssueBook.objects.filter(member=member)

    context = {
        'requested_books': requested_books,
        'issued_books': issued_books
    }

    return render(request, 'issued_books.html', context)




#admin cancelled books 




#cancelled request show the user 




@login_required
def cancelled_requests(request):
    member = Member.objects.get(username=request.user)
    cancelled_requests = RequestBook.objects.filter(member=member)
    return render(request, 'cancelled_requests.html', {'cancelled_requests': cancelled_requests})



@login_required
def returned_books(request):
    # Get the currently logged in user
    user = request.user

    # Get the Member instance for the user
    member = Member.objects.get(username=user)

    # Get the requested books for the member
    requested_books = RequestBook.objects.filter(member=member)

    # Get the issued books for the member
    issued_books = IssueBook.objects.filter(member=member)

    context = {
        'requested_books': requested_books,
        'issued_books': issued_books
    }

    return render(request, 'return_book.html', context)
#return book




from django.urls import reverse

from django.http import JsonResponse

from django.views.decorators.cache import cache_control

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def return_book(request, issued_book_id):
    issued_book = get_object_or_404(IssueBook, id=issued_book_id)
    if request.method == 'POST':
        issued_book.return_date = timezone.now()
        issued_book.save()

        # Create a new ReturnBook object
        return_book = ReturnBook.objects.create(
            issue=issued_book,
            member=issued_book.member,
            return_date=issued_book.return_date,
        )

        # Update the issued_books queryset to exclude the returned book
        issued_books = IssueBook.objects.filter(
            Q(return_date__isnull=True) & Q(member=issued_book.member))

        # Return a JSON response with the success message
        return JsonResponse({'message': 'Book has been returned successfully'})

    # Retrieve only the issued books that have not been returned
    issued_books = IssueBook.objects.filter(return_date__isnull=True, member=issued_book.member)

    context = {'issued_books': issued_books}
    return render(request, 'return_book.html', context)


def returned_books_admin(request):
    returned_books = ReturnBook.objects.all()
    context = {'returned_books': returned_books}
    return render(request, 'returned_books.html', context)

#proceed return admin
def proceed_return(request, return_id):
    returned_book = get_object_or_404(ReturnBook, id=return_id)
    book = returned_book.issue.book
    book.available_copies += 1
    book.save()
    returned_book.status = 'PROCEED'
    returned_book.save()
    messages.success(request, 'Return has been marked as Proceed')
    # Remove the returned book item from the list, but don't delete it permanently
    returned_book.delete()
    return redirect('returned_books_admin')



def cancel_return(request, return_id):
    returned_book = ReturnBook.objects.get(id=return_id)
    returned_book.delete()
    messages.success(request, 'Return has been cancelled')
    return redirect('returned_books_admin')


from django.shortcuts import render, get_object_or_404
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect



from .models import ReturnBook

#add penalty

# def add(request):
#     return render(request,'add_penalty.html')

from django.contrib import messages

def add_penalty(request, return_id):
    return_book = get_object_or_404(ReturnBook, id=return_id)
    if request.method == 'POST':
        penalty_reason = request.POST.get('penalty_reason')
        fine_amount = request.POST.get('fine_amount')
        return_book.penalty_reason = penalty_reason
        return_book.fine_amount = fine_amount
        return_book.save()
        messages.success(request, 'Penalty added successfully.')
        return redirect('returned_books_admin')
    else:
        context = {'penalty_reason_choices': ReturnBook.PENALTY_CHOICES,
                   'fine_amount': return_book.fine_amount,
                   'return_book': return_book}
        return render(request, 'penalty_list.html', context)




#category 

@login_required(login_url='/registration/')
def category_list(request):
    categories = Category.objects.all()
    return render(request, 'category_list.html', {'categories': categories})


def category_books(request, category_id):
    category = Category.objects.get(id=category_id)
    books = Book.objects.filter(category=category)
    context = {'category': category, 'books': books}
    return render(request, 'category_books.html', context)

def search_books_student(request):
    query = request.GET.get('q')

    # Search for books and categories that match the query
    books = Book.objects.filter(Q(title__icontains=query) | Q(author__icontains=query))
    categories = Category.objects.filter(name__icontains=query)

    # If a single category matches the query, get the books in that category
    if len(categories) == 1:
        category = categories.first()
        books = Book.objects.filter(category=category)

    context = {
        'books': books,
        'categories': categories,
        'query': query
    }
    return render(request, 'search_result_student.html', context)

#show all members

def show_members(request):
    members = Member.objects.all()
    return render(request, 'member.html', {'members': members})

#delete memeber

def delete_member(request, member_id):
    member = get_object_or_404(Member, id=member_id)
    member.delete()
    return redirect('show_members')

#show all penalty

def penalty_list(request):
    return_books = ReturnBook.objects.select_related('member', 'issue__book').all()
    context = {'return_books': return_books}
    return render(request, 'penalty_list.html', context)

