from rest_framework.permissions import BasePermission


class IsManagerUser(BasePermission):
    """
    Allows access only to users present in manager group
    """    
    
    def has_permission(self, request, view):
        """
        Method to determine the permission criteria for the permission class

        Args:
            request (Request): request object obtained from the client side
            view (View): view object obtained from server

        Returns:
            bool: true if manager user else false
        """        
        
        return isManager(request)


class IsCustomerUser(BasePermission):
    """
    Allows access only to users not in manager or delivery-crew groups
    """    
    
    def has_permission(self, request, view):
        """
        Method to determine the permission criteria for the permission class

        Args:
            request (Request): request object obtained from the client side
            view (View): view object obtained from server

        Returns:
            bool: true if neither manager nor crew user else false
        """        
        
        return bool(
            request.user and
            request.user.is_authenticated and
            not isManager(request) and 
            not isCrew(request)
        )

        
class IsDeliveryCrewUser(BasePermission):
    """
    Allows access only to users present in delivery crew group
    """    
    
    def has_permission(self, request, view):
        """
        Method to determine the permission criteria for the permission class

        Args:
            request (Request): request object obtained from the client side
            view (View): view object obtained from server

        Returns:
            bool: true if crew user else false
        """        
        
        return isCrew(request)


class IsManagerorCrewUser(BasePermission):
    """
    Allows access only to users present in manager group or delivery crew group
    """    
    
    def has_permission(self, request, view):
        """
        Method to determine the permission criteria for the permission class

        Args:
            request (Request): request object obtained from the client side
            view (View): view object obtained from server

        Returns:
            bool: true if manager or crew user else false
        """        
        
        return bool(
            isManager(request)
            or isCrew(request)
        )


class IsAdminUser(BasePermission):
    """
    Allows access only to users having superuser privilige
    """    
    
    def has_permission(self, request, view):
        """
        Method to determine the permission criteria for the permission class

        Args:
            request (Request): request object obtained from the client side
            view (View): view object obtained from server

        Returns:
            bool: true if user has super user status else false
        """        
        
        return bool(request.user and request.user.is_superuser)


def isManager(request):
    """
    Method to check is valid authenticated user is a manager

    Args:
        request (Request): request object obtained from client side

    Returns:
        bool: true if user is authenticated and is present in manager group else false
    """    
    
    return bool(
        request.user
        and request.user.is_authenticated
        and request.user.groups.filter(name='Manager').exists()
    )


def isCrew(request):
    """
    Method to check is valid authenticated user is a delivery crew member

    Args:
        request (Request): request object obtained from client side

    Returns:
        bool: true if user is authenticated and is present in delivery-crew group else false
    """    
    
    return bool(
        request.user
        and request.user.is_authenticated
        and request.user.groups.filter(name='Delivery crew').exists()
    )
