import instaloader
import csv
from unidecode import unidecode
import getpass 
import webbrowser
import platform

os = platform.system()
if os == 'Linux':
    chrome_path = '/usr/bin/google-chrome %s'
elif os == 'Windows':
    chrome_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'
elif os == 'Darwin':
    chrome_path = 'open -a /Applications/Google\ Chrome.app %s'


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

def profileElegible(followee):
    elegible = True
    if followee.followers <= maxFollowers:
        for word in followee.biography.split(' '):
            word = unidecode(word).replace('.','').replace('-','').replace('_','').replace(',','').replace('%','').replace('*','').replace('|','').replace('@','').replace('/',' ').replace('(','').replace(')', '').replace(':','').replace('"','').replace('#','').replace('[','').replace(']','').strip()
            for w in word.split(' '):
                for blackListedWord in blacklisted_words:
                    if w.upper() == blackListedWord.upper():
                        elegible = False
    else:
        return False
    return elegible

def openProfilesChrome(urls):
    tabs_n = input("How many tabs to open in the browser time at a time? ")
    j = 0
    tabsOpened = 0
    for i in urls:
        j+=1
        
        url = "https://www.instagram.com/" + i
        webbrowser.get(chrome_path).open(url)
        tabsOpened+=1
        if j == int(tabs_n):
            input("Continue? (Enter)")
            j = 0
    print("Total tabs opened:", tabsOpened)

def storeProfile(username, option):
    if option == 1 or option == 3:
        f = open("profiles_stored.txt", "a")
        f.write(username + "\n")



L = instaloader.Instaloader()


# Getting user info...
print("Enter your credentials...")
username = input("Username: ")
password = getpass.getpass(prompt='Password: ', stream=None) 

maleOrFemale = 0
displayType = 0
userToScrap = 0

#Login or load session
print("Logging in...")
L.login(username, password)
print("Logged in")
print("What to do with the profiles")
print("1) Wipe the current profiles and store new ones")
print("2) Read the profiles and display it")
print("3) Add profiles to the current database to read them later")
profilesOption = int(input())
if profilesOption != 2:
    print("User to scrap profile...")
    userToScrap = input("Username: ")
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
    print("6) Female - hard search (takes a lot of time)")
    maleOrFemale = int(input())

    if maleOrFemale == 6:
        maxFollowers = int(input("Maximum of followers (0 to no limit): "))
        if not maxFollowers:
            maxFollowers = 9999999999999999999999

    #reading datasets
    print("Loading names datasets...")
    csv_female = csv.reader(open('datasets/female_names.csv', "r"))
    csv_male = csv.reader(open('datasets/male_names.csv', "r"))
    csv_blacklisted_words_in_bio = csv.reader(open('datasets/blacklisted_words.csv', "r"))

    if profilesOption == 1:
        f = open("profiles_stored.txt", "w")
        f.write("")
        f.close()

    female_names = []
    male_names = []
    blacklisted_words = []
    for name in csv_female:
        female_names.append(name[0].split(' ', 1)[0])
    for name in csv_male:
        male_names.append(name[0].split(' ', 1)[0])
    for word in csv_blacklisted_words_in_bio:
        blacklisted_words.append(word[0].split(' ', 1)[0])


    # Obtain profile metadata
    profile = instaloader.Profile.from_username(L.context, userToScrap)


    print("Retreaving metadata from profile, please stand by...")
    #SORTING FEMALE, MALE, UNKNOWN

    if displayType == 1:
        toDisplay = profile.get_followers()
        print("Loading follower list...")
    elif displayType == 2:
        toDisplay = profile.get_followees()
        print("Loading following list...")

    urls = []
    i = 0
    elegible = 0
    for followee in toDisplay:
        user = unidecode(followee.full_name.upper() or followee.username.upper()).replace('.', '').replace('-','').replace('(','').replace(')','').replace('@','').replace('[','').replace(']','').replace('_', ' ').replace("'", '').split(' ', 1)[0].replace('_', '').replace('~', '').replace('!', '').replace('*', '').replace('0', '').replace('1', '').replace('2', '').replace('3', '').replace('4', '').replace('5', '').replace('6', '').replace('7', '').replace('8', '').replace('9', '').replace('#', '').strip()
        i+=1
        if maleOrFemale == 1 and isFemale(user):
            print("(",str(i),")    ", (followee.full_name or followee.username), "               (https://www.instagram.com/"+followee.username+")")
            urls.append(followee.username)
            storeProfile(followee.username, profilesOption)
            elegible+=1
        elif maleOrFemale == 2:
            urls.append(followee.username)
            if isFemale(user):
                print("(",str(i),")  (fem)  ", (followee.full_name or followee.username), "               (https://www.instagram.com/"+followee.username+")")
            elif not isMale(user):
                print("(",str(i),")  (unk)  ", (followee.full_name or followee.username), "               (https://www.instagram.com/"+followee.username+")          ", user)
            storeProfile(followee.username, profilesOption)
            elegible+=1
        elif maleOrFemale == 3 and isMale(user):
            urls.append(followee.username)
            print("(",str(i),")    ", (followee.full_name or followee.username), "               (https://www.instagram.com/"+followee.username+")")
            storeProfile(followee.username, profilesOption)
            elegible+=1
        elif maleOrFemale == 4:
            urls.append(followee.username)
            if isMale(user):
                print("(",str(i),")  (man)  ", (followee.full_name or followee.username), "               (https://www.instagram.com/"+followee.username+")")
            elif not isFemale(user):
                print("(",str(i),")  (unk)  ", (followee.full_name or followee.username), "               (https://www.instagram.com/"+followee.username+")          ", user)
            storeProfile(followee.username, profilesOption)
            elegible+=1
        elif maleOrFemale == 5 and not isFemale(user) and not isMale(user):
            urls.append(followee.username)
            print("(",str(i),")  (unk)  ", (followee.full_name or followee.username), "               (https://www.instagram.com/"+followee.username+")          ", user)
            storeProfile(followee.username, profilesOption)
            elegible+=1
        elif maleOrFemale == 6 and isFemale(user):
            if profileElegible(followee):
                print("(",str(i),")    ", (followee.full_name or followee.username), "               (https://www.instagram.com/"+followee.username+")")
                urls.append(followee.username)
                storeProfile(followee.username, profilesOption)
                elegible+=1

    print(elegible, "profiles to be opened...")
    openProfilesChrome(urls)
else:
    f = open("profiles_stored.txt", "r")
    profiles = []
    for user in f.readlines():
        profiles.append(user.replace('\n',''))
    openProfilesChrome(profiles)