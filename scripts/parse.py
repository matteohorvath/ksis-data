import asyncio
from prisma import Prisma
from bs4 import BeautifulSoup
from datetime import datetime
async def main() -> None:
    db = Prisma()
    await db.connect()
    with open("../data/upcoming.html", "r") as f:
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
   

    await db.disconnect()


if __name__ == '__main__':
    asyncio.run(main())
