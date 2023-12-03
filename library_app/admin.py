from django.contrib import admin
from .models import Member, Category, Book, Penalty,  RequestBook, CancelledBook, IssueBook, ReturnBook, Review

admin.site.register(Member)
admin.site.register(Category)
admin.site.register(Book)
admin.site.register(RequestBook)
admin.site.register(CancelledBook)
admin.site.register(IssueBook)
admin.site.register(ReturnBook)
admin.site.register(Penalty)

admin.site.register(Review)
