import instaloader
import csv
import sys
from unidecode import unidecode
import getpass 


L = instaloader.Instaloader()


# Getting user info...
print("Enter your credentials...")
username = input("Username: ")
password = getpass.getpass(prompt='Password: ', stream=None) 
print("")
print("")

#Login or load session
print("Logging in...")
L.login(username, password)
print("Logged in")
print("")
print("")
print("User to scrap profile...")
userToScrap = input("Username: ")
print("")
print("")
print("Display type:")
print("1) Followers")
print("2) Following")
displayType = int(input())
print("")
print("")
print("Male or female")
print("1) Female")
print("2) Female and unknown")
print("3) Male")
print("4) Male and unknown")
print("5) Unknown only")
maleOrFemale = int(input())
print("")
print("")


#reading datasets
print("Loading names datasets...")
csv_female = csv.reader(open('datasets/female_names.csv', "r"))
csv_male = csv.reader(open('datasets/male_names.csv', "r"))

female_names = []
male_names = []
for name in csv_female:
    female_names.append(name[0].split(' ', 1)[0])
for name in csv_male:
    male_names.append(name[0].split(' ', 1)[0])


# Obtain profile metadata
profile = instaloader.Profile.from_username(L.context, userToScrap)

def isFemale(name):
    for n in female_names:
        if n == name.upper():
            return True
    return False

def isMale(name):
    for n in male_names:
        if n == name.upper():
            return True
    return False

print("Retreaving metadata from profile, please stand by...")
#SORTING FEMALE, MALE, UNKNOWN

if displayType == 1:
    toDisplay = profile.get_followers()
    print("Loading follower list...")
elif displayType == 2:
    toDisplay = profile.get_followees()
    print("Loading following list...")

i = 0
for followee in toDisplay:
    user = unidecode(followee.full_name.upper() or followee.username.upper()).replace('.', '').replace('-','').replace('(','').replace(')','').replace('@','').replace('[','').replace(']','').replace('_', ' ').replace("'", '').split(' ', 1)[0].replace('_', '').replace('~', '').replace('!', '').replace('*', '').replace('0', '').replace('1', '').replace('2', '').replace('3', '').replace('4', '').replace('5', '').replace('6', '').replace('7', '').replace('8', '').replace('9', '').replace('#', '').strip()
    i+=1
    
    #if followee.followers <= followerLimit:
    if maleOrFemale == 1 and isFemale(user):
        print("(",str(i),")    ", (followee.full_name or followee.username), "               (https://www.instagram.com/"+followee.username+")")
    elif maleOrFemale == 2:
        if isFemale(user):
            print("(",str(i),")  (fem)  ", (followee.full_name or followee.username), "               (https://www.instagram.com/"+followee.username+")")
        elif not isMale(user):
            print("(",str(i),")  (unk)  ", (followee.full_name or followee.username), "               (https://www.instagram.com/"+followee.username+")          ", user)
    elif maleOrFemale == 3 and isMale(user):
        print("(",str(i),")    ", (followee.full_name or followee.username), "               (https://www.instagram.com/"+followee.username+")")
    elif maleOrFemale == 4:
        if isMale(user):
            print("(",str(i),")  (man)  ", (followee.full_name or followee.username), "               (https://www.instagram.com/"+followee.username+")")
        elif not isFemale(user):
            print("(",str(i),")  (unk)  ", (followee.full_name or followee.username), "               (https://www.instagram.com/"+followee.username+")          ", user)
    elif maleOrFemale == 5 and not isFemale(user) and not isMale(user):
        print("(",str(i),")  (unk)  ", (followee.full_name or followee.username), "               (https://www.instagram.com/"+followee.username+")          ", user)
        