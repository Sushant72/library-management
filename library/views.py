from django.shortcuts import render, redirect
from .models import Book, Member, Transaction
import requests
from django.http import HttpResponse
from django.contrib import messages
from django.utils import timezone


def home(request):
    return render(request, 'library/home.html')

def book_list(request):
    query = request.GET.get("q")
    if query:
        books = Book.objects.filter(title__icontains=query) | Book.objects.filter(author__icontains=query)
    else:
        books = Book.objects.all()
    return render(request, 'library/book_list.html', {'books': books})

def member_list(request):
    members = Member.objects.all()
    return render(request, 'library/member_list.html', {'members': members})

def issue_book(request):
    if request.method == 'POST':
        member_id = request.POST['member']
        book_id = request.POST['book']
        member = Member.objects.get(id=member_id)
        book = Book.objects.get(id=book_id)

        if member.debt > 500:
            return HttpResponse("Cannot issue, member owes more than ₹500")
        if book.stock <= 0:
            return HttpResponse("Cannot issue, book out of stock")

        book.stock -= 1
        book.save()
        member.debt += 50  # Assume ₹50 rent
        member.save()

        Transaction.objects.create(member=member, book=book, rent_fee=50)
        return redirect('home')

    return render(request, 'library/issue_book.html', {
        'members': Member.objects.all(),
        'books': Book.objects.all()
    })

def return_book(request, transaction_id):
    txn = Transaction.objects.get(id=transaction_id)
    txn.return_date = timezone.now().date()
    txn.save()

    txn.book.stock += 1
    txn.book.save()
    return redirect('home')

def import_books(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        page = request.POST.get('page', 1)
        url = f"https://frappe.io/api/method/frappe-library?page={page}&title={title}"
        try:
            response = requests.get(url)
            response.raise_for_status()  
            data = response.json().get('message', [])

            if not data:
                messages.warning(request, "No books found for that title.")
            else:
                added = 0
                for item in data:
                    _, created = Book.objects.get_or_create(
                        title=item.get('title'),
                        author=item.get('authors'),
                        isbn=item.get('isbn'),
                        publisher=item.get('publisher'),
                        defaults={'stock': 1}
                    )
                    if created:
                        added += 1

                messages.success(request, f"✅ Imported {added} new books successfully.")

        except Exception as e:
            messages.error(request, f"❌ Error importing books: {e}")

        return redirect('import-books')
    return render(request, 'library/import_books.html')

