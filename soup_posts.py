from inspect import classify_class_attrs
import logging
from logging.handlers import RotatingFileHandler
import re
import unicodedata

from bs4 import BeautifulSoup
from selenium.common.exceptions import TimeoutException

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
options = Options()

from helpers import wait_until_xpath
from constants import LOGGER_BACKUP_COUNT

# Create logger
logger = logging.getLogger('soup_posts')
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

printout_handler = logging.StreamHandler()
writetofile_handler = RotatingFileHandler(
    'logs/log_posts.txt', mode='a', maxBytes=5*1024*1024, 
    backupCount=LOGGER_BACKUP_COUNT, encoding=None, delay=0)

printout_handler.setLevel(logging.INFO)
printout_handler.setFormatter(formatter)
writetofile_handler.setLevel(logging.INFO)
writetofile_handler.setFormatter(formatter)

logger.addHandler(printout_handler)
logger.addHandler(writetofile_handler)


class SoupPosts:
    @classmethod
    def set_browser(cls, browser):
        cls.browser = browser

    @classmethod
    def monaco(cls, soup):
        def condition(tag):
            if tag is None:
                return False
            return tag.name == 'a' and \
                   'Covid-19' in tag.get('title', '') and \
                   ' cas ' in tag.get('title', '')
        def post_condition(tag):
            if tag is None:
                return False
            return tag.name == 'p' and \
                   len(tag.contents) == 1 and \
                   'personnes guéries s’élève' in tag.contents[0]
        tag = soup.find(condition)
        url = 'https://www.gouv.mc' + tag['href']
        # timed_out = wait_until_xpath(
        #     cls.browser, url,
        #     "//*[contains(text(), 'personnes guéries s’élève')]",
        #     logger)
        # if timed_out:
        #     return tag, None
        # post_source = cls.browser.page_source
        # post_soup = BeautifulSoup(post_source, 'html.parser')
        # post_tag = post_soup.find(post_condition)
        # logger.debug('Monaco post tag: %s', post_tag)
        # cases = re.search(
        #     'personnes guéries s’élève [a-zàâçéèêëîïôûùüÿñæœ .-]*([0-9]+)\.',
        #     post_tag.contents[0]
        # ).group(1)
        return tag, url

    @classmethod
    def san_marino(cls, soup):
        def condition(tag):
            if tag is None:
                return False
            keywords = ['aggiornamento', 'epidemia', 'covid-19', 'campagna', 'vaccinale']
            return tag.name == 'a' and \
                all([kw in tag.get('title', '').lower() for kw in keywords])

        def post_condition(tag):
            if tag is None:
                return False
            return tag.name == 'p' and \
                len(tag.contents) == 1 and \
                'Il numero totale di persone contagiate' in tag.contents[0] and \
                'di ieri è di' in tag.contents[0]

        tag = soup.find(condition)
        url = 'https://www.iss.sm' + tag['href']
        # timed_out = wait_until_xpath(
        #     cls.browser, url,
        #     # Changed 2021-01-12
        #     # "//*[contains(text(), 'Il numero totale di persone "
        #     # "contagiate individuate dall’inizio della pandemia "
        #     # "fino alla mezzanotte di ieri è di')]",
        #     "//*[contains(text(), 'Il numero totale di persone contagiate')]",
        #     logger)
        # if timed_out:
        #     cls.browser.close()
        #     cls.browser = webdriver.Firefox(options=options)
        #     logger.info('SoupPosts browser reloaded')
        #     return tag, None
        # post_source = cls.browser.page_source
        # post_soup = BeautifulSoup(post_source, 'html.parser')
        # post_tag = post_soup.find(post_condition)
        # cases = re.search(
        #     # Changed 2021-01-12
        #     # 'Il numero totale di persone contagiate individuate '
        #     # 'dall’inizio della pandemia fino alla mezzanotte '
        #     # 'di ieri è di ([0-9.]+)',
        #     'Il numero totale di persone contagiate .* di ieri è di ([0-9.]+)',
        #     post_tag.contents[0]
        # ).group(1).replace('.', '')
        return url, None

    @classmethod
    def algeria(cls, soup):
        def condition(tag):
            if tag is None:
                return False
            return tag.name == 'a' and \
                'Coronavirus:' in tag.contents[0]
        tag = soup.find(condition)
        url = 'https://www.aps.dz' + tag['href']
        return tag, url

    @classmethod
    def angola(cls, soup):
        def condition(tag):
            if tag is None:
                return False
            return tag.name == 'h2' and \
                'COVID-19' in tag.contents[0]
        tag = soup.find(condition).parent.parent.parent.parent
        url = 'https://governo.gov.ao' + tag['href']
        return tag, url

    @classmethod
    def burkina_faso(cls, soup):
        def condition(tag):
            if tag is None:
                return False
            return tag.name == 'a' and \
                'Maladie à Coronavirus' in tag.get('title', '')
        tag = soup.find(condition)
        url = tag['href']
        return tag, url

    @classmethod
    def comoros(cls, soup):
        def condition(tag):
            if tag is None:
                return False
            return tag.name == 'h5' and \
                'card-title' in tag.get('class', []) and \
                'Pandémie COVID' in tag.text
        tag = soup.find(condition).parent
        url = 'https://stopcoronavirus.km/' + tag.a['href']
        return tag, url

    @classmethod
    def cote_divoire_two(cls, soup):
        def condition(tag):
            if tag is None:
                return False
            return tag.name == 'a' and \
                'Point de la Situation de la COVID-19' in tag.text
        tag = soup.find(condition)
        url = tag['href']
        return tag, url

    @classmethod
    def kenya(cls, soup):
        def condition(tag):
            if tag is None:
                return False
            return tag.name == 'a' and \
                'Press Statement on Covid-19' in tag.text
        tag = soup.find(condition)
        url = tag['href']
        return tag, url

    @classmethod
    def madagascar(cls, soup):
        def condition(tag):
            if tag is None:
                return False
            return tag.name == 'a' and \
                'COVID-19' in unicodedata.normalize(
                    'NFKC', tag.text) and \
                'Situation épidémiologique' in unicodedata.normalize(
                    'NFKC', tag.text)
        tag = soup.find(condition)
        url = tag['href']
        return tag, url

    @classmethod
    def senegal(cls, soup):
        def condition(tag):
            if tag is None:
                return False
            return tag.name == 'a' and \
                'Coronavirus : Communiqué de Presse' in tag.text
        tag = soup.find(condition)
        url = 'https://www.sante.gouv.sn' + tag['href']
        return tag, url

    @classmethod
    def south_africa_one(cls, soup):
        def condition(tag):
            if tag is None:
                return False
            return tag.name == 'h2' and \
                'blog-shortcode-post-title entry-title' in ' '.join(tag.get('class', [])) and \
                'Update on Covid-19' in tag.text
        tag = soup.find(condition)
        url = tag.a['href']
        return tag, url

    @classmethod
    def south_africa_two(cls, soup):
        def condition(tag):
            if tag is None:
                return False
            return tag.name == 'h3' and \
                'elementor-post__title' in tag.get('class', []) and \
                'LATEST CONFIRMED CASES OF COVID-19 IN SOUTH AFRICA' in tag.text
        tag = soup.find(condition)
        url = tag.a['href']
        return tag, url
