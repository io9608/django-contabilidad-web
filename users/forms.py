from django import forms
from .models import Investment, Partner
from .models import ProductPurchase

class ProductForm(forms.ModelForm):
    class Meta:
        model = ProductPurchase
        fields = ['product_name', 'cost_per_unit', 'amount', 'weight']

class InvestmentForm(forms.ModelForm):
    class Meta:
        model = Investment
        fields = ['initial_amount', 'profit_percentage', 'notes']

class PartnerForm(forms.ModelForm):
    class Meta:
        model = Partner
        fields = ['name', 'amount', 'profit_share']

# Formset for multiple partners
PartnerFormSet = forms.inlineformset_factory(
    Investment, Partner, form=PartnerForm, extra=1, can_delete=True
)
