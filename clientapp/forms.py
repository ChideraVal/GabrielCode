from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth.models import User
from .models import Loan, LoanPayment, Repayment, Disbursement
from django import forms

class CustomAuthForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)
        self.fields["username"].widget.attrs['autocomplete'] = 'off'


class CustomUserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)
        self.fields["username"].widget.attrs['autocomplete'] = 'off'
        self.fields["first_name"].widget.attrs['autocomplete'] = 'off'
        self.fields["last_name"].widget.attrs['autocomplete'] = 'off'
        self.fields["email"].widget.attrs['autocomplete'] = 'off'
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'autocomplete': 'off'})
        }


class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)
        # self.fields["username"].widget.attrs['autocomplete'] = 'off'
    
    # class Meta:
    #     model = User
    #     fields = ['username', 'first_name', 'last_name', 'email']


class LoanForm(forms.ModelForm):
    class Meta:
        model = Loan
        exclude = ['owner', 'approval_status', 'payment_status', 'create_time']
        labels = {
            'amount': 'Amount (₦)',
            'monthly_income': 'Monthly Income (₦)',
            'source_of_income': 'Source of Income (if employed)',
            'bvn': 'BVN',
            'employer_name': 'Employer Name',
            'means_of_id': 'Means of ID',
            'marital_status': 'Marital Status',
            'gender': 'Gender',
            'membership_id': 'Membership ID',
            'guarantor_name': 'Guarantor Name',
            'guarantor_contact': 'Guarantor Contact',
            'agreement_confirmed': 'I confirm that all information provided is accurate.'
        }

    agreement_confirmed = forms.BooleanField(
        label="I confirm that all information provided is accurate.",
        required=True
    )

    def save(self, owner, commit=False):
        self.instance.owner = owner
        self.instance.save()
        return super().save(commit)


class LoanPaymentForm(forms.ModelForm):
    class Meta:
        model = LoanPayment
        exclude = ['loan', 'approval_status', 'create_time']
    
        labels = {
            'amount': 'Amount to Pay (₦)',
        }

    def save(self, loan, commit = False):
        self.instance.loan = loan
        self.instance.save()
        return super().save(commit)


# Repayment Form
class RepaymentForm(forms.ModelForm):
    class Meta:
        model = Repayment
        exclude = ['loan', 'user', 'date']
        labels = {
            'amount': 'Repayment Amount (₦)',
        }

    def save(self, loan, user, commit=False):
        self.instance.loan = loan
        self.instance.user = user
        self.instance.save()
        return super().save(commit)


# Disbursement Form
class DisbursementForm(forms.ModelForm):
    class Meta:
        model = Disbursement
        exclude = ['loan', 'user', 'date', 'status']
        labels = {
            'amount': 'Disbursement Amount (₦)',
            'bank_name': 'Bank Name',
            'account_number': 'Account Number',
            'account_name': 'Account Name',
        }

    def save(self, loan, user, commit=False):
        self.instance.loan = loan
        self.instance.user = user
        self.instance.save()
        return super().save(commit)
