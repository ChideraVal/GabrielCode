from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from .models import Loan, LoanPayment, Repayment, Disbursement
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from .forms import CustomAuthForm, CustomUserCreationForm, CustomUserChangeForm, CustomPasswordChangeForm, LoanForm, LoanPaymentForm, RepaymentForm, DisbursementForm
@login_required
def repayment_portal(request, loan_id):
    loan = Loan.objects.get(id=loan_id)
    if request.method == 'POST':
        form = RepaymentForm(data=request.POST)
        if form.is_valid():
            form.save(loan=loan, user=request.user)
            return redirect(f'/loanpayments/{loan.id}/')
        else:
            return render(request, 'repayment.html', {'form': form, 'loan': loan})
    form = RepaymentForm()
    return render(request, 'repayment.html', {'form': form, 'loan': loan})


# Only staff/admin should access this view in a real app
@login_required
def disbursement_portal(request, loan_id):
    loan = Loan.objects.get(id=loan_id)
    if not loan.is_approved():
        return HttpResponse('<h1>Disbursement cannot be made since loan has not been approved!</h1>')
    if request.method == 'POST':
        form = DisbursementForm(data=request.POST)
        if form.is_valid():
            disbursement = form.save(loan=loan, user=request.user)
            disbursement.status = 'Completed'
            disbursement.save()
            return redirect('/')
        else:
            return render(request, 'disbursement.html', {'form': form, 'loan': loan})
    form = DisbursementForm()
    return render(request, 'disbursement.html', {'form': form, 'loan': loan})
import logging
from django.core.mail import get_connection, EmailMessage
from django.conf import settings
from django.template.loader import render_to_string


logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s: %(message)s'
)

@login_required
def home(request):
    loans = Loan.objects.filter(owner=request.user).all()
    return render(request, 'home.html', {'loans': loans, 'total': sum([i.amount_with_tax() for i in loans])})

@login_required
def loan_payment_details(request, id):
    loan = Loan.objects.get(id=id)
    paid_balance = float(sum([payment.amount for payment in loan.loanpayment_set.filter(approval_status='Approved').all()]))
    rem_balance = loan.amount_with_tax() - paid_balance
    return render(request, 'payments.html', {'loan': loan, 'rem': rem_balance, 'paid': paid_balance})

@login_required
def request_loan(request):
    if request.method == 'POST':
        form = LoanForm(data=request.POST)
        if form.is_valid():
            new_loan = form.save(owner=request.user)
            return redirect('/')
        else:
            print(form.errors)
            return render(request, 'editprofile.html', {'form': form})
    form = LoanForm()
    return render(request, 'requestloan.html', {'form': form})

@login_required
def make_payment(request, id):
    loan = Loan.objects.get(id=id)
    if loan.approval_status != 'Approved':
        return HttpResponse('<h1>Payment cannot be made since loan has not been approved!</h1>')
    if request.method == 'POST':
        form = LoanPaymentForm(data=request.POST)
        paid_balance = float(sum([payment.amount for payment in loan.loanpayment_set.filter(approval_status='Approved').all()]))
        rem_balance = loan.amount_with_tax() - paid_balance
        if int(form.data['amount']) > rem_balance:
            return HttpResponse(f'<h1>Over payment! Payment cannot be greater than ₦{rem_balance}.</h1>')
        if form.is_valid():
            # Save the payment but do not redirect to loanpayments yet
            payment = form.save(loan=loan)
            # Show institution account details page
            amount = form.cleaned_data['amount']
            return render(request, 'institution_account.html', {'amount': amount, 'loan': loan})
        else:
            print(form.errors)
            return render(request, 'makepayment.html', {'form': form, 'loan': loan})
    form = LoanPaymentForm()
    return render(request, 'makepayment.html', {'form': form, 'loan': loan})

def sign_in(request):
    path = request.get_full_path()
    next_url = path.replace('/signin/?next=', '')
    logging.info(f'PATH = {path}')
    logging.info(f'NEXT = {next_url}')
    print(f"COOKIES: {request.COOKIES}")

    if request.method == 'POST':
        form = CustomAuthForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if next_url == '/signin/':
                return redirect('/')
            return redirect(next_url)
        else:
            print(form.errors)
            return render(request, 'signin.html', {'form': form, 'path': path})
    form = CustomAuthForm(request)
    return render(request, 'signin.html', {'form': form, 'path': path})

def sign_up(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            
        # Send email
            connection = get_connection()
            subject = 'Account Created Successfully!'
            html_content = render_to_string('subscribemail.html', {'name': user.username})
            from_email = settings.DEFAULT_FROM_EMAIL
            msg = EmailMessage(subject, html_content, from_email, [user.email], connection=connection)
            msg.content_subtype = "html"
            msg.send()
            return redirect('/signin/')
        else:
            print(form.errors)
            return render(request, 'signup.html', {'form': form})
    form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(instance=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
        else:
            print(form.errors)
            return render(request, 'editprofile.html', {'form': form})
    form = CustomUserChangeForm(instance=request.user)
    return render(request, 'editprofile.html', {'form': form})

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('/')
        else:
            print(form.errors)
            return render(request, 'changepassword.html', {'form': form})
    form = PasswordChangeForm(user=request.user)
    return render(request, 'changepassword.html', {'form': form})

def sign_out(request):
    logout(request)
    return redirect('/signin/')
