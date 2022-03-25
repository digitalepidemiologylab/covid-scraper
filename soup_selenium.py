from string import digits

from helpers import only_digits


class SoupSelenium:
    @staticmethod
    def austria(soup):
        def condition(tag):
            if tag is None:
                return False
            return tag.name == 'div' and \
                len(tag.contents) == 1 and \
                'dpPositivGetestet' in tag.get('data-key', []) and \
                'fit' in tag.get('class', [])
        tag = soup.find(condition)
        # print('tag', tag)
        return tag, int(only_digits(tag.contents[0]))

    @staticmethod
    def estonia(soup):
        def condition(tag):
            if tag is None:
                return False
            return tag.name == 'div' and \
                ' '.join(tag.get('class', [])) == 'QFReadout QFUpperBound QFDisabled'
        tag = soup.find(condition)
        return tag.div, int(only_digits(tag.div.text))

    @staticmethod
    def italy(soup):
        def condition(tag):
            if tag is None:
                return False
            return tag.name == 'strong' and \
                'Totale casi' in tag.text
        tags = soup.find_all(condition)
        assert len(tags) == 2
        # print('TAGS')
        # print(tags[0].parent.parent.parent.parent.find_next_sibling())
        # print(tags[1].parent.parent.parent.parent.find_next_sibling())
        tag = tags[0].parent.parent.parent.parent
        number = tag.find_next_sibling().g.find_next_sibling().text
        return tag.parent, int(only_digits(number))

    @staticmethod
    def israel(soup):
        def condition(tag):
            if tag is None:
                return False
            # 'נפטרים מצטבר' in tag.contents[0]  # deaths
            return tag.name == 'h3' and \
                len(tag.contents) == 1 and \
                'אחוז נבדקים חיוביים אתמול' in tag.contents[0]  # percent of positive tests
        tag = soup.find(condition).parent.parent
        number = tag.find_next_sibling().find('h4').text
        return tag, str(number)

    @staticmethod
    def israel_2022_01_30(soup):
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
        number = tag_inner.find_previous_sibling().contents[0]
        return tag_inner.parent, int(only_digits(number))

    @staticmethod
    def kosovo_old(soup):
        def condition(tag):
            if tag is None:
                return False
            return tag.name == 'h5' and \
                len(tag.contents) == 1 and \
                'Raste' in tag.contents[0]
        tags = soup.find_all(condition)
        return tags[1].parent, int(only_digits(tags[1].parent.h3.contents[0]))

    @staticmethod
    def kosovo(soup):
        def condition(tag):
            if tag is None:
                return False
            return tag.name == 'div' and \
                'kpi-label' in tag.get('class', []) and \
                'Gjithsej' in tag.text
        tag = soup.find(condition)
        return tag.parent, int(only_digits(tag.find_next_sibling().text))

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
        ).contents[0]
        return tag.parent.parent, int(only_digits(number))

    @staticmethod
    def lithuania(soup):
        def condition(tag):
            if tag is None:
                return False
            # Before 2022-02-06: 'Iš viso buvusių/esamų atvejų skaičius' in tag.contents[0]
            return tag.name == 'span' and \
                len(tag.contents) == 1 and \
                'Iš viso buvusių/esamų' in tag.contents[0] and \
                'skaičius' in tag.contents[0]
        tag = soup.find(condition)
        number = tag.parent.parent.td.span.contents[0]
        return tag.parent.parent, int(only_digits(number))

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
        return tag, int(only_digits(tag.find(condition_number).div.contents[0]))

    @staticmethod
    def poland(soup):
        def condition(tag):
            # Before 2022-02
            # 'osoby zakażone od 4 marca 2020' in tag.contents[0]
            return tag.name == 'strong' and \
                len(tag.contents) == 1 and \
                'od 4 marca 2020' in tag.contents[0]
        tag = soup.find(condition)
        tag = tag.parent.parent.parent
        number_tag = \
            tag.p.find_next_sibling().find_next_sibling().span.strong.span
        number = number_tag.contents[1]
        return tag, int(only_digits(number))

    @staticmethod
    def portugal(soup):
        def condition(tag):
            return tag.name == 'text' and \
                'Confirmados' in tag.text
        tag = soup.find(condition)
        tag = tag.parent.parent.parent
        number = tag.find_next_sibling().svg.g.find_next_sibling().text
        return tag.parent, int(only_digits(number))

    @staticmethod
    def romania(soup):
        def condition(tag):
            return tag.name == 'div' and \
                ' '.join(tag.get('class', [''])) == \
                'responsive-text flex-vertical flex-fix allow-shrink ' \
                'indicator-top-text' and \
                len(tag.find_all(condition_inner)) > 0
            # 'flex-justify-center widget-body flex-fluid full-width ' \
            # 'flex-vertical overflow-y-hidden overflow-x-hidden' and \

        def condition_inner(tag):
            return tag.name == 'text' and \
                   len(tag.contents) == 1 and \
                   'Total cazuri confirmate' in tag.contents[0]
        tag = soup.find(condition).parent
        number = \
            tag.div.find_next_sibling().g.find_next_sibling().text
        # tag.div.div.find_next_sibling().g.find_next_sibling().svg.text
        return tag, int(only_digits(number))

    @staticmethod
    def united_kingdom(soup):
        def condition(tag):
            if tag is None:
                return False
            return tag.name == 'a' and \
                'value-item-people_tested_positive-total-cumcasesbypublishdate-1_modal' in tag.get('id', '')
        tags = soup.find_all(condition)
        assert len(tags) == 1
        return tags[0], int(only_digits(tags[0].contents[0]))

    # AFRO
    @staticmethod
    def botswana(soup):
        def condition(tag):
            if tag is None:
                return False
            return tag.name == 'div' and \
                'kpi-label' in tag.get('class', []) and \
                'Total Confirmed Botswana Cases' in tag.text
        tag = soup.find(condition)
        total = only_digits(tag.find_next_sibling().text)
        return tag.parent, int(total)

    @staticmethod
    def cape_verde(soup):
        def condition(tag):
            if tag is None:
                return False
            return tag.name == 'svg' and \
                'Nº  de Casos Confirmados' in tag.get('aria-label', '') and \
                '.' in tag.get('aria-label', '') and \
                '(' not in tag.get('aria-label', '')
        tag = soup.find(condition)
        return tag, int(only_digits(tag['aria-label']))

    @staticmethod
    def gabon(soup):
        def condition(tag):
            if tag is None:
                return False
            return tag.name == 'strong' and \
                'CAS CONFIRMÉS' in tag.text
        tag = soup.find(condition).parent.parent.parent
        total = tag.find_next_sibling().text
        return tag.parent, int(only_digits(total))

    @staticmethod
    def gambia(soup):
        def condition(tag):
            if tag is None:
                return False
            return tag.name == 'svg' and \
                'Total Cases' in tag.get('aria-label', '') and \
                '.' in tag.get('aria-label', '')
        tag = soup.find(condition)
        return tag, int(only_digits(tag['aria-label']))

    @staticmethod
    def zambia(soup):
        def condition(tag):
            if tag is None:
                return False
            return tag.name == 'div' and \
                'title text-center' == ' '.join(tag.get('class', [])) and \
                'Total in Zambia' in tag.text
        tag = soup.find(condition)
        total = tag.find_next_sibling().find_next_sibling().h3.text
        return tag, int(only_digits(total))
