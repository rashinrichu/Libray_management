from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Member(models.Model):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    address = models.CharField(max_length=200)
    phone_number = models.IntegerField(max_length=20)
    image = models.ImageField(upload_to='member_images/', blank=True)
    dob = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Category(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.name



class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    available_copies = models.PositiveIntegerField()
    language = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    year_of_publish = models.PositiveIntegerField()
    image = models.ImageField(upload_to='book_images/', blank=True, null=True)

    def __str__(self):
        return self.title
    
    
    # ...


class RequestBook(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    request_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.member} - {self.book.title}"


class CancelledBook(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    request = models.ForeignKey(RequestBook, on_delete=models.CASCADE)
    cancel_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.member.user.get_full_name()} - {self.book.title} - {self.cancel_date.date()}"

class IssueBook(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    issue_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField()
    return_date = models.DateTimeField(null=True, blank=True)
    

    def __str__(self):
        return f"{self.member.user.get_full_name()} - {self.book.title}"



class ReturnBook(models.Model):
    issue = models.ForeignKey(IssueBook, on_delete=models.CASCADE)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    return_date = models.DateTimeField(auto_now_add=True)
    fine_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def save(self, *args, **kwargs):
        # Calculate fine amount based on due date and return date
        if self.issue.due_date and self.return_date:
            overdue_days = (self.return_date - self.issue.due_date).days
            if overdue_days > 0:
                fine_amount = overdue_days * 10  # 10 Rs per day overdue fine
                self.fine_amount = fine_amount
        
        super(ReturnBook, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.member.user.get_full_name()} - {self.issue.book.title}"

class Penalty(models.Model):
    issue = models.ForeignKey(IssueBook, on_delete=models.CASCADE)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    issue_date = models.DateField()
    expiry_date = models.DateField()
    return_date = models.DateField(auto_now_add=True)
    over_due = models.IntegerField()
    penalty = models.IntegerField()
    reason = models.CharField(max_length=50)
    total = models.IntegerField()



    def __str__(self):
        return f"{self.member.user.get_full_name()} - {self.book.title}"


class Review(models.Model):
    RATING_CHOICES = [
        (0.5, '0.5 stars'),
        (1.0, '1 star'),
        (1.5, '1.5 stars'),
        (2.0, '2 stars'),
        (2.5, '2.5 stars'),
        (3.0, '3 stars'),
        (3.5, '3.5 stars'),
        (4.0, '4 stars'),
        (4.5, '4.5 stars'),
        (5.0, '5 stars'),
    ]
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    rating = models.FloatField(choices=RATING_CHOICES)
    comment = models.TextField(blank=True)
    review_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.member.user.get_full_name()} - {self.book.title}"
