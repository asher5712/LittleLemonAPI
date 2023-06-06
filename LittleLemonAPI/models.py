from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
    """
    The 'Category' model for defining the type of the meal.
    Contains two fields 'slug' and 'title' for the category of food item
    """    
    
    # slug field for entering the title as a single slug word
    slug = models.SlugField()
    
    # title field for describing the title of food category
    title = models.CharField(max_length=255, db_index=True)
    
    
    def __str__(self):
        """
        The dunder string method for the model to display the random print statement

        Returns:
            str: title of the category
        """        
        
        return self.title


class MenuItem(models.Model):
    """
    The 'MenuItem' model for defining the food item available in menu.
    Contains four fields 'title', 'price', 'featured' and 'title' for the food item
    """    
    
    # title field for describing the category of the food item
    title = models.CharField(max_length=255, db_index=True)
    
    # price field for describing the price of the food item
    price = models.DecimalField(max_digits=6, decimal_places=2, db_index=True)
    
    # featured field for describing whether the item is todays special
    featured = models.BooleanField(db_index=True)
    
    # category field for describing the category of the food item
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    
    def __str__(self):
        """
        The dunder string method for the model to display the random print statement

        Returns:
            str: name of the food item
        """        
        
        return self.title


class Cart(models.Model):
    """
    The 'Cart' model for defining the temporary cart for selected food item.
    Contains three main fields 'user', 'menuitem' and 'quantity' while 
    two additional fields 'unit_price' and 'total price' of the food items
    """    
    
    # user field for checking the user adding the items to cart
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    # menuitem field for describing the item to be added in cart
    menuitem = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    
    # quantity field for describing the quantity of specific menu item
    quantity = models.SmallIntegerField()
    
    # additional unit_price field for keeping record of items unit price
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    
    # additional price field for keeping record of total price of items in cart
    price = models.DecimalField(max_digits=6, decimal_places=2)
    
    def __str__(self):
        """
        The dunder string method for the model to display the random print statement

        Returns:
            str: user with menutiem added to cart
        """        
         
        return f'{self.user} - {self.menuitem}'
    
    class Meta:
        """
        The meta classs for handling the meta data of the model.
        It contains the unique together constraint for the model
        """        
        
        # constraint to check a single user should not place same menuitem multiple times
        unique_together = ('menuitem', 'user')

        
class Order(models.Model):
    """
    The 'Order' model for defining the order given by the user.
    Contains five fields 'user', 'delivery_crew', 'status', 'date' and 'total' for order object
    """    
    
    # user field for checking the user adding the items to cart
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    # crew field for assigning the crew member to the order
    delivery_crew = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='delivery_crew', null=True)
    
    # status field for checking whether the order is still under progress or finished.
    # If finished its status is false
    status = models.BooleanField(db_index=True, default=0)
    
    # total field for keeping record of total price of items in cart
    total = models.DecimalField(max_digits=6, decimal_places=2)
    
    # date field for keeping record of order placing date
    date = models.DateField(db_index=True)
    
    def __str__(self): 
        """
        The dunder string method for the model to display the random print statement

        Returns:
            str: user name with crew name and status of the order
        """        
        
        return f'{self.user} - {self.delivery_crew}, {self.status}'

    
class OrderItem(models.Model):
    """
    The 'OrderItem' model for having details of order with menuitems.
    Contains three main fields 'order', 'menuitem' and 'quantity' while 
    two additional fields 'unit_price' and 'total price' of the food items
    """    
    
    # order field for to show which order this item represents
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    
    # menuitem field for describing the items ordered
    menuitem = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    
    # quantity field for describing the quantity of specific menu item
    quantity = models.SmallIntegerField()
    
    # additional unit_price field for keeping record of items unit price
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    
    # additional price field for keeping record of total price of items
    price = models.DecimalField(max_digits=6, decimal_places=2)
    
    def __str__(self): 
        """
        The dunder string method for the model to display the random print statement.

        Returns:
            str: order representation with total price
        """        
        
        return f'{self.order}, {self.price}'
    
    class Meta:
        """
        The meta classs for handling the meta data of the model.
        It contains the unique together constraint for the model
        """        
        
        # constraint to ensure single menuitem could be placed in multiple orders
        unique_together = ('order', 'menuitem')
