import requests
from bs4 import BeautifulSoup


def players_parsing():

    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/117.0"
    }

    players_counting = (lambda: [1 + 25 * i for i in range(20)])()
    pages = [1 + i for i in range(20)]
    players = []

    for page in pages:
        url = f'https://www.transfermarkt.world/spieler-statistik/wertvollstespieler/marktwertetop?ajax=yw1&altersklasse=alle&ausrichtung=alle&jahrgang=0&kontinent_id=0&land_id=0&page={page}&plus=1&spielerposition_id=alle'
        response = requests.get(url, headers=headers)

        soup = BeautifulSoup(response.text, "lxml")

        costs = soup.find_all('td', class_="rechts hauptlink")
        name_n_role = soup.find_all('table', class_='inline-table')
        commands = soup.find_all('td', class_='zentriert')
        ages = soup.find_all('td', class_="zentriert")

        players_count = players_counting[pages.index(page)]
        for nr in name_n_role:
            if nr.find('a'):
                index = players_count
                name = nr.find_all('a')[-1].text
                role = nr.find_all('td')[-1].text
                # print(index, name, role)
                players_count += 1
                players_data1 = {'id': index,
                                'name': name,
                                'role': role,
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
            # print(count, i)
            if i.find('img'):
                if ages[count - 1].text != '':
                    # print(players_count)
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

    return players

        # players_count = players_counting[pages.index(page)]
        # for i in soup.find_all('a'):
        #     if 'profil/spieler' in str(i.get('href')):
        #         url = f'https://www.transfermarkt.world{i.get('href')}'
        #
        #         response = requests.get(url, headers=headers)
        #         soup = BeautifulSoup(response.text, "lxml")
        #         for i in soup.find_all('a', class_="data-header__success-data"):
        #             if i.get('title') == 'Победитель Лиги Чемпионов':
        #                 cl = i.find('span', class_="data-header__success-number").text
        #                 for i in players:
        #                     if i['id'] == players_count:
        #                         i['cl'] = cl


                # players_count += 1

for i in players_parsing():
    print(i)
