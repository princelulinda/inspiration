import six
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.admin.views.decorators import user_passes_test
from django.contrib.auth.mixins import UserPassesTestMixin


def superuser_required(
    function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url=None
):
    """
    Decorator for views that checks that the user is logged in and if the user is a superuser,
    redirecting to the log-in page if necessary.
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_superuser,
        login_url=login_url,
        redirect_field_name=redirect_field_name,
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


class LoginRequiredSuperuserMixim(UserPassesTestMixin):
    """ Mixin for superuser """
    def test_func(self):
        return self.request.user.is_superuser
    
class LoginRequiredStaffMixim(UserPassesTestMixin):

    """ Mixin for staff user """

    def test_func(self):
        return self.request.user.is_staff
    

def group_required(group, login_url=None, raise_exception=False):
    def check_perms(user):
        if isinstance(group, six.string_types):
            groups = (group, ) 
        else:
            groups = group
        
        # first check if the user has the permission
        
        if user.groups.filter(name__in=groups).exists():
            return True
        
        # In case the 403 handler should be called raise the exception
        if raise_exception:
            raise PermissionDenied
        
        # as the last resort, show the login form
        return False
    
    return user_passes_test(check_perms, login_url=login_url)