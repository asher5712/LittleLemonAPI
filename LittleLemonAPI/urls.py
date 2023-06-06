from django.urls import path
from . import views

urlpatterns = [
    # path for handling menuitems
    path('menu-items', views.MenuItemsView.as_view(), name='menu-items'),
    
    # path for handling single menuitem
    path('menu-items/<int:pk>', views.SingleMenuItem.as_view(), name='single-item'),
    
    # # path for handling item categories
    path('categories', views.CategoriesView.as_view(), name='categories'),
    
    # # path for handling single category
    path('categories/<int:pk>', views.SingleCategoryView.as_view(), name='single-category'),
    
    # path for handling manager users
    path('groups/manager/users', views.ManagerView.as_view(), name='managers'),
    
    # path for handling single manager user
    path('groups/manager/users/<int:pk>', views.SingleManagerView.as_view(), name='single-manager'),
    
    # path for handling delivery crew users
    path('groups/delivery-crew/users', views.DeliveryCrewView.as_view(), name='delivery-crew'),
    
    # path for handling single delivery drew user
    path('groups/delivery-crew/users/<int:pk>', views.SingleDeliveryCrewView.as_view(), name='single-delivery-crew'),
    
    # path for handling cartitems
    path('cart/menu-items', views.CartView.as_view(), name='cart'),
    
    # path for handling orderitems
    path('orders', views.OrderItemView.as_view(), name='order-item'),
    
    # path for handling single orderitem
    path('orders/<int:pk>', views.SingleOrderItemView.as_view(), name='single-order'),
]