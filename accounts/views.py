from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from allauth.socialaccount.models import SocialToken, SocialApp
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from django.contrib.auth.decorators import login_required
import json
from json2html import *

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

#I am creating an empty list, which I will append dictionary objects to
#Once I populate them with existing cells from our API return
def otherContactsParse(otherContacts):
    otherContactsList = []
    for person in otherContacts:
        #Everything here is self explanatory, I am, for example, taking the name field from the dictionary
        #I see whether or not the get function returned a value, if so using the correct field, I put that in a 
        #Temporary variable which I then append to the dictionary at its respective key.
        fella = {"Name":[],"Email":[],"Phone":[]}
        names = person.get('names', [])
        phones = person.get('phoneNumbers', [])
        emails = person.get('emailAddresses', [])
        if names:
            name = names[0].get('displayName')
            fella["Name"].append(name)
        else:
            fella["Name"].append("Not Provided")
        if emails:
            email = emails[0].get('value')
            fella["Email"].append(email)
        else:
            fella["Email"].append("Not Provided")
        if phones:
            phone = phones[0].get('canonicalForm')
            fella["Phone"].append(phone)
        else:
            fella["Phone"].append("Not Provided")
        otherContactsList.append(fella)
    return otherContactsList

#I am creating an empty list, which I will append dictionary objects to
#Once I populate them with existing cells from our API return
def contactsParse(contacts):
    contactsList = []
    for person in contacts:
        #Everything here is self explanatory, I am, for example, taking the name field from the dictionary
        #I see whether or not the get function returned a value, if so using the correct field, I put that in a 
        #Temporary variable which I then append to the dictionary at its respective key.
        fella = {"Name":[],"Nickname":[],"Relation":[],"Email":[],"Phone":[],"Birthday":[], "Address":[], "Organization":[]}
        names = person.get('names', [])
        nicknames = person.get('nicknames', [])
        relations = person.get('relations', [])
        emails = person.get('emailAddresses', [])
        phones = person.get('phoneNumbers', [])        
        birthdays = person.get('birthdays', [])
        addresses = person.get('addresses', [])
        organizations = person.get('organizations', [])

        #Welcome to if-statement hell
        #There is probably a better, pythonic way of doing this but I don't care.
        if names:
            name = names[0].get('displayName')
            fella["Name"].append(name)
        else:
            fella["Name"].append("Not Provided")

        if nicknames:
            nickname = nicknames[0].get('value')
            fella["Nickname"].append(nickname)
        else:
            fella["Nickname"].append("Not Provided")

        if relations:
            type = relations[0].get('formattedType')
            guy = relations[0].get('person')
            fella["Relation"].append(guy + ", " + type)
        else:
            fella["Relation"].append("Not Provided")

        if emails:
            email = emails[0].get('value')
            fella["Email"].append(email)
        else:
            fella["Email"].append("Not Provided")

        if phones:
            phone = phones[0].get('canonicalForm')
            fella["Phone"].append(phone)
        else:
            fella["Phone"].append("Not Provided")

        if birthdays:
            birthday = birthdays[0].get('text')
            fella["Birthday"].append(birthday)
        else:
            fella["Birthday"].append("Not Provided")

        if addresses:
            address = addresses[0].get('formattedValue')
            fella["Address"].append(address)
        else:
            fella["Address"].append("Not Provided")

        if organizations:
            orgName = organizations[0].get('name')
            title = organizations[0].get('title')
            fella["Organization"].append(title + ", " + orgName)
        else:
            fella["Organization"].append("Not Provided")

        contactsList.append(fella)

    return contactsList

@login_required
def index(request):
    if request.user.is_authenticated:
        user = request.user
        creds = get_cred(user)
        #Build the v1 People API with given credentials
        peopleService = build('people', 'v1', credentials=creds)
        
        #Call the People API otherContacts() method, which will return a dict containing emails, names, and phone numbers
        otherContactsDump = peopleService.otherContacts().list(readMask='emailAddresses,names,phoneNumbers').execute()
        otherContactsList = otherContactsParse(otherContactsDump.get('otherContacts', []))
        otherContacts = json.dumps(otherContactsList, indent = 4)  
        
        #Call the People API connections() method, which will try to scrape every available personFields (unfortunately no easy 'all')
        contactsDump = peopleService.people().connections().list(resourceName='people/me',sortOrder='FIRST_NAME_ASCENDING',personFields='addresses,ageRanges,birthdays,emailAddresses,genders,names,nicknames,occupations,organizations,phoneNumbers,relations').execute()
        #Use my dumb way of stripping out garbage information that the API returns and return a list of dicts
        contactsList = contactsParse(contactsDump.get('connections', []))
        #Convert the list we just returned from the parse function to a JSON
        contacts = json.dumps(contactsList, indent = 4)  
       
        #Convert our JSONs into an HTML table
        otherContacts = json2html.convert(json=otherContacts, table_attributes="id=\"other-Contacts-Table\" class=\"table table-striped table-bordered table-hover\"")
        contacts = json2html.convert(json=contacts, table_attributes="id=\"contacts-Table\" caption=\"Contacts\" class=\"table table-striped table-bordered table-hover\"")
        return render(request, 'accounts/index.html', {'otherContacts' : otherContacts, 'contacts' : contacts})
    else:
        #If we are not logged in return to the home screen.
        print("Not authenticated")
        return HttpResponseRedirect(reverse('home:index'))
