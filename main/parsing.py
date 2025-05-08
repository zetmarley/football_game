import requests
from bs4 import BeautifulSoup
from main.models import Player

def reform_role(role):
    try:
        if 'вратарь' in role.lower():
            done_role = 'ВРТ'
        elif len(role.split(' ')) == 2:
            role = role.split(' ')
            if 'полузащитник' in role[1].lower():
                role[1] = 'ПЗ'
                done_role = role[0][0] + role[1]
            else:
                role[1] = role[1].title()
                done_role = role[0][0] + role[1][0]
        return done_role
    except UnboundLocalError:
        return '-'

def players_parsing():

    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/117.0"
    }

    players_counting = (lambda: [1 + 25 * i for i in range(20)])()
    pages = [1 + i for i in range(20)]
    players = []

    for page in pages:
        print(f'Parsing... Page: {page}/20')
        url = f'https://www.transfermarkt.world/spieler-statistik/wertvollstespieler/marktwertetop?ajax=yw1&altersklasse=alle&ausrichtung=alle&jahrgang=0&kontinent_id=0&land_id=0&page={page}&plus=1&spielerposition_id=alle'
        response = requests.get(url, headers=headers)

        soup = BeautifulSoup(response.text, "lxml")

        costs = soup.find_all('td', class_="rechts hauptlink")
        name_n_role = soup.find_all('table', class_='inline-table')
        commands = soup.find_all('td', class_='zentriert')
        ages = soup.find_all('td', class_="zentriert")
        countries = soup.find_all('td', class_="zentriert")

        players_count = players_counting[pages.index(page)]
        for nr in name_n_role:
            if nr.find('a'):
                index = players_count
                name = nr.find_all('a')[-1].text
                role = nr.find_all('td')[-1].text
                players_count += 1
                players_data1 = {'id': index,
                                'name': name,
                                'role': reform_role(role),
                                 'cl': 0}
                players.append(players_data1)

        players_count = players_counting[pages.index(page)]

        for cmnd in commands:
            if cmnd.find_all('a'):
                index = players_count
                team = cmnd.find('a').get('title')
                players_count += 1
                for i in players:
                    if i['id'] == index:
                        i['team'] = team

        count = 0
        players_count = players_counting[pages.index(page)]

        for i in ages:
            if i.find('img'):
                if ages[count - 1].text != '':
                    age = ages[count - 1].text
                    for i in players:
                        if i['id'] == players_count:
                            i['age'] = age
                    players_count += 1

            count += 1


        players_count = players_counting[pages.index(page)]

        for cost in costs:
            value = cost.find('a').text
            for i in players:
                if i['id'] == players_count:
                    i['cost'] = value
            players_count += 1

        players_count = players_counting[pages.index(page)]
        for c in countries:
            if c.find('img', class_="flaggenrahmen"):
                country = c.find('img', class_="flaggenrahmen").get('alt')
                for i in players:
                    if i['id'] == players_count:
                        i['country'] = country
                players_count += 1

    for i in players:

        Player.objects.update_or_create(
            name=i['name'],
            defaults={
                'team': i['team'],
                'role': i['role'],
                'cl': int(i['cl']),
                'age': int(i['age']),
                'country': i['country'],
                'cost': i['cost']
            }
        )
    print(f'Parsing completed!')