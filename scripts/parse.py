import asyncio
from prisma import Prisma
from bs4 import BeautifulSoup
from datetime import datetime
from tqdm import tqdm
import os
async def main() -> None:
    db = Prisma()
    await db.connect()
    #os.system("rm db.sqlite")
    #os.system("prisma db push")
    import glob 
    years = glob.glob("data/years/*")

    comps = []
    for y in tqdm(years):
        with open(y, "r") as f:
            html = f.read()
            soup = BeautifulSoup(html, "html.parser")
            table = soup.find_all("table")
            for t in table:
                #month level
                trs = t.find_all("tr")
                for tr in tqdm(trs):
                    #competition level
                    #print(tr.prettify())
                    a_s = tr.find_all("a")
                    strongs = tr.find_all("strong")
                    comp_date = datetime.strptime( strongs[0].text.replace(" ",""), '%Y.%m.%d')
                    comp_title = strongs[1].text
                    comp_place = strongs[2].text.split(":")[1]
                    comp_categories = []
                    #print(len(a_s))
                    for a in range(1,len(a_s)):
                        #competition detail level
                        comp_categories.append(a_s[a].text)
                    #print(comp_date, comp_title, comp_place, comp_categories)
                    comps.append([comp_date, comp_title, comp_place, comp_categories])
                    
                    post = await db.competition.create(
                            {
                                'deadline' : datetime.fromtimestamp(0),
                                'organiser' : "",
                                'place' : comp_place,
                                'title' : comp_title,
                                'date' : comp_date 
                            }
                    )
                    print("posted comp ", post)
                    for cats in comp_categories:
                        cat = await db.category.create({'name' : cats,
                                'competition_id' : post.id
                        })
                    
    with open("data/upcoming.html", "r") as f:
        html = f.read()
        soup = BeautifulSoup(html, "html.parser")
        table = soup.find_all("table")
        for t in table:
            tds = t.find_all("td")
            i = 0
            date = ''
            title = ""
            organiser = ""
            place = ""
            deadline = ''
            for td in tds:
                strongs = td.find_all("strong")
                for x in range(len(strongs)):
                    if i%2==0:
                        date =datetime.strptime( strongs[0].text.replace(" ", ""), "%Y.%m.%d")
                    else:
                        title = strongs[0].text 
                        organiser = strongs[1].text.split(":")[1]
                        place = strongs[2].text.split(":")[1]
                        deadline = datetime.strptime(strongs[3].text.split(":")[1].replace(" ", ""), "%Y.%m.%d")
                       


                        
                        break

                i += 1
            
            post = await db.competition.create(
                {
                    'deadline' : deadline,
                    'organiser' : organiser,
                    'place' : place,
                    'title' : title,
                    'date' : date
                }
            )
            print("posted ", post)
   

    await db.disconnect()
    print("done")


if __name__ == '__main__':
    asyncio.run(main())
