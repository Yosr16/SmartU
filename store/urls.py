from django.urls import path

from . import views

urlpatterns = [
	#Leave as empty string for base url
    path('store/', views.store, name='store'),
	path('cart/', views.cart, name="cart"),
	path('checkout/', views.checkout, name="checkout"),
    path('confirmation/', views.confirmation_page, name='confirmation_page'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),

	path('update_item/', views.updateItem, name="update_item"),
	path('process_order/', views.processOrder, name="process_order"),

]