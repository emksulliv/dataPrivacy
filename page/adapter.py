from django.conf import settings
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter

#Here I am overriding the redirect_url to be dynamic instead of 
#Using the statically defined LOGIN_REDIRECT_URL 
class socialAccountAdapter(DefaultSocialAccountAdapter):
    def get_connect_redirect_url(self, request, socialaccount):        
        path = "/accounts/{provider}/"
        #I retrieve the provider of the social account that has logged in
        #Login redirect will be /accounts/google/ for a google login
        return path.format(provider=socialaccount.provider)