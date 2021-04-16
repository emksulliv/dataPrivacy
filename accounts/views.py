from django.shortcuts import render
from django.http import HttpResponse

from allauth.socialaccount.models import SocialToken, SocialApp
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow


def get_cred(user):
    token = SocialToken.objects.get(account__user=user, account__provider='google')
    social_app = SocialApp.objects.get(provider='google')
    creds = Credentials(
        token=token.token,
        refresh_token=token.token_secret,
        token_uri='https://oauth2.googleapis.com/token',
        client_id=social_app.client_id,
        client_secret=social_app.secret,
    )

    #If there are no valid credentials, try to refresh them.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("Trying to refresh")
            creds.refresh(Request())

    return creds
    
    

def index(request):
    user = request.user
    creds = get_cred(user)
    #Build the v1 People API with given credentials
    peopleService = build('people', 'v1', credentials=creds)
    #Call the People API otherContacts() method, which will return a JSON containing emails, names, and phone numbers
    results1 = peopleService.otherContacts().list(readMask='emailAddresses,names,phoneNumbers').execute()
    otherContacts = results1.get('otherContacts', [])
    #Call the People API connections() method, which will try to scrape every available personFields (unfortunately no easy 'all')
    results2 = peopleService.people().connections().list(resourceName='people/me', personFields='addresses,ageRanges,biographies,birthdays,calendarUrls,clientData,emailAddresses,events,externalIds,genders,imClients,interests,locales,locations,miscKeywords,names,nicknames,occupations,organizations,phoneNumbers,photos,relations,sipAddresses,skills,urls,userDefined').execute()
    contacts = results2.get('contacts', [])

    return render(request, 'accounts/index.html', context={'otherContacts' : otherContacts, 'contacts' : contacts})
