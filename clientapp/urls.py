from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('signin/', views.sign_in),
    path('signup/', views.sign_up),
    path('editprofile/', views.edit_profile),
    path('changepassword/', views.change_password),
    path('signout/', views.sign_out),
    path('requestloan/', views.request_loan),
    path('loanpayments/<int:id>/', views.loan_payment_details),
    path('makepayment/<int:id>/', views.make_payment)
    ,
    path('repayment/<int:loan_id>/', views.repayment_portal, name='repayment_portal'),
    path('disbursement/<int:loan_id>/', views.disbursement_portal, name='disbursement_portal'),
]