from django import forms
from PublisherApp.models import Doctor, Tutor
from .models import Payment


class UserRegistrationForm(forms.Form):
    doctor = forms.ModelChoiceField(queryset=Doctor.objects.all(), required=False)
    tutor = forms.ModelChoiceField(queryset=Tutor.objects.all(), required=False)


class UPITransactionForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['order_id', 'upi_transaction_id', 'upi_payment_reference', 'payment_status']

    order_id = forms.CharField(max_length=100, required=True)
    upi_transaction_id = forms.CharField(max_length=255, required=False)
    upi_payment_reference = forms.CharField(max_length=255, required=False)
    payment_status = forms.ChoiceField(
        choices=[('Pending', 'Pending'), ('Completed', 'Completed'), ('Failed', 'Failed')],
        initial='Pending',
        required=True
    )

    def clean_order_id(self):
        order_id = self.cleaned_data.get('order_id')
        # You can add a custom validation for the order_id if necessary.
        return order_id
