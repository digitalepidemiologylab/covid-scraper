import re

from helpers import only_digits


class SoupWgets:
    @staticmethod
    def andorra(soup):
        def condition(tag):
            if tag is None:
                return False
            return tag.name == 'div' and \
                'col-2' in tag.get('class', []) and \
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
        # assert len(tags) == 2
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
                'div').contents[0].contents[0].replace(' ', ''))

    @staticmethod
    def bulgaria(soup):
        def condition(tag):
            if tag is None:
                return False
            return tag.name == 'p' and \
                'statistics-value' in tag.get('class', []) and \
                'confirmed' in tag.get('class', []) and \
                len(tag.contents) == 1
        tag = soup.find(condition)
        return tag, int(tag.contents[0])

    @staticmethod
    def czechia(soup):
        def condition(tag):
            if tag is None:
                return False
            return tag.name == 'p' and \
                'mb-0 text--center' == ' '.join(tag.get('class', [''])) and \
                len(tag.contents) == 1 and \
                tag.contents[0] == 'Potvrzené případy'
        tag = soup.find(condition)
        return tag.parent, \
            int(tag.find_next_sibling(
            ).find(
                'span', attrs={'id': 'count-sick'}
            ).contents[0].replace(u'\xa0', ''))

    @staticmethod
    def france(soup):
        def condition(tag):
            if tag is None:
                return False
            return tag.name == 'h4' and \
                'table-indicateurs-open-data-france' in tag.text
        tags = soup.find_all(condition)
        assert len(tags) == 1
        return tags[0].text.replace(' ', '').replace('\n', ''), None

    @staticmethod
    def germany(soup):
        def condition(tag):
            if tag is None:
                return False
            return tag.name == 'strong' and \
                'Gesamt' == tag.text
        tag = soup.find(condition)
        tag = tag.parent.find_next_sibling()
        # Before 2022-01-26
        # return tag, int(tag.strong.text.replace('.', ''))
        return tag, int(only_digits(tag.text))

    @staticmethod
    def gibraltar_before_2021_11_20_17_24_02(soup):
        def condition(tag):
            if tag is None:
                return False
            return tag.name == 'li' and \
                'Confirmed cases:' in tag.contents[0]
        tags = soup.find_all(condition)
        assert len(tags) == 1
        return tags[0].parent, int(tags[0].contents[0][17:])

    @staticmethod
    def gibraltar_before_2021_12_12_14_41_04(soup):
        def condition_recovered(tag):
            if tag is None:
                return False
            return tag.name == 'li' and \
                'Recovered cases:' in tag.contents[0]

        def condition_active(tag):
            if tag is None:
                return False
            return tag.name == 'li' and \
                'Active cases in Gibraltar' in tag.contents[0]

        def condition_deaths(tag):
            if tag is None:
                return False
            return tag.name == 'li' and \
                'Deaths' in tag.contents[0]
        tags_recovered = soup.find_all(condition_recovered)
        tags_active = soup.find_all(condition_active)
        tags_deaths = soup.find_all(condition_deaths)
        assert len(tags_recovered) == 1
        assert len(tags_active) == 1
        assert len(tags_deaths) == 1
        total_cases = int(tags_recovered[0].contents[0][17:]) + \
            int(tags_active[0].contents[2].split('(')[0][2:]) + \
            int(tags_deaths[0].contents[0][8:])
        return tags_recovered[0].parent, total_cases

    @staticmethod
    def gibraltar(soup):
        def condition_recovered(tag):
            if tag is None:
                return False
            return tag.name == 'li' and \
                'Recovered cases:' in tag.contents[0]

        def condition_active(tag):
            if tag is None:
                return False
            return tag.name == 'li' and \
                'Active cases in Gibraltar' in tag.contents[0]

        def condition_deaths(tag):
            if tag is None:
                return False
            return tag.name == 'li' and \
                'Deaths' in tag.contents[0]
        tags_recovered = soup.find_all(condition_recovered)
        tags_active = soup.find_all(condition_active)
        tags_deaths = soup.find_all(condition_deaths)
        assert len(tags_recovered) == 1
        assert len(tags_active) == 1
        assert len(tags_deaths) == 1
        total_cases = int(only_digits(tags_recovered[0].contents[0][17:])) + \
            int(only_digits(tags_active[0].contents[2].split('(')[0][2:])) + \
            int(only_digits(tags_deaths[0].contents[0][8:].split(' ')[0]))
        return tags_recovered[0].parent, total_cases

    @staticmethod
    def greece(soup):
        def condition(tag):
            if tag is None:
                return False
            return tag.name == 'a' and \
                'Ημερήσια έκθεση επιτήρησης COVID-19' in tag.get('aria-label', '')
        tag = soup.find(condition)
        return tag['aria-label'], None

    @staticmethod
    def kyrgyzstan_before_2021_01_12_9_15_00(soup):
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
        return tag.tbody, cases[0]

    @staticmethod
    def kyrgyzstan(soup):
        def condition(tag):
            if tag is None:
                return False
            return tag.name == 'h4' and \
                'Всего' in tag.text
        tag = soup.find(condition)
        covid_1 = tag.parent.parent.find_next_sibling().find_next_sibling().div
        covid_2 = covid_1.find_next_sibling()
        cases = int(covid_1.h4.text) + int(covid_2.h4.text)
        return tag.parent.parent, cases

    @staticmethod
    def luxembourg(soup):
        def condition(tag):
            if tag is None:
                return False
            return tag.name == 'article' and \
                'card' in tag.get('class', []) and \
                'resource-card' in tag.get('class', [])
        tag = soup.find(condition)
        return tag.div.h4.contents[0], None

    @staticmethod
    def north_macedonia(soup):
        def condition(tag):
            if tag is None:
                return False
            return tag.name == 'a' and \
                'податоци за covid-19' in tag.get('title', '').lower()
        tag = soup.find(condition)
        return tag, None

    @staticmethod
    def portugal(soup):
        def condition(tag):
            if tag is None:
                return False
            return tag.name == 'a' and \
                len(tag.contents) == 1 and \
                'Relatório de Situação nº' in tag.text
        tag = soup.find(condition)
        return tag.text, None

    @staticmethod
    def spain(soup):
        def condition(tag):
            if tag is None:
                return False
            return tag.name == 'div' and \
                'banner-coronavirus banner-verde' == ' '.join(tag.get('class', ['']))
        tag = soup.find(condition)
        return tag, int(tag.find('p', {'class': 'cifra'}).text.replace('.', ''))

    @staticmethod
    def romania(soup):
        def condition(tag):
            if tag is None:
                return False
            return tag.name == 'h3' and \
                tag.get('id', '') == 'chart-label-confirmed_cases'
        tag = soup.find(condition)
        return tag, int(only_digits(tag.text))

    @staticmethod
    def russia(soup):
        def condition(tag):
            if tag is None:
                return False
            # Change since 2022-01-20 11:24:23
            # 'Выявлено случаев' = total cases -> 'Выявлено' = daily cases
            return tag.name == 'div' and \
                'cv-countdown__item-label' in tag.get('class', []) and \
                len(tag.contents) == 1 and \
                (
                    'Выявлено' in tag.contents or
                    'Выявлено случаев' in tag.contents
                )
        tags = soup.find_all(condition)
        # assert len(tags) == 1
        return tags[0].parent.parent, \
            int(tags[0].find_previous_sibling(
            ).contents[0].contents[0].replace(' ', ''))

    @staticmethod
    def switzerland(soup):
        def condition(tag):
            if tag is None:
                return False
            return tag.name == 'th' and \
                tag.get('class', [''])[0] == 'detail-card-geography-table__title-cell' and \
                len(tag.contents) == 1 and \
                tag.contents[0] == 'Switzerland'
        tag = soup.find(condition)
        number_tag = tag.find_next_sibling().find_next_sibling()
        number = number_tag.contents[0].replace(' ', '')
        return tag.parent, int(number)

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

    # AFRO
    @staticmethod
    def cote_divoire_one(soup):
        def condition(tag):
            if tag is None:
                return False
            return tag.name == 'div' and \
                'alert alert-danger alert-dismissible fade show cas' in ' '.join(tag.get('class', [])) and \
                'Cas Confirmés' in tag.text
        tag = soup.find(condition)
        total = tag.strong.text
        return tag, int(only_digits(total))

    @staticmethod
    def equatorial_guinea(soup):
        def condition(tag):
            if tag is None:
                return False
            return tag.name == 'b' and \
                'Casos confirmados' == tag.text
        tag = soup.find(condition).parent.parent
        total = tag.find_next_sibling().find_next_sibling().find_next_sibling().text
        return tag, int(only_digits(total))

    @staticmethod
    def ethiopia(soup):
        def condition(tag):
            if tag is None:
                return False
            return tag.name == 'div' and \
                'highlight-body' in tag.get('class', []) and \
                'Total Cases' == tag.text
        tag = soup.find(condition).parent
        return tag, int(only_digits(tag.div.text))

    @staticmethod
    def nigeria(soup):
        def condition(tag):
            if tag is None:
                return False
            return tag.name == 'h6' and \
                'text-white' in tag.get('class', []) and \
                'Confirmed Cases' in tag.text
        tag = soup.find(condition).parent
        total = tag.h2.text
        return tag, int(only_digits(total))

    @staticmethod
    def sierra_leone(soup):
        def condition(tag):
            if tag is None:
                return False
            return tag.name == 'span' and \
                'exad-corona-label' in tag.get('class', []) and \
                'Cases:' in tag.text
        tag = soup.find(condition)
        total = tag.find_next_sibling().text
        return tag.parent, int(only_digits(total))

    @staticmethod
    def uganda(soup):
        def condition(tag):
            if tag is None:
                return False
            return tag.name == 'h5' and \
                'mb-0 f18 txt-color' in ' '.join(tag.get('class', [])) and \
                'CUMULATIVE CASES' in tag.text
        tag = soup.find(condition).parent
        total = tag.h2.text
        return tag.parent, int(only_digits(total))
