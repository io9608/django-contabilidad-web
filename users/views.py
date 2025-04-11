from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from .forms import InvestmentForm, PartnerFormSet
from django.db.models import Sum
from .models import Investment, Partner
from .models import ProductPurchase
from .forms import ProductForm

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

def dashboard_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    # Investment calculations
    investments = Investment.objects.filter(user=request.user)
    total_initial = investments.aggregate(Sum('initial_amount'))['initial_amount__sum'] or 0
    
    partners = Partner.objects.filter(investment__user=request.user)
    total_partner_investment = partners.aggregate(Sum('amount'))['amount__sum'] or 0
    total_investment = total_initial + total_partner_investment
    profit_percentage = 10  # This should come from user input
    total_profit = total_investment * (profit_percentage / 100)

    # Product stock calculations
    product_stock = (
        ProductPurchase.objects.filter(user=request.user)
        .values('product_name')
        .annotate(
            total_amount=Sum('amount'),
            total_cost=Sum('total_cost')
        )
    )

    context = {
        'total_initial': total_initial,
        'total_partner_investment': total_partner_investment,
        'total_investment': total_investment,
        'total_profit': total_profit,
        'partners': partners,
        'product_stock': product_stock,  # Make sure this is included
    }
    return render(request, 'dashboard.html', context)

def logout_view(request):
    logout(request)
    return redirect('login')
def settings_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, 'settings.html')


def investments_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    if request.method == 'POST':
        investment_form = InvestmentForm(request.POST)
        partner_formset = PartnerFormSet(request.POST, prefix='partners')
        
        if investment_form.is_valid() and partner_formset.is_valid():
            investment = investment_form.save(commit=False)
            investment.user = request.user
            investment.save()
            
            # Save partners linked to the investment
            partner_formset.instance = investment
            partner_formset.save()
            
            return redirect('dashboard')
    else:
        investment_form = InvestmentForm()
        partner_formset = PartnerFormSet(prefix='partners')

    return render(request, 'investments.html', {
        'investment_form': investment_form,
        'partner_formset': partner_formset,
    })

from django.shortcuts import get_object_or_404

def delete_partner(request, partner_id):
    partner = get_object_or_404(Partner, id=partner_id, investment__user=request.user)
    partner.delete()
    return redirect('dashboard')

def products_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.user = request.user
            product.save()
            return redirect('products')
    else:
        form = ProductForm()

    # Group purchases by date
    purchases = ProductPurchase.objects.filter(user=request.user).order_by('-date_added')
    grouped_purchases = {}
    for purchase in purchases:
        date_str = purchase.date_added.strftime("%Y-%m-%d")
        if date_str not in grouped_purchases:
            grouped_purchases[date_str] = []
        grouped_purchases[date_str].append(purchase)

    return render(request, 'products.html', {
        'form': form,
        'grouped_purchases': grouped_purchases,
    })

def delete_product(request, product_id):
    product = get_object_or_404(ProductPurchase, id=product_id, user=request.user)
    product.delete()
    return redirect('products')


