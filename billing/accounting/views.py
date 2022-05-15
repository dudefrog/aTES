from django.http import HttpRequest
from django.shortcuts import redirect, render

from .models import Transaction


def index_view(request: HttpRequest):
    if request.user.is_anonymous:
        return redirect("/login")

    balance = request.user.balance / 100
    transactions = [
        {
            "sum": (t.amount / 100) * (1 if t.is_credit else -1),
            "date": t.created_at,
            "comment": ("Picked up" if t.is_debit else "Completed")
            + f' task "{t.related_task.title}"',
        }
        for t in Transaction.objects.filter(user=request.user)
    ]
    print(transactions)

    return render(
        request,
        "accounting/index.html",
        {"balance": balance, "transactions": transactions},
    )
