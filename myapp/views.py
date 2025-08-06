# users/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required

from django.db.models import Q
from django.conf import settings

from django.contrib.auth import get_user_model

from .forms import *
from .models import *

def base(request):
    query = request.GET.get('q')
    category_id = request.GET.get('category')
    products = Product.objects.all()
    categories = Category.objects.all()

    if query:
        products = products.filter(Q(title__icontains=query) | Q(description__icontains=query))
    if category_id:
        products = products.filter(category__id=category_id)

    return render(request, 'base.html', {'products': products, 'categories': categories})

from django.contrib.auth import get_user_model
from .models import Message

CustomUser = get_user_model()

from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from .forms import UserSignupForm  # Make sure this matches your form name

# def signup_view(request):
#     if request.method == 'POST':
#         form = UserSignupForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             login(request, user)
#             messages.success(request, "Signup successful. Welcome!")
#             return redirect('dashboard')  # Change as per your URL name
#         else:
#             messages.error(request, "Please correct the errors below.")
#     else:
#         form = UserSignupForm()

#     return render(request, 'registration/signup.html', {'form': form})

# views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from .forms import UserSignupForm

def signup_view(request):
    if request.method == 'POST':
        form = UserSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Automatically log in after signup
            messages.success(request, "Signup successful. Welcome!")
            return redirect('base')  
    else:
        form = UserSignupForm()
    return render(request, 'registration/signup.html', {'form': form})


# views.py
from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserSignupForm

def signup_view(request):
    if request.method == 'POST':
        form = UserSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Signup successful. Welcome!")
            return redirect('dashboard')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = UserSignupForm()

    return render(request, 'registration/signup.html', {'form': form})

# Handle user logout
def logout_view(request):
    logout(request)
    return redirect('login')

# profile
@login_required
def profile_view(request):
    return render(request, 'account/profile.html', {'user': request.user})

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm

@login_required
def edit_profile_view(request):
    if request.method == 'POST':
        form = EditUserForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = EditUserForm(instance=request.user)
    
    return render(request, 'account/edit_profile.html', {'form': form})


# dashboard
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Avg
from django.shortcuts import render


def about(request):
    return render(request, 'about/about.html')

# chat
@login_required
def user_list_view(request):
    users = get_user_model().objects.exclude(id=request.user.id)  
    return render(request, 'users/user_list.html', {'users': users})


@login_required
def chat_view_by_id(request, user_id):
    other_user = get_object_or_404(CustomUser, id=user_id)
    messages = Message.objects.filter(
        (Q(sender=request.user) & Q(receiver=other_user)) |
        (Q(sender=other_user) & Q(receiver=request.user))
    ).order_by('timestamp')

    if request.method == 'POST':
        text = request.POST.get('text')
        image = request.FILES.get('image')
        Message.objects.create(sender=request.user, receiver=other_user, text=text, image=image)
        return redirect('chat', user_id=other_user.id)  # ✅ Corrected: use user_id instead of username

    return render(request, 'users/chat.html', {
        'messages': messages,
        'receiver': other_user
    })

# Feedback

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import FeedbackForm
from .models import Feedback

@login_required
def feedback_view(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.user = request.user
            feedback.save()
            return render(request, 'feedback/feedback_thanks.html')  # Create this template
    else:
        form = FeedbackForm()
    return render(request, 'feedback/feedback.html', {'form': form})

@login_required
def view_feedbacks(request):
    if request.user.is_superuser:
        feedbacks = Feedback.objects.all().order_by('-created_at')
        return render(request, 'feedback/view_feedbacks.html', {'feedbacks': feedbacks})
    else:
        return redirect('dashboard')


# product List


@login_required
def dashboard(request):
    query = request.GET.get('q')
    category_id = request.GET.get('category')
    products = Product.objects.all()
    categories = Category.objects.all()

    if query:
        products = products.filter(Q(title__icontains=query) | Q(description__icontains=query))
    if category_id:
        products = products.filter(category__id=category_id)

    return render(request, 'dashboard/dashboard.html', {'products': products, 'categories': categories})



# mainApplicationFunctionality20240625
# myapp/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import *
from .forms import *

# ----------------------------
# PRODUCT VIEWS
# ----------------------------
@login_required
def product_list(request):
    query = request.GET.get('q')
    category_id = request.GET.get('category')
    products = Product.objects.all()
    categories = Category.objects.all()

    if query:
        products = products.filter(Q(title__icontains=query) | Q(description__icontains=query))
    if category_id:
        products = products.filter(category__id=category_id)

    return render(request, 'product/product_list.html', {'products': products, 'categories': categories})

@login_required
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    is_in_wishlist = Wishlist.objects.filter(user=request.user, product=product).exists()
    review_form = ReviewForm()
    return render(request, 'product/product_detail.html', {
        'product': product,
        'review_form': review_form,
        'is_in_wishlist': is_in_wishlist,
    })

@login_required
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.user = request.user  
            product.save()
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'product/product_form.html', {'form': form})

@login_required
def product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_detail', pk=pk)
    else:
        form = ProductForm(instance=product)
    return render(request, 'product/product_form.html', {'form': form})


# ----------------------------
# WISHLIST VIEWS
# ----------------------------
@login_required
def toggle_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist_item, created = Wishlist.objects.get_or_create(user=request.user, product=product)
    if not created:
        wishlist_item.delete()  # It existed, so remove it
    return redirect('product_detail', pk=product_id)


@login_required
def wishlist_view(request):
    wishlist = Wishlist.objects.filter(user=request.user)
    return render(request, 'wishlist/wishlist.html', {'wishlist': wishlist})

@login_required
def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    Wishlist.objects.get_or_create(user=request.user, product=product)
    return redirect('wishlist')

@login_required
def remove_from_wishlist(request, product_id):
    Wishlist.objects.filter(user=request.user, product__id=product_id).delete()
    return redirect('wishlist')


# ----------------------------
# CART VIEWS
# ----------------------------
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Cart

@login_required
def cart_view(request):
    cart_items = Cart.objects.filter(user=request.user, payment_proceeded=False)
    cart = cart_items.first() if cart_items.exists() else None

    # Calculate totals
    total_amount = sum(item.product.cost * item.quantity for item in cart_items)
    total_items = sum(item.quantity for item in cart_items)

    context = {
        'cart_items': cart_items,
        'cart': cart,
        'total_amount': total_amount,
        'total_items': total_items,
    }

    return render(request, 'cart/cart.html', context)



from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Product, Cart

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        try:
            quantity = int(request.POST.get('quantity', 1))
        except (TypeError, ValueError):
            quantity = 1

        # Check if item already exists in cart
        cart_item, created = Cart.objects.get_or_create(
            user=request.user,
            product=product,
            payment_proceeded=False,
            defaults={'quantity': quantity}
        )
        
        if not created:
            # If it already exists, increase the quantity
            cart_item.quantity += quantity
            cart_item.save()

    return redirect('cart')  # Redirect to cart page



@login_required
def remove_from_cart(request, cart_id):
    Cart.objects.filter(id=cart_id, user=request.user).delete()
    return redirect('cart')


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Cart, Product, PendingPurchaseRequest
from django.contrib.auth.models import User
from .models import Cart, PendingPurchaseRequest, ManualPaymentInfo
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

@login_required
def proceed_payment(request):
    cart_items = Cart.objects.filter(user=request.user, payment_proceeded=False)
    if not cart_items.exists():
        return redirect('cart')

    user_profile = request.user.profile
    seller_profile = cart_items.first().product.user.profile  # Assuming same seller for all items
    seller_qr = seller_profile.qr_code_image.url if seller_profile.qr_code_image else None
    user_qr = user_profile.qr_code_image.url if user_profile.qr_code_image else None

    if request.method == "POST":
        # Case 1: QR payment
        if seller_qr and user_qr:
            for item in cart_items:
                PendingPurchaseRequest.objects.create(user=request.user, cart=item, payment_proceeded=True)
                item.payment_proceeded = True
                item.product.is_sold = True  # Assuming there's an is_sold field
                item.product.save()
                item.save()
            return redirect('cart')

        # Case 2: Manual payment
        else:
            ManualPaymentInfo.objects.create(
                user=request.user,
                card_number=request.POST.get('card_number'),
                cvv=request.POST.get('cvv'),
                expiry=request.POST.get('expiry'),
                address=request.POST.get('address'),
                phone=request.POST.get('phone')
            )
            for item in cart_items:
                PendingPurchaseRequest.objects.create(user=request.user, cart=item, payment_proceeded=True)
                item.payment_proceeded = True
                item.product.is_sold = True
                item.product.save()
                item.save()
            return redirect('cart')

    return render(request, 'cart/proceed_payment.html', {
        'cart_items': cart_items,
        'seller_qr': seller_qr,
        'user_qr': user_qr
    })

# ----------------------------
# CHECKOUT & PURCHASE REQUESTS
# ----------------------------


# @login_required
# def checkout(request):
#     cart_items = Cart.objects.filter(user=request.user)
#     for item in cart_items:
#         PendingPurchaseRequest.objects.create(buyer=request.user, product=item.product, status='Pending')
#     cart_items.delete()
#     return redirect('purchase_requests')

from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from .models import Cart, PendingPurchaseRequest

@login_required
def checkout(request):
    cart_items = Cart.objects.filter(user=request.user)
    order_details = []
    
    for item in cart_items:
        purchase = PendingPurchaseRequest.objects.create(
            buyer=request.user,
            product=item.product,
            status='Pending',
            payment_proceeded=False,
            seller_confirmed=False,
            buyer_received=False,
            cart_id=item.id,
            user_id=request.user.id
        )
        order_details.append(f"- {item.product.name} (₹{item.product.price})")

    if order_details:
        subject = "RotiApp Order Confirmation"
        message = (
            f"Dear {request.user.username},\n\n"
            f"Thank you for your order! The following items have been placed for purchase:\n"
            f"{chr(10).join(order_details)}\n\n"
            "We will notify you once the seller confirms your request.\n\n"
            "Regards,\nRotiApp Team"
        )

        admin_subject = f"New Order Placed by {request.user.username}"
        admin_message = (
            f"A new order has been placed by {request.user.username} ({request.user.email}).\n\n"
            f"Order Details:\n{chr(10).join(order_details)}\n\n"
            "Check the admin panel to manage the request."
        )

        admin_emails = list(User.objects.filter(is_superuser=True).values_list('email', flat=True))

        # Send to user
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [request.user.email])

        # Send to admin(s)
        if admin_emails:
            send_mail(admin_subject, admin_message, settings.DEFAULT_FROM_EMAIL, admin_emails)


    cart_items.delete()
    return redirect('purchase_requests')


from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import PendingPurchaseRequest

@login_required
def purchase_requests(request):
    user = request.user
    purchase_requests = PendingPurchaseRequest.objects.filter(
        Q(user=user) | Q(cart__product__user=user)
    ).distinct()

    return render(request, 'purchase/purchase_requests.html', {
        'purchase_requests': purchase_requests
    })


from django.contrib.auth.decorators import login_required

from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import PendingPurchaseRequest, Product, Cart
# @login_required
# def confirm_purchase(request, request_id):
#     purchase_request = get_object_or_404(PendingPurchaseRequest, id=request_id)

#     # Only seller can confirm
#     if purchase_request.cart.product.user != request.user:
#         messages.error(request, "You are not authorized to confirm this purchase.")
#         return redirect('purchase_requests')

#     if not purchase_request.payment_proceeded:
#         messages.warning(request, "Payment has not been made yet.")
#         return redirect('purchase_requests')

#     # Confirm the seller part
#     purchase_request.seller_confirmed = True
#     purchase_request.save()

#     # Mark product as sold
#     product = purchase_request.cart.product
#     product.is_sold = True
#     product.save()

#     # Save to BoughtProduct list
#     BoughtProduct.objects.create(buyer=purchase_request.user, product=product)

#     # Remove cart entry
#     purchase_request.cart.delete()

#     messages.success(request, "Purchase confirmed. Product marked as sold.")
#     return redirect('purchase_requests')


from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .models import PendingPurchaseRequest, BoughtProduct
from django.core.mail import send_mail
from django.conf import settings

@login_required
def confirm_purchase(request, request_id):
    purchase_request = get_object_or_404(PendingPurchaseRequest, id=request_id)

    # Ensure only the seller can confirm
    if purchase_request.cart.product.user != request.user:
        messages.error(request, "You are not authorized to confirm this purchase.")
        return redirect('purchase_requests')

    if not purchase_request.payment_proceeded:
        messages.warning(request, "Payment has not been made yet.")
        return redirect('purchase_requests')

    # Mark seller confirmation
    purchase_request.seller_confirmed = True
    purchase_request.save()

    # Mark product as sold
    product = purchase_request.cart.product
    product.is_sold = True
    product.save()

    # Create BoughtProduct record
    BoughtProduct.objects.create(
        buyer=purchase_request.user,
        seller=product.user,
        product=product,
        quantity=purchase_request.cart.quantity,
        price_per_item=product.cost,
        total_price=product.cost * purchase_request.cart.quantity,
        is_returned=False,
    )

    # Remove cart entry
    purchase_request.cart.delete()

    # ✅ Send confirmation email to buyer
    buyer_email = purchase_request.user.email
    send_mail(
        subject='Your Purchase Has Been Confirmed 🎉',
        message=f'Dear {purchase_request.user.username},\n\n'
                f'Thank you for your purchase of "{product.title}".\n'
                f'The seller has confirmed the order and the product is now marked as sold.\n\n'
                f'Product: {product.title}\n'
                f'Quantity: {purchase_request.cart.quantity}\n'
                f'Total Amount: ₹{product.cost * purchase_request.cart.quantity}\n\n'
                f'Thank you for using CampusSwap!',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[buyer_email],
        fail_silently=False,
    )

    messages.success(request, "Purchase confirmed and buyer notified via email.")
    return redirect('purchase_requests')

# ----------------------------
# RETURN PRODUCT
# ----------------------------
@login_required
def return_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    # Check if this user actually bought the product
    if not BoughtProduct.objects.filter(product=product, buyer=request.user).exists():
        messages.error(request, "You can only return products you have purchased.")
        return redirect('bought_history')

    if request.method == 'POST':
        form = ReturnForm(request.POST, request.FILES)
        if form.is_valid():
            return_obj = form.save(commit=False)
            return_obj.product = product
            return_obj.user = request.user
            return_obj.save()
            messages.success(request, "Return request submitted successfully.")
            return redirect('bought_history')
    else:
        form = ReturnForm()
    return render(request, 'return/return_form.html', {'form': form, 'product': product})


@login_required
def bought_history(request):
    bought_products = BoughtProduct.objects.filter(buyer=request.user).select_related('product')
    return render(request, 'purchase/bought_history.html', {'bought_products': bought_products})


# views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import PendingPurchaseRequest

@login_required
def my_pending_purchases(request):
    pending_requests = PendingPurchaseRequest.objects.filter(
        user=request.user,
        payment_proceeded=True,
        seller_confirmed=False
    )
    return render(request, 'purchase/my_pending_purchases.html', {'pending_requests': pending_requests})

from django.contrib.auth.decorators import login_required
from .models import BoughtProduct

@login_required
def purchase_history(request):
    purchases = BoughtProduct.objects.filter(buyer=request.user).order_by('-purchased_at')
    return render(request, 'purchase/purchase_history.html', {'purchases': purchases})

@login_required
def sales_history(request):
    sales = BoughtProduct.objects.filter(seller=request.user).order_by('-purchased_at')
    return render(request, 'purchase/sales_history.html', {'sales': sales})

from django.shortcuts import render

def terms_and_conditions(request):
    return render(request, 'terms/terms.html')
