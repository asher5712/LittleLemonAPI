from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User, Group
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import MenuItem, Cart, Order, OrderItem, Category
from .serializers import MenuItemSerializer, UserSerializer, CartSerializer, OrderSerializer, OrderItemSerializer, CategorySerializer
from .permissions import IsManagerUser, IsCustomerUser, IsManagerorCrewUser, isManager, isCrew
from datetime import datetime

# Create your views here.
class CategoriesView(generics.ListCreateAPIView):
    """
    View class for displaying and creating categories.
    Contains 'queryset' and 'serializer_class' attributes for handling the model.    
    """
    
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    
    
    def get_permissions(self):
        """
        Method to provide the permissions for different requests specifically for this specified view

        Returns:
            list: permission list for different requests
        """        
        
        permission_classes = [IsManagerUser]
        if self.request.method == 'GET':
            permission_classes = []
        return [permission() for permission in permission_classes]



class SingleCategoryView(generics.RetrieveUpdateDestroyAPIView):
    """
    View class for showing and managing single menuitem.
    Contains 'queryset' and 'serializer_class' attributes for handling the model
    """    
    
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


    def get_permissions(self):
        """
        Method to provide the permissions for different requests specifically for this specified view

        Returns:
            list: permission list for different requests
        """        
        
        permission_classes = [IsManagerUser]
        if self.request.method == 'GET':
            permission_classes = []
        return [permission() for permission in permission_classes]



class MenuItemsView(generics.ListCreateAPIView):
    """
    View class for displaying and creating menuitems.
    Contains 'queryset' and 'serializer_class' attributes for handling the model.
    Further, ordering, search and filter can be performed here
    """    
    
    queryset = MenuItem.objects.select_related('category').all()
    serializer_class = MenuItemSerializer
    
    
    def get_permissions(self):
        """
        Method to provide the permissions for different requests specifically for this specified view

        Returns:
            list: permission list for different requests
        """        
        
        permission_classes = [IsManagerUser]
        if self.request.method == 'GET':
            permission_classes = []
        return [permission() for permission in permission_classes]


    ordering_fields = ['price', 'featured']
    filterset_fields = ['category__title', 'price', 'featured']
    search_fields = ['title','category__title']
    
    
    
class SingleMenuItem(generics.RetrieveUpdateDestroyAPIView):
    """
    View class for showing and managing single menuitem.
    Contains 'queryset' and 'serializer_class' attributes for handling the model
    """    
    
    queryset = MenuItem.objects.select_related('category').all()
    serializer_class = MenuItemSerializer
    
    
    def get_permissions(self):
        """
        Method to provide the permissions for different requests specifically for this specified view

        Returns:
            list: permission list for different requests
        """        
        
        permission_classes = [IsManagerUser]
        if self.request.method == 'GET':
            permission_classes = []
        return [permission() for permission in permission_classes]



class ManagerView(generics.ListCreateAPIView):
    """
    View class for displaying and generating managers.
    Contains 'queryset' and 'serializer_class' attributes for handling the model.
    Can be used by Manager users only
    """    
    
    queryset = User.objects.filter(groups__name='Manager')
    serializer_class = UserSerializer
    
    permission_classes = [IsManagerUser]
    
    
    def create(self, request, *args, **kwargs):
        """
        Method to make any user a manager user. 
        'username' must be provided to this view from client side to work properly

        Args:
            request (Request): request object from the client side

        Returns:
            Response: response object for the user
        """        
        
        username = request.data.get('username')
        if username: # The section will only work is username is provided from client side
            user = get_object_or_404(User, username=username) # If username not in 'User' model then 404 error generated
            managers = Group.objects.get(name="Manager")
            if not user.groups.contains(managers): # Checking if user is present in manager group
                managers.user_set.add(user)
                serialized_user = UserSerializer(user)
                return Response({'message': 'object added to managers', 'item':serialized_user.data}, status=status.HTTP_201_CREATED)
            else:
                serialized_user = UserSerializer(user)
                return Response({'message': 'object already present in managers', 'item':serialized_user.data}, status=status.HTTP_226_IM_USED)
        return Response({'message':'error occured, cannot add to managers'}, status=status.HTTP_400_BAD_REQUEST)
    
    
    
class SingleManagerView(generics.DestroyAPIView):
    """
    View class for removing any manager.
    Can be used by Manager users only
    """    
    
    queryset = User.objects.filter(groups__name='Manager')
    serializer_class = UserSerializer
        
    permission_classes = [IsManagerUser]
    
    
    def perform_destroy(self, instance):
        """
        Method to remove the manager from Managers group

        Args:
            instance (User): user object for performing action
        """        
        
        managers = Group.objects.get(name="Manager")
        if instance.groups.contains(managers): # Checking if user present in Managers group
            managers.user_set.remove(instance)    

    
    
class DeliveryCrewView(generics.ListCreateAPIView):
    """
    View class for displaying and generating managers.
    Contains 'queryset' and 'serializer_class' attributes for handling the model.
    Can be used by Manager users only
    """    
    
    queryset = User.objects.filter(groups__name='Delivery crew')
    serializer_class = UserSerializer
    
    permission_classes = [IsManagerUser]
    
    
    def create(self, request, *args, **kwargs):
        """
        Method to make any user a delivery crew user. 
        'username' must be provided to this view from client side to work properly

        Args:
            request (Request): request object from the client side

        Returns:
            Response: response object for the user
        """        
        
        username = request.data.get('username')
        if username: # The section will only work is username is provided from client side
            user = get_object_or_404(User, username=username) # If username not in 'User' model then 404 error generated
            crews = Group.objects.get(name="Delivery crew")
            if not user.groups.contains(crews): # Checking if user is present in delivery crew group
                crews.user_set.add(user)
                serialized_user = UserSerializer(user)
                return Response({'message': 'object added to delivery crew', 'item':serialized_user.data}, status=status.HTTP_201_CREATED)
            else:
                serialized_user = UserSerializer(user)
                return Response({'message': 'object already present in delivery crew', 'item':serialized_user.data}, status=status.HTTP_226_IM_USED)
        return Response({'message':'error occured, cannot add to delivery crew'}, status=status.HTTP_400_BAD_REQUEST)
    
    
    
class SingleDeliveryCrewView(generics.DestroyAPIView):
    """
    View class for removing any delivery staff.
    Can be used by Manager users only
    """    

    queryset = User.objects.filter(groups__name='Delivery crew')
    serializer_class = UserSerializer
    
    permission_classes = [IsManagerUser]
    
    
    def perform_destroy(self, instance):
        """
        Method to remove the crew member from Delivery-crews group

        Args:
            instance (User): user object for performing action
        """        
        
        crew = Group.objects.get(name="Delivery crew")
        if instance.groups.contains(crew): # Checking if userpresent in Delivery-crew group
            crew.user_set.remove(instance)
    
    
    
class CartView(generics.ListCreateAPIView, generics.DestroyAPIView):
    """
    View class for displaying, creating and destroying cart items.
    Can be used only by Customers
    """    
    
    serializer_class = CartSerializer
    
    permission_classes = [IsAuthenticated]
    
    
    def get_queryset(self):
        """
        Method for making personalized queryset for all users

        Returns:
            QuerySet[Cart]: query set containing personalized cart objects
        """        
        return Cart.objects.filter(user=self.request.user)
    
    
    def destroy(self, request, *args, **kwargs):
        """
        Method to flush the complete cart

        Args:
            request (Request): request object from the client side

        Returns:
            Response: response object for the client
        """        
        
        items = self.get_queryset()
        deleted = items.delete()
        return Response({'message': 'cart flushed', 'item':deleted}, status=status.HTTP_200_OK)



class OrderItemView(generics.ListCreateAPIView):
    """
    View class for displaying and generating orders.
    User must be authenticated for using this view.
    Further, order list can be filtered and searched
    """    
    
    serializer_class = OrderSerializer
    
    filterset_fields = ['status', 'date']
    ordering_fields = ['status', 'date']
    
    
    def get_queryset(self):
        """
        Methods for making personalized querysets

        Returns:
            QuerySet[Order]: different order querysets for managers, crew members and customers
        """        
        
        request = self.request
        user = request.user
        
        if isManager(request): # Checking if user is manager
            return Order.objects.all()
        elif isCrew(request): # Checking if user is delivery crew member
            return Order.objects.filter(delivery_crew=user)
        return Order.objects.filter(user=user) # Returning only specified user's orders
    
    
    def get_permissions(self):
        """
        Method to provide the permissions for different requests specifically for this specified view

        Returns:
            list: permission list for different requests
        """        
        
        permission_classes = [IsAuthenticated]
        if self.request.method == 'POST': # Checking if post request is made
            permission_classes = [IsCustomerUser]
        return [permission() for permission in permission_classes]


    def perform_action(self, serializer, obj):
        """
        Method for creating the serializer object and saving the item

        Args:
            serializer (ModelSerializer): serializer class for generating object
            obj (Model): model object for generating serializer object

        Returns:
            Serializer: serializer object after saving the item
        """        
        
        serialized_order = serializer(obj)
        serialized_order.is_valid(raise_exception=True)
        serialized_order.save()
        return serialized_order
        

    def create(self, request, *args, **kwargs):
        """
        Method for generting the orders.
        Only customers can generate the orderitems

        Args:
            request (Request): request object from the client side

        Returns:
            Response: different response objects for the clients
        """        
        
        user = request.user
        cart_items = Cart.objects.filter(user=user)
        if not cart_items: # Checking if cart is empty
            return Response({"message": "Cart is empty"}, status=status.HTTP_204_NO_CONTENT)
        
        # Calucalting the totaal price
        total_price = 0
        for item in cart_items: 
            total_price += item.price
        
        # Generating order object
        order = Order(user=user, total=total_price, date=datetime.now())
        serialized_order = self.perform_action(OrderSerializer, order)
            
        # Making orderitem objects from cart items
        for item in cart_items:
            order_item = OrderItem(
                order=order,
                menuitem=item.menuitem,
                quantity=item.quantity,
                unit_price=item.unit_price,
                price=item.price
            )
                
            self.perform_action(OrderItemSerializer, order_item)
            item.delete()

        return Response({'message':'request successful', 'item': serialized_order.data}, status=status.HTTP_201_CREATED)
        
        
        
class SingleOrderItemView(generics.RetrieveUpdateDestroyAPIView):
    """
    View class for handling single orderitem.
    User must be authenticated for using this view.
    Seperate permissions for seperate request types
    """    
    
    serializer_class = OrderSerializer
    
    
    def get_permissions(self):
        """
        Method to provide the permissions for different requests specifically for this specified view

        Returns:
            list: permission list for different requests
        """        
        
        permission_classes = [IsManagerUser]
        if self.request.method == 'GET':
            permission_classes = [IsAuthenticated]
        elif self.request.method == 'PATCH':
            permission_classes = [IsManagerorCrewUser]
        return [permission() for permission in permission_classes]

    
    def get_queryset(self):
        """
        Methods for making personalized querysets

        Returns:
            QuerySet[Order]: different order querysets for managers, crew members and customers
        """      
          
        request = self.request
        user = request.user
        
        if isManager(request): # Checking if user is manager
            return Order.objects.all()
        elif isCrew(request): # Checking if user is delivery crew member
            return Order.objects.filter(delivery_crew=user)
        return Order.objects.filter(user=user) # Returning only specified user's orders
    
    
    def perform_update(self, serializer):
        request = self.request
        
        order_instance = self.get_object() # Get object instance
        # Create data object
        req_obj = dict(
            user = order_instance.user.id,
            total = order_instance.total,
            date = order_instance.date,
            # Managers can change crew-id and status
            delivery_crew = request.data.get('delivery_crew', order_instance.delivery_crew.id),
            status = request.data.get('status', order_instance.status),
        )
        
        # Crew can only change status so, fixing (hard coding) the crew_id
        if isCrew(request):
            req_obj['delivery_crew'] = order_instance.delivery_crew.id
        
        # Saving the model instance uing serializer
        serializer = self.get_serializer(order_instance, data=req_obj, partial=False)
        serializer.is_valid(raise_exception=True)
        serializer.save()
