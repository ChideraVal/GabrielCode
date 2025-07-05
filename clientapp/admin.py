from django.contrib import admin
from .models import Loan, LoanPayment


class LoanAdmin(admin.ModelAdmin):
    list_display = ['id', 'amount', 'duration', 'approval_status', 'payment_status', 'create_time']


# class StaffAdmin(admin.ModelAdmin):
#     list_display = ['id', 'name', 'email', 'department', 'created_at']


# class StaffFileAdmin(admin.ModelAdmin):
#     list_display = ['id', 'file_name', 'uploaded_at']

class LoanPaymentAdmin(admin.ModelAdmin):
    list_display = ['id', 'amount', 'approval_status', 'create_time']

admin.site.site_header = 'Admin Dashboard'
admin.site.site_title = 'Admin Dashboard'


admin.site.register(Loan, LoanAdmin)
admin.site.register(LoanPayment, LoanPaymentAdmin)
