import requests
import pandas as pd
import os
import datetime

DATA = "../data/"
url = "https://ksis.szts.sk/mtasz"

#get every year competitions
years = [str(i) for i in range(2014, 2024)]

def download_year(y): 
    if not os.path.exists(DATA + "years"):
        os.makedirs(DATA + "years")
    for y in years:
        print("Downloading year: " + y)
        r = requests.get(url + "/menu.php?rok=" + y)
        with open(DATA + "years/" +y + ".html", 'wb') as f:
            f.write(r.content)

#for y in years:
#    download_year(y)

#download competitions
comp_ids = [str(i) for i in range(1, 370)]

def download_competition(c):
    if not os.path.exists(DATA + "competitions"):
        os.makedirs(DATA + "competitions")
    for c in comp_ids:
        print("Downloading competition: " + c)
        r = requests.get(url + "/podujatie.php?pod_id=" + c)
        with open(DATA + "competitions/" + c + ".html", 'wb') as f:
            f.write(r.content)

#for c in comp_ids:
#    download_competition(c)

#download upcomings

def download_upcoming():
    print("Downloading upcoming")
    r = requests.get(url + "/menu.php?akcia=KS")
    with open(DATA + "upcoming.html", 'wb') as f:
        f.write(r.content)

#download_upcoming()


#download rankings
# first date is 2011-09-18
def download_day_rank(age, style, start):
    print("Downloading rankings for: " + str(start) + " " + age + " " + style)
    r = requests.get(url + "/slp_poradie.php?dt_od="+ start.strftime("%Y.%m.%d")+ "&evkor="+age+"&s_l=" + style)
    with open(DATA + "rankings/" + age + "/" + style + "/" + start.strftime("%Y-%m-%d") + ".html", 'wb') as f:
        f.write(r.content)
            
def download_rankings():
    #"FLN", "IFI", "JN1", "JN2" 
    ages = ["SE1", "SE2", "SE3", "SE4", "PD"]
    dance_style = ["S", "L", "T"]
    #for one week gaps from 2011-09-18 till today
    for age in ages:
        for style in dance_style:
            if not os.path.exists(DATA + "rankings/" + age + "/" + style):
                os.makedirs(DATA + "rankings/" + age + "/" + style)
            today = datetime.date.today()
            start = datetime.date(2011, 2, 13)
            delta = datetime.timedelta(days=21)
            while start < today:
                download_day_rank(age, style, start)
                start += delta
            download_day_rank(age, style, today)
download_rankings()

# download dancers
def download_dancers():
    print("Downloading dancers")
    r = requests.get(url + "/menu.php?akcia=CZ&hladany_text=")
    with open(DATA + "dancers.html", 'wb') as f:
        f.write(r.content)

#download_dancers()

# download couples

def download_couples():
    print("Downloading couples")
    r = requests.get(url + "/menu.php?akcia=CZP&hladany_text=&vekktg=&vtstt=&vtlat=")
    with open(DATA + "couples.html", 'wb') as f:
        f.write(r.content)

#download_couples()

# download formations

def download_formations():
    print("Downloading formations")
    r = requests.get(url + "/menu.php?akcia=CZF&hladany_text=")
    with open(DATA + "formations.html", 'wb') as f:
        f.write(r.content)

#download_formations()

# download judges

def download_judges():
    print("Downloading judges")
    r = requests.get(url + "/menu.php?akcia=CZR&hladany_text=")
    with open(DATA + "judges.html", 'wb') as f:
        f.write(r.content)

#download_judges()

# download counters

def download_counters():
    print("Downloading counters")
    r = requests.get(url + "/menu.php?akcia=CZS&hladany_text=")
    with open(DATA + "counters.html", 'wb') as f:
        f.write(r.content)

#download_counters()

