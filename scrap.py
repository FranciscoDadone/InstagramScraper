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
maleOrFemale = int(input())
print("")
print("")
followerLimit = 99999999999999
followerLimit = int(input("Follower limit?:"))
if followerLimit == 0:
    followerLimit = 99999999999999


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

def printArr(arr, ftype):
    print("---  DISPLAYING ALL",ftype,"  ---")
    i = 0
    for user in arr:
        i+=1
        if ftype == "UNKNOWN":
            print(i, ")   ", (user.full_name or user.username), "               (https://www.instagram.com/"+user.username+")          ", unidecode(user.full_name.upper() or user.username.upper()).replace('.', '').replace('_', ' ').replace("'", '').split(' ', 1)[0].replace('_', '').replace('~', '').replace('!', '').replace('*', '').replace('0', '').replace('1', '').replace('2', '').replace('3', '').replace('4', '').replace('5', '').replace('6', '').replace('7', '').replace('8', '').replace('9', '').strip())
        else:
            print(i, ")   ", (user.full_name or user.username), "               (https://www.instagram.com/"+user.username+")")
    



print("Retreaving metadata from profile, please stand by...")
#SORTING FEMALE, MALE, UNKNOWN
female_followers = []
male_followers = []
unknown_followers = []
if displayType == 1:
    toDisplay = profile.get_followers()
    print("Loading follower list...")
elif displayType == 2:
    toDisplay = profile.get_followees()
    print("Loading following list...")

i = 0
for followee in toDisplay:
    user = unidecode(followee.full_name.upper() or followee.username.upper()).replace('.', '').replace('_', ' ').replace("'", '').split(' ', 1)[0].replace('_', '').replace('~', '').replace('!', '').replace('*', '').replace('0', '').replace('1', '').replace('2', '').replace('3', '').replace('4', '').replace('5', '').replace('6', '').replace('7', '').replace('8', '').replace('9', '').strip()
    i+=1
    # if displayType == 1:
    #     print("("+str(i),"/",str(profile.followers)+")", followee.username, str(followee.followers))
    # elif displayType == 2:
    #     print("("+str(i),"/",str(profile.followees)+")", followee.username, str(followee.followers))
        
    if isFemale(user) and followee.followers <= followerLimit:
        female_followers.append(followee)
    elif isMale(user) and followee.followers <= followerLimit:
        male_followers.append(followee)
    elif followee.followers <= followerLimit:
        unknown_followers.append(followee)
        
    if maleOrFemale == 1 and isFemale(user) and followee.followers <= followerLimit:
        print("("+str(i),"/",str(profile.followers)+")    ", (followee.full_name or followee.username), "               (https://www.instagram.com/"+followee.username+")")
        female_followers.append(followee)
    elif maleOrFemale == 2:
        if isFemale(user):
            print("("+str(i),"/",str(profile.followers)+")  (fem)  ", (followee.full_name or followee.username), "               (https://www.instagram.com/"+followee.username+")")
            female_followers.append(followee)
        elif not isMale(user):
            print("("+str(i),"/",str(profile.followers)+")  (unk)  ", (followee.full_name or followee.username), "               (https://www.instagram.com/"+followee.username+")          ", unidecode(followee.full_name.upper() or followee.username.upper()).replace('.', '').replace('_', ' ').replace("'", '').split(' ', 1)[0].replace('_', '').replace('~', '').replace('!', '').replace('*', '').replace('0', '').replace('1', '').replace('2', '').replace('3', '').replace('4', '').replace('5', '').replace('6', '').replace('7', '').replace('8', '').replace('9', '').strip())
            unknown_followers.append(followee)
    elif maleOrFemale == 3 and isMale(user) and followee.followers <= followerLimit:
        print("("+str(i),"/",str(profile.followers)+")    ", (followee.full_name or followee.username), "               (https://www.instagram.com/"+followee.username+")")
        male_followers.append(followee)
    elif maleOrFemale == 4:
        if isMale(user):
            print("("+str(i),"/",str(profile.followers)+")  (man)  ", (followee.full_name or followee.username), "               (https://www.instagram.com/"+followee.username+")")
            male_followers.append(followee)
        elif not isFemale(user):
            print("("+str(i),"/",str(profile.followers)+")  (unk)  ", (followee.full_name or followee.username), "               (https://www.instagram.com/"+followee.username+")          ", unidecode(followee.full_name.upper() or followee.username.upper()).replace('.', '').replace('_', ' ').replace("'", '').split(' ', 1)[0].replace('_', '').replace('~', '').replace('!', '').replace('*', '').replace('0', '').replace('1', '').replace('2', '').replace('3', '').replace('4', '').replace('5', '').replace('6', '').replace('7', '').replace('8', '').replace('9', '').strip())
            unknown_followers.append(followee)
    
    


if maleOrFemale == 1:
    printArr(female_followers, "FEMALE")
elif maleOrFemale == 2:
    printArr(female_followers, "FEMALE")
    printArr(unknown_followers, "UNKNOWN")
elif maleOrFemale == 3:
    printArr(male_followers, "MALE")
elif maleOrFemale == 4:
    printArr(male_followers, "MALE")
    printArr(unknown_followers, "UNKNOWN")