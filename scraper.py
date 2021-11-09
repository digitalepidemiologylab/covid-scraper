import os
import sys
import re
import time
from datetime import datetime
import json
from hashlib import sha512
import logging
from logging.handlers import RotatingFileHandler
from time import sleep
from pathlib import Path

from bs4 import BeautifulSoup
from helium import start_firefox
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

# Create logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

printout_handler = logging.StreamHandler()
writetofile_handler = RotatingFileHandler(
    'log.txt', mode='a', maxBytes=5*1024*1024, 
    backupCount=2, encoding=None, delay=0)

printout_handler.setLevel(logging.INFO)
printout_handler.setFormatter(formatter)
writetofile_handler.setLevel(logging.INFO)
writetofile_handler.setFormatter(formatter)

logger.addHandler(printout_handler)
logger.addHandler(writetofile_handler)

# Create browser
global browser
options = Options()
options.headless = True
browser = webdriver.Firefox(options=options)
# browser = start_firefox()
delay = 10


WEBSITES = {
    # 'Andorra': 'https://www.govern.ad/coronavirus',
    'Andorra': 'https://www.govern.ad/covid/taula.php',
    'Armenia': 'https://e.infogram.com/71d42d9d-504e-4a8b-a697-f52f4178b329?src=embed',
    'Azerbaijan': 'https://koronavirusinfo.az/az/page/statistika/azerbaycanda-cari-veziyyet',
    'Belarus': 'https://stopcovid.belta.by/',
    # 'Gibraltar': 'https://www.gibraltar.gov.gi/covid19',
    'Gibraltar': 'https://healthygibraltar.org/news/update-on-wuhan-coronavirus/',
    'Israel': 'https://datadashboard.health.gov.il/COVID-19/general',  # Hard to load
    'Kosovo': 'https://covid19-rks.net/',  # JS
    'Kyrgyzstan': 'http://med.kg/ru/informatsii.html',
    'Latvia': 'https://spkc.maps.arcgis.com/apps/opsdashboard/index.html#/4469c1fb01ed43cea6f20743ee7d5939',
    'Lithuania': 'https://e.infogram.com/57e5b447-c2ca-40da-aedb-cbf97df68a8e?src=embed',
    'Luxembourg': 'https://data.public.lu/fr/datasets/covid-19-rapports-journaliers/',
    'Monaco': 'https://www.gouv.mc/Actualites',
    # 'Montenegro': 'https://www.covidodgovor.me/me/statistika',  # JS that wget can't load
    'Montenegro': 'https://e.infogram.com/_/lQ4CDrD827kOcRBewceO?src=embed',
    # 'North_Macedonia': 'http://iph.mk/category/informacii/',  # PDFs with info
    'Poland': 'https://rcb-gis.maps.arcgis.com/apps/dashboards/fc789be735144881a5ea2c011f6c9265',
    'Romania': 'https://instnsp.maps.arcgis.com/apps/opsdashboard/index.html#/5eced796595b4ee585bcdba03e30c127',
    'Russia': 'https://стопкоронавирус.рф',
    'San_Marino': 'https://www.iss.sm/on-line/home/archivio-ufficio-stampa-iss.html',
    'Ukraine': 'https://covid19.gov.ua/',
    'Uzbekistan': 'https://coronavirus.uz/ru'
}

POSTS = [
    'Monaco', 'San_Marino'
]

WGET_DOWNLOADS = [
    'Andorra', 'Armenia', 'Azerbaijan', 'Belarus', 'Gibraltar', 'Kyrgyzstan',
    'Luxembourg', 'Monaco', 'North_Macedonia', 'Russia', 'San_Marino',
    'Ukraine', 'Uzbekistan'
]

HELIUM_DOWNLOADS = [
    'Israel', 'Kosovo', 'Latvia', 'Lithuania', 'Montenegro', 'Poland', 'Romania'
]

XPATHS = {
    'Israel': "//h3[contains(text(),'מאומתים חדשים אתמול')]",
    'Kosovo': "//h5[contains(text(),'Raste')]",
    'Latvia': "//span[contains(text(),'Saslimušo skaits')]",
    'Lithuania': "//span[contains(text(),'Iš viso buvusių/esamų atvejų skaičius')]",
    'Montenegro': "//*[//span[contains(text(), 'UKUPAN BROJ OBOLJELIH')] and //div[@class='igc-textual-text innertext']]",
    'Poland': "//strong[contains(text(),'osoby zakażone od 4 marca 2020')]",
    'Romania': "//*[@style='fill: rgb(230, 0, 0); stroke-width: 2px; font-size: 160px; line-height: normal;']"
}


def get_soup(p):
    with open(p, 'rb') as f:
        return BeautifulSoup(f.read(), 'html.parser')


def remove_latest_if_page_unchanged(p_1, p_2, country, t):
    try:
        soup_1, soup_2 = [get_soup(p) for p in [p_1, p_2]]
    except UnicodeDecodeError:
        logger.warning('Unicode decode error.')
        return
    num_1 = None
    num_2 = None
    try:
        soup_1, num_1 = getattr(Soup, country.lower())(soup_1)
        soup_2, num_2 = getattr(Soup, country.lower())(soup_2)
    except AssertionError:
        logger.warning('The structure of the file "%s" have changed. Check the source.', p_2)
    except Exception as exc:
        logger.error('%s: %s', type(exc).__name__, str(exc))
    logger.debug('%s: %s %s', country, num_1, num_2)
    remove = False
    if country in POSTS:
        if compare_soups(soup_1, soup_2):
            remove = True
    else:
        if num_1 and num_2:
            if num_1 == num_2:
                remove = True
        elif compare_soups(soup_1, soup_2):
            remove = True
    if remove:
        try:
            os.remove(p_2)
        except FileNotFoundError:
            logger.error('File "%s" not found.', p_2)
        except PermissionError:
            logger.error('You have no permission to remove the file "%s".', p_2)
    else:
        logger.info('The file "%s" has changed. Keeping the new version.', p_2)
        numbers = {}
        with open('logs/numbers.json', 'rb') as f:
            numbers = json.load(f)
        with open('logs/numbers.json', 'w') as f:
            if not numbers.get(country):
                numbers[country] = {t: num_2}
            else:
                numbers[country][t] = num_2
            json.dump(numbers, f)
    return


def compare_soups(soup_1, soup_2):
    hash_1, hash_2 = [sha512(soup.encode()).digest() for soup in [soup_1, soup_2]]
    return hash_1 == hash_2


class Soup:
    @staticmethod
    def andorra(soup):
        def condition(tag):
            if tag is None:
                return False
            return tag.name == 'div' and \
                   'col-2' in tag.get('class', '') and \
                   'Confirmats totals' in tag.contents[0]
        tags = soup.find_all(condition)
        assert len(tags) == 1
        return tags[0].parent, int(tags[0].contents[2])

    @staticmethod
    def armenia(soup):
        def condition(tag):
            if tag is None:
                return False
            return tag.name == 'script' and \
                   len(tag.contents) == 1 and \
                   'window.infographicData' in tag.contents[0]
        tag = soup.find(condition)
        cases = re.search(
            '"text":"Հաստատված դեպքերի ընդհանուր քանակը-([0-9]+)"',
            tag.contents[0]
        ).group(1)
        return tag, int(cases)

    @staticmethod
    def azerbaijan(soup):
        def condition(tag):
            if tag is None:
                return False
            return tag.name == 'span' and \
                   'Virusa yoluxan' in tag.contents[0]
        tags = soup.find_all(condition)
        assert len(tags) == 1
        return tags[0].parent.parent, \
               int(tags[0].find_previous_sibling('strong').contents[0])

    @staticmethod
    def belarus(soup):
        def condition(tag):
            if tag is None:
                return False
            return tag.name == 'div' and \
                   'ЗАРЕГИСТРИРОВАНЫ' in tag.contents
        tags = soup.find_all(condition)
        assert len(tags) == 2
        return tags[0].parent.parent, \
               int(tags[0].find_previous_sibling(
                   "div").contents[0].contents[0].replace(' ', ''))

    @staticmethod
    def israel(soup):
        def condition_outer(tag):
            if tag is None:
                return False
            return tag.name == 'h3' and \
                   len(tag.contents) == 1 and \
                   'מאומתים חדשים אתמול' in tag.contents[0]
        def condition_inner(tag):
            if tag is None:
                return False
            return tag.name == 'span' and \
                   len(tag.contents) == 1 and \
                   'סה"כ' in tag.contents[0]
        tag_outer = soup.find(condition_outer)
        tag_outer = tag_outer.parent.parent.parent.parent
        tag_inner = tag_outer.find(condition_inner)
        number = tag_inner.find_previous_sibling().contents[0].replace(',', '')
        return tag_inner.parent, int(number)

    @staticmethod
    def kosovo(soup):
        def condition(tag):
            if tag is None:
                return False
            return tag.name == 'h5' and \
                   len(tag.contents) == 1 and \
                   'Raste' in tag.contents[0]
        tag = soup.find(condition)
        return tag.parent, int(tag.parent.h3.contents[0].replace(',', ''))

    @staticmethod
    def gibraltar(soup):
        def condition(tag):
            if tag is None:
                return False
            return tag.name == 'li' and \
                   'Confirmed cases:' in tag.contents[0]
        tags = soup.find_all(condition)
        assert len(tags) == 1
        return tags[0].parent, int(tags[0].contents[0][17:])

    @staticmethod
    def kyrgyzstan(soup):
        def condition(tag):
            if tag is None:
                return False
            return tag.name == 'section' and \
                   'sp-section-3' in tag.get('id', '')
        tag = soup.find(condition)
        covid_1 = tag.tbody.tr.find_next_sibling().find_next_sibling(
            ).td.find_next_sibling().find_next_sibling()
        covid_2 = covid_1.find_next_sibling()
        cases = (
            int(covid_1.p.span.span.b.contents[0]),
            int(covid_2.p.span.strong.span.contents[0])
        )
        return tag.tbody, cases

    @staticmethod
    def latvia(soup):
        def condition(tag):
            if tag is None:
                return False
            return tag.name == 'span' and \
                   len(tag.contents) == 1 and \
                   'Saslimušo skaits' in tag.contents[0]
        tag = soup.find(condition)
        number = tag.parent.find_next_sibling().find(
            lambda tag: tag.name == 'strong'
        ).contents[0].replace(' ', '')
        return tag.parent.parent, int(number)

    @staticmethod
    def lithuania(soup):
        def condition(tag):
            if tag is None:
                return False
            return tag.name == 'span' and \
                   len(tag.contents) == 1 and \
                   'Iš viso buvusių/esamų atvejų skaičius' in tag.contents[0]
        tag = soup.find(condition)
        number = tag.parent.parent.td.span.contents[0]
        return tag.parent.parent, int(number)

    @staticmethod
    def luxembourg(soup):
        def condition(tag):
            return tag.name == 'article' and \
                   'card' in tag.get('class', []) and \
                   'resource-card' in tag.get('class', [])
        tag = soup.find(condition)
        return tag.div.h4.contents[0], None

    @staticmethod
    def monaco(soup):
        def condition(tag):
            if tag is None:
                return False
            return tag.name == 'a' and \
                   'Covid-19' in tag.get('title', '') and \
                   'cas' in tag.get('title', '')
        def post_condition(tag):
            return tag.name == 'p' and \
                   len(tag.contents) == 1 and \
                   'personnes guéries s’élève' in tag.contents[0]
        tag = soup.find(condition)
        url = 'https://www.gouv.mc' + tag['href']
        browser.get(url)
        try:
            WebDriverWait(browser, delay).until(
                EC.presence_of_element_located((
                    By.XPATH,
                    "//*[contains(text(), 'personnes guéries s’élève')]"
                ))
            )
        except TimeoutException:
            logger.warning("The link '%s' has not loaded.", url)
            return tag, None
        post_source = browser.page_source
        post_soup = BeautifulSoup(post_source, 'html.parser')
        post_tag = post_soup.find(post_condition)
        logger.debug('Monaco post tag: %s', post_tag)
        cases = re.search(
            'personnes guéries s’élève [a-zàâçéèêëîïôûùüÿñæœ .-]*([0-9]+)\.',
            post_tag.contents[0]
        ).group(1)
        return tag, int(cases)

    @staticmethod
    def montenegro(soup):
        def condition(tag):
            return tag.name == 'div' and \
                   tag.get('class', [''])[0] == 'InfographicEditor-Contents-Item' and \
                   len(tag.find_all(condition_inner)) > 0
        def condition_inner(tag):
            return tag.name == 'span' and \
                   len(tag.contents) == 1 and \
                   'UKUPAN BROJ OBOLJELIH' in tag.contents[0]
        def condition_number(tag):
            return tag.name == 'div' and \
                   'igc-textual-text' in tag.get('class', []) and \
                   'innertext' in tag.get('class', [])
        tag = soup.find(condition)
        return tag, int(tag.find(condition_number).div.contents[0])

    @staticmethod
    def north_macedonia(soup):
        def condition(tag):
            if tag is None:
                return False
            return tag.name == 'a' and \
                   'Состојба со COVID-19' in tag.get('title', '')
        tags = soup.find_all(condition)
        assert len(tags) == 1
        return tags[0].parent.parent.parent.parent.parent, None

    @staticmethod
    def poland(soup):
        def condition(tag):
            return tag.name == 'strong' and \
                   len(tag.contents) == 1 and \
                   'osoby zakażone od 4 marca 2020' in tag.contents[0]
        tag = soup.find(condition)
        tag = tag.parent.parent.parent
        number_tag = \
            tag.p.find_next_sibling().find_next_sibling().span.strong.span
        number = number_tag.contents[1].replace(' ', '').replace(',', '')
        return tag, int(number)

    @staticmethod
    def romania(soup):
        def condition(tag):
            return tag.name == 'div' and \
                   ' '.join(tag.get('class', [''])) == \
                   'flex-justify-center widget-body flex-fluid full-width ' \
                   'flex-vertical overflow-y-hidden overflow-x-hidden' and \
                   len(tag.find_all(condition_inner)) > 0
        def condition_inner(tag):
            return tag.name == 'text' and \
                   len(tag.contents) == 1 and \
                   'Total cazuri confirmate' in tag.contents[0]
        tag = soup.find(condition)
        number_tag = \
            tag.div.div.find_next_sibling().g.find_next_sibling().svg.text
        number = number_tag.replace('\n', '').replace(',', '')
        return tag, int(number)

    @staticmethod
    def russia(soup):
        def condition(tag):
            if tag is None:
                return False
            return tag.name == 'div' and \
                   'cv-countdown__item-label' in tag.get('class', '') and \
                   'Выявлено случаев' in tag.contents and \
                   len(tag.contents) == 1
        tags = soup.find_all(condition)
        assert len(tags) == 1
        return tags[0].parent.parent, \
               int(tags[0].find_previous_sibling(
               ).contents[0].contents[0].replace(' ', ''))

    @staticmethod
    def san_marino(soup):
        def condition(tag):
            return tag.name == 'a' and \
                   'Aggiornamento settimanale epidemia COVID-19 e Campagna Vaccinale' in tag.get('title', '')
        def post_condition(tag):
            return tag.name == 'p' and \
                   len(tag.contents) == 1 and \
                   'Il numero totale di persone contagiate individuate ' \
                   'dall’inizio della pandemia fino alla mezzanotte ' \
                   'di ieri è di' in tag.contents[0]
        tag = soup.find(condition)
        url = 'https://www.iss.sm' + tag['href']
        browser.get(url)
        try:
            WebDriverWait(browser, delay).until(
                EC.presence_of_element_located((
                    By.XPATH,
                    "//*[contains(text(), 'Il numero totale di persone "
                    "contagiate individuate dall’inizio della pandemia "
                    "fino alla mezzanotte di ieri è di')]"
                ))
            )
        except TimeoutException:
            logger.warning("The link '%s' has not loaded.", url)
            return tag, None
        post_source = browser.page_source
        post_soup = BeautifulSoup(post_source)
        post_tag = post_soup.find(post_condition)
        cases = re.search(
            'Il numero totale di persone contagiate individuate '
            'dall’inizio della pandemia fino alla mezzanotte '
            'di ieri è di ([0-9.]+)',
            post_tag.contents[0]
        ).group(1).replace('.', '')
        return tag, int(cases)
        

    @staticmethod
    def ukraine(soup):
        def condition(tag):
            if tag is None:
                return False
            return tag.name == 'span' and \
                   'хворих на Covid-19' in tag.contents
        tags = soup.find_all(condition)
        assert len(tags) == 1
        return tags[0].parent.parent, \
               int(tags[0].find_next_sibling(
                   ).contents[0].strip().replace(' ', ''))

    @staticmethod
    def uzbekistan(soup):
        def condition(tag):
            if tag is None:
                return False
            return tag.name == 'p' and \
                   'Всего подтверждено' in tag.contents[0]
        tags = soup.find_all(condition)
        assert len(tags) == 1
        return tags[0].parent.parent.parent, \
               int(tags[0].find_next_sibling()['data-count'])


if __name__ == '__main__':
    try:
        while True:
            user = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) ' \
                'AppleWebKit/605.1.15 (KHTML, like Gecko) ' \
                'Version/13.1 Safari/605.1.15'
            start_time = time.time()
            for country, url in WEBSITES.items():
                t = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
                p = f"data/{country.lower()}_{t}.html"
                if country in WGET_DOWNLOADS:
                    command = f'wget -O "{p}" -U "{user}" --connect-timeout=1 --read-timeout=10 --limit-rate=500K -e robots=off "{url}"'
                    os.system(command)
                elif country in HELIUM_DOWNLOADS:
                    browser.get(url)
                    try:
                        WebDriverWait(browser, delay).until(
                            EC.presence_of_element_located((
                                By.XPATH,
                                XPATHS[country]
                            ))
                        )
                    except TimeoutException:
                        logger.error('Info for %s has not laoded.', country)
                        continue
                    source = browser.page_source
                    with open(p, 'w') as f:
                        logger.debug('Written page source to file %s', p)
                        f.write(source)
                else:
                    logger.error(
                        '%s is not in either of the lists: `WGET_DOWNLOADS`, '
                        '`HELIUM_DOWNLOADS`. Please doublecheck.',
                        country)
                    continue
                if os.stat(p).st_size == 0:
                    os.remove(p)
                ps = sorted([p.name for p in Path('.').iterdir() if p.name.startswith(country.lower())])
                if len(ps) in [0, 1]:
                    continue
                if ps[-1] != p:
                    logger.error('File "%s" has not been saved.', p)
                    continue
                remove_latest_if_page_unchanged(*ps[-2:], country, t)
            full_cycle = time.time() - start_time
            logger.info('CYCLE COMPLETE: %d s', time.time() - start_time)
            # break
            t = datetime.utcnow()
            sleeptime = 60 - (t.second + t.microsecond/1000000.0)
            time.sleep(sleeptime)
            # if int(full_cycle) < 60:
            #     sleep(60 - int(full_cycle))
    except KeyboardInterrupt:
        browser.close()
        sys.exit()
