import os
import time
from os.path import basename

import requests
from bs4 import BeautifulSoup

from config.settings import MEDIA_ROOT
from main.models import Player, Logo, Flag


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
    start_time = time.time()
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/117.0"
    }

    players_counting = (lambda: [1 + 25 * i for i in range(20)])()
    pages = [1 + i for i in range(20)]
    players = []
    player_profiles_links = []
    for page in pages:
        print(f'Parsing... Page: {page}/20')
        url = f'https://www.transfermarkt.world/spieler-statistik/wertvollstespieler/marktwertetop?ajax=yw1&altersklasse=alle&ausrichtung=alle&jahrgang=0&kontinent_id=0&land_id=0&page={page}&plus=1&spielerposition_id=alle'
        response = requests.get(url, headers=headers)

        soup = BeautifulSoup(response.text, "lxml")
        links = soup.find_all('td', class_="hauptlink")
        costs = soup.find_all('td', class_="rechts hauptlink")
        name_n_role = soup.find_all('table', class_='inline-table')
        team_age_country = soup.find_all('td', class_='zentriert')  # commands

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

        for team in team_age_country:
            if team.find_all('a'):
                index = players_count
                logo = team.find('img').get('src')
                team = team.find('a').get('title')
                players_count += 1
                for i in players:
                    if i['id'] == index:
                        i['team'] = team

                logo_path = f'{MEDIA_ROOT}/logo/{team.replace(' ', '_')}.png'
                if not os.path.exists(logo_path):
                    with open(logo_path, "wb") as f:
                        f.write(requests.get(logo).content)

                html_logo_path = f'/media/logo/{team.replace(' ', '_')}.png'

                Logo.objects.update_or_create(
                    team=team,
                    defaults={
                        'pic': html_logo_path
                    })

        count = 0
        players_count = players_counting[pages.index(page)]

        for i in team_age_country:
            if i.find('img'):
                if team_age_country[count - 1].text != '':
                    age = team_age_country[count - 1].text
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
        for c in team_age_country:
            if c.find('img', class_="flaggenrahmen"):
                flag = c.find('img', class_="flaggenrahmen").get('src')
                country = c.find('img', class_="flaggenrahmen").get('alt')
                for i in players:
                    if i['id'] == players_count:
                        i['country'] = country
                players_count += 1

                flag_path = f'{MEDIA_ROOT}/flags/{country.replace(' ', '_')}.png'

                if not os.path.exists(flag_path):
                    with open(flag_path, "wb") as f:
                        f.write(requests.get(flag).content)

                html_flag_path = f'/media/flags/{country.replace(' ', '_')}.png'

                Flag.objects.update_or_create(
                    country=country,
                    defaults={
                        'pic': html_flag_path
                    })

        for l in links:
            if 'profil/spieler' in l.find('a')['href']:
                player_profiles_links.append(f'https://www.transfermarkt.world{l.find('a')['href']}')

    for i in players:
        Player.objects.update_or_create(
            name=i['name'],
            defaults={
                'team': i['team'],
                'role': i['role'],
                'cl': 0,
                'age': int(i['age']),
                'country': i['country'],
                'cost': i['cost']
            }
        )

    print('Photo and CL parsing...')
    count_circles = 0

    while len(player_profiles_links) != 0:
        for link in player_profiles_links:
            count_circles += 1
            middle_time = time.time()
            middle_execution_time = middle_time - start_time
            print(f'Circle: {count_circles}| links: {player_profiles_links.index(link)}/{len(player_profiles_links)}')
            print(f'{middle_execution_time:.4f} seconds')
            profiles_response = requests.get(link, headers=headers)
            soup = BeautifulSoup(profiles_response.text, "lxml")
            try:
                team_number = soup.find('div', class_="data-header__headline-container")
                team_number = team_number.find('span', class_="data-header__shirt-number").text
                team_number = team_number.replace('#', '')
                profile = soup.find('div', class_='modal__content')
                profile = profile.find('img')
                name = profile.get('alt')
                player = Player.objects.get(name=name)

                photo = profile.get('src').replace('?lm=1', '')
                photo_path = f'{MEDIA_ROOT}/players/{name.replace(' ', '_')}.png'

                if not os.path.exists(photo_path):
                    with open(photo_path, "wb") as f:
                        f.write(requests.get(photo).content)
                        print(f'Photo {name} saved {player_profiles_links.index(link)}/{len(player_profiles_links)}')
                else:
                    print(f'Photo {name} updated {player_profiles_links.index(link)}/{len(player_profiles_links)}')
                player.photo_path = f'/media/players/{name.replace(' ', '_')}.png'
                if team_number:
                    player.team_number = team_number

                cl = soup.find_all('img')
                for i in cl:
                    if i.get('alt') == 'Победитель Лиги Чемпионов':
                        cl_done = int(i.next_element.next_element.text)
                        player.cl = cl_done

                player.save()
                player_profiles_links.remove(link)

            except AttributeError:
                print('Error, Repeat')
            except Player.DoesNotExist:
                player_profiles_links.remove(link)
                print('Player not exists')
            except requests.exceptions.ChunkedEncodingError:
                print('I dont give a fuck, man')
    end_time = time.time()
    execution_time = end_time - start_time
    print(f'Parsing completed! {execution_time:.4f} seconds')
