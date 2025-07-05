from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from datetime import datetime as dt

days = (
    (i, f'{i} days') for i in range(1, 101)
)

a_status = (
    ('Approved',) * 2,
    ('Pending',) * 2, 
    ('Rejected',) * 2
)

p_status = (
    ('Paid',) * 2,
    ('Unpaid',) * 2,
)

e_status = (
    (('Student',) * 2),
    (('Employed',) * 2),
    (('Self Employed',) * 2)
)

class Loan(models.Model):
    amount = models.DecimalField(decimal_places=2, max_digits=8, null=False, blank=False)
    create_time = models.DateTimeField(default=timezone.now)
    duration = models.IntegerField(choices=days)
    approval_status = models.TextField(choices=a_status, default=a_status[1][1])
    payment_status = models.TextField(choices=p_status, default=p_status[1][1])
    purpose = models.TextField(max_length=4000, null=True, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    employment_status = models.CharField(max_length=14, null=True, choices=e_status, default=e_status[1][1])
    monthly_income = models.IntegerField(null=True, blank=False)
    source_of_income = models.CharField(max_length=200, null=True, blank=False)

    def __str__(self):
        return str(self.amount)

    def is_approved(self):
        return self.approval_status == 'Approved'

    def is_paid(self):
        return self.payment_status == 'Paid'
    
    def rem_time(self):
        return (timezone.now() - self.create_time).days
    
    def amount_with_tax(self):
        return int(self.amount) + ((5/100) * int(self.amount))


class LoanPayment(models.Model):
    amount = models.DecimalField(decimal_places=2, max_digits=8, null=False, blank=False)
    create_time = models.DateTimeField(default=timezone.now)
    approval_status = models.TextField(choices=a_status, default=a_status[1][1])
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.amount)

    def is_approved(self):
        return self.approval_status == 'Approved'
