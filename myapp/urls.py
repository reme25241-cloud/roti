# users/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', base, name='base'),
    path('about/', about, name='about'),
    
    path('signup/', signup_view, name='signup'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    
    path('profile/', login_required(profile_view), name='profile'),
    path('profile/edit/', edit_profile, name='edit_profile'),
    
    path('password/', auth_views.PasswordChangeView.as_view(template_name='registration/change_password.html', success_url='/dashboard/'), name='change_password'),

    # Reset password
    path('reset-password/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset_form.html'), name='password_reset'),
    path('reset-password/done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
    path('reset-password-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset-password-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),
    

    path('dashboard/', dashboard, name='dashboard'),
    path('messages/', user_list_view, name='user_list'),
    path('messages/<int:user_id>/', chat_view_by_id, name='chat'),
    
    path('feedback/', feedback_view, name='feedback'),
    path('feedbacks/', view_feedbacks, name='view_feedbacks'),

    # prediction # mainApplicationFunctionality20240625
    path('product_list/', product_list, name='product_list'),
    path('product/<int:pk>/', product_detail, name='product_detail'),
    path('product/add/', product_create, name='product_create'),
    path('product/<int:pk>/edit/', product_edit, name='product_edit'),
    
    path('wishlist/', wishlist_view, name='wishlist'),
    path('wishlist/add/<int:product_id>/', add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/remove/<int:product_id>/', remove_from_wishlist, name='remove_from_wishlist'),
    
    path('wishlist/toggle/<int:product_id>/', toggle_wishlist, name='toggle_wishlist'),

    path('cart/', cart_view, name='cart'),
    path('cart/add/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:cart_id>/', remove_from_cart, name='remove_from_cart'),
    path('checkout/', checkout, name='checkout'),
    
    path('cart/proceed-payment/', proceed_payment, name='proceed_payment'),


    path('purchase-requests/', purchase_requests, name='purchase_requests'),
    

    path('purchase/confirm/<int:request_id>/', confirm_purchase, name='confirm_purchase'),
    
    path('my_pending_purchases/', my_pending_purchases, name='my_pending_purchases'),

    path('bought-history/', bought_history, name='bought_history'),
    path('return-product/<int:product_id>/', return_product, name='return_product'),
    
    path('purchases/', purchase_history, name='purchase_history'),
    path('sales/', sales_history, name='sales_history'),
    
    path('terms/', terms_and_conditions, name='terms_and_conditions'),
    
] 
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)