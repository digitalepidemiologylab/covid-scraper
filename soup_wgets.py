import re
import logging

from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException

class SoupWgets:
    @staticmethod
    def andorra(soup, browser=None):
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
    def armenia(soup, browser=None):
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
    def azerbaijan(soup, browser=None):
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
    def belarus(soup, browser=None):
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
    def gibraltar(soup, browser=None):
        def condition(tag):
            if tag is None:
                return False
            return tag.name == 'li' and \
                   'Confirmed cases:' in tag.contents[0]
        tags = soup.find_all(condition)
        assert len(tags) == 1
        return tags[0].parent, int(tags[0].contents[0][17:])

    @staticmethod
    def kyrgyzstan(soup, browser=None):
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
    def luxembourg(soup, browser=None):
        def condition(tag):
            return tag.name == 'article' and \
                   'card' in tag.get('class', []) and \
                   'resource-card' in tag.get('class', [])
        tag = soup.find(condition)
        return tag.div.h4.contents[0], None

    @staticmethod
    def north_macedonia(soup, browser=None):
        def condition(tag):
            if tag is None:
                return False
            return tag.name == 'a' and \
                   'Состојба со COVID-19' in tag.get('title', '')
        tags = soup.find_all(condition)
        assert len(tags) == 1
        return tags[0].parent.parent.parent.parent.parent, None

    @staticmethod
    def russia(soup, browser=None):
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
    def ukraine(soup, browser=None):
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
    def uzbekistan(soup, browser=None):
        def condition(tag):
            if tag is None:
                return False
            return tag.name == 'p' and \
                   'Всего подтверждено' in tag.contents[0]
        tags = soup.find_all(condition)
        assert len(tags) == 1
        return tags[0].parent.parent.parent, \
               int(tags[0].find_next_sibling()['data-count'])
