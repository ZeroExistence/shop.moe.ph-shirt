## This is a middleware for stripping slash on the url
## Some cleanup is needed since all the imports are from middleware.common

import re
from urllib.parse import urlparse

from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.core.mail import mail_managers
from django.http import HttpResponsePermanentRedirect
from django.urls import is_valid_path
from django.utils.deprecation import MiddlewareMixin
from django.utils.http import escape_leading_slashes


class RemoveSlashMiddleware(MiddlewareMixin):
    """
    This middleware provides the inverse of the APPEND_SLASH option built into
    django.middleware.common.CommonMiddleware. It should be placed just before
    or just after CommonMiddleware.
    If REMOVE_SLASH is True, the initial URL ends with a slash, and it is not
    found in the URLconf, then a new URL is formed by removing the slash at the
    end. If this new URL is found in the URLconf, then Django redirects the
    request to this new URL. Otherwise, the initial URL is processed as usual.
    For example, foo.com/bar/ will be redirected to foo.com/bar if you don't
    have a valid URL pattern for foo.com/bar/ but do have a valid pattern for
    foo.com/bar.
    Using this middlware with REMOVE_SLASH set to False or without REMOVE_SLASH
    set means it will do nothing.
    Orginally, based closely on Django's APPEND_SLASH CommonMiddleware
    implementation at
    https://github.com/django/django/blob/master/django/middleware/common.py.
    It has been reworked to use regular expressions instead of deconstructing/
    reconstructing the URL, which was problematically re-encoding some of the
    characters.
    """

    def process_request(self, request):

        old_url = request.build_absolute_uri()
        # match any / followed by ? (query string present)
        # OR match / at the end of the string (no query string)
        trailing_slash_regexp = r'(\/(?=\?))|(\/$)'
        new_url = old_url

        if getattr(settings, 'APPEND_SLASH') and getattr(settings, 'REMOVE_SLASH'):
            raise ImproperlyConfigured("APPEND_SLASH and REMOVE_SLASH may not both be True.")

        # Remove slash if REMOVE_SLASH is set and the URL has a trailing slash
        # and there is no pattern for the current path
        if getattr(settings, 'REMOVE_SLASH', False) and re.search(trailing_slash_regexp, old_url):
            urlconf = getattr(request, 'urlconf', None)
            if (not is_valid_path(request.path_info, urlconf)) and is_valid_path(request.path_info[:-1], urlconf):
                new_url = re.sub(trailing_slash_regexp, '', old_url)
                if settings.DEBUG and request.method == 'POST':
                    raise RuntimeError((""
                    "You called this URL via POST, but the URL ends in a "
                    "slash and you have REMOVE_SLASH set. Django can't "
                    "redirect to the non-slash URL while maintaining POST "
                    "data. Change your form to point to %s (without a "
                    "trailing slash), or set REMOVE_SLASH=False in your "
                    "Django settings.") % (new_url))

        if new_url == old_url:
            # No redirects required.
            return
        return HttpResponsePermanentRedirect(new_url)