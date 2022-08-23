from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException


WEBSITES = {
    # 'Andorra': 'https://www.govern.ad/coronavirus',
    'Andorra': 'https://www.govern.ad/covid/taula.php',
    'Armenia': 'https://e.infogram.com/71d42d9d-504e-4a8b-a697-f52f4178b329?src=embed',
    'Azerbaijan': 'https://koronavirusinfo.az/az',
    # 'Austria': 'https://covid19-dashboard.ages.at/',
    'Austria': 'https://info.gesundheitsministerium.gv.at/data/timeline-faelle-ems.csv',
    'Belarus': 'https://stopcovid.belta.by/',
    'Bulgaria': 'https://coronavirus.bg/bg/',
    'Czechia': 'https://onemocneni-aktualne.mzcr.cz/covid-19',
    # 'Estonia': 'https://www.terviseamet.ee/et/koroonaviiruse-andmestik',
    'Estonia': 'https://tableauapp.tehik.ee/t/TEHIK/views/Est_koroonakaart3/Nakatumine',
    'Germany': 'https://www.rki.de/DE/Content/InfAZ/N/Neuartiges_Coronavirus/Fallzahlen.html',
    'France': 'https://www.data.gouv.fr/fr/datasets/synthese-des-indicateurs-de-suivi-de-lepidemie-covid-19/#resources',
    # 'Gibraltar': 'https://www.gibraltar.gov.gi/covid19',
    'Gibraltar': 'https://healthygibraltar.org/news/update-on-wuhan-coronavirus/',
    'Greece': 'https://eody.gov.gr/category/covid-19/',
    # 'Italy': 'http://opendatadpc.maps.arcgis.com/apps/opsdashboard/index.html#/b0c68bce2cce478eaac82fe38d4138b1',
    'Italy': 'https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-json/dpc-covid19-ita-andamento-nazionale-latest.json',
    'Israel': 'https://datadashboard.health.gov.il/COVID-19/general',  # Hard to load
    # 'Kosovo': 'https://covid19-rks.net/',  # JS
    'Kosovo': 'https://datastudio.google.com/embed/reporting/2e546d77-8f7b-4c35-8502-38533aa0e9e8',
    # 'Kyrgyzstan': 'http://med.kg/ru/informatsii.html',
    'Kyrgyzstan': 'http://med.kg',  # TODO: another scraper
    'Latvia': 'https://spkc.maps.arcgis.com/apps/opsdashboard/index.html#/4469c1fb01ed43cea6f20743ee7d5939',
    'Lithuania': 'https://e.infogram.com/57e5b447-c2ca-40da-aedb-cbf97df68a8e?src=embed',
    'Luxembourg': 'https://data.public.lu/fr/datasets/covid-19-rapports-journaliers/',
    'Malta': 'https://raw.githubusercontent.com/COVID19-Malta/COVID19-Data/master/COVID-19%20Malta%20-%20Aggregate%20Data%20Set.csv',
    'Monaco': 'https://www.gouv.mc/Actualites',
    # 'Montenegro': 'https://www.covidodgovor.me/me/statistika',  # JS that wget can't load
    'Montenegro': 'https://e.infogram.com/_/lQ4CDrD827kOcRBewceO?src=embed',
    'Netherlands': 'https://data.rivm.nl/covid-19/COVID-19_aantallen_gemeente_per_dag.csv',
    'North_Macedonia': 'http://iph.mk/category/informacii/',  # PDFs with info
    'Poland': 'https://rcb-gis.maps.arcgis.com/apps/dashboards/fc789be735144881a5ea2c011f6c9265',
    # 'Portugal': 'https://covid19.min-saude.pt/relatorio-de-situacao/',
    # 'Portugal': 'https://esriportugal.maps.arcgis.com/apps/dashboards/01bb26e8a53847338f1d508da7e7924a',
    # 'Romania': 'https://instnsp.maps.arcgis.com/apps/dashboards/5eced796595b4ee585bcdba03e30c127',
    'Romania': 'https://datelazi.ro/embed/confirmed_cases',
    'Russia': 'https://стопкоронавирус.рф',
    'San_Marino': 'https://www.iss.sm/on-line/home/archivio-ufficio-stampa-iss.html',
    'Slovakia': 'https://raw.githubusercontent.com/Institut-Zdravotnych-Analyz/covid19-data/main/DailyStats/OpenData_Slovakia_Covid_DailyStats.csv',
    'Spain': 'https://www.mscbs.gob.es/profesionales/saludPublica/ccayes/alertasActual/nCov-China/situacionActual.htm',
    'Switzerland': 'https://www.covid19.admin.ch/en/epidemiologic/case?geo=CH&time=total&rel=abs&geoView=table',
    'Ukraine': 'https://covid19.gov.ua/',
    'United_Kingdom': 'https://coronavirus.data.gov.uk/details/cases?areaType=overview&areaName=United%20Kingdom',
    'Uzbekistan': 'https://coronavirus.uz/ru',
    'AFRO_WHO': 'https://covid19.who.int/WHO-COVID-19-global-table-data.csv',
    'Algeria': 'https://www.aps.dz/sante-science-technologie/tag/Minist%C3%A8re%20de%20la%20Sant%C3%A9',
    'Angola': 'https://governo.gov.ao/ao/noticias/saude/',
    # 'Botswana': 'https://datastudio.google.com/embed/reporting/46b5a8f8-1271-498b-bdd2-d325f3f6297f/page/K2uXB',
    'Burkina_Faso': 'https://www.sig.gov.bf/infos-covid-19',
    'Cape_Verde': 'https://app.powerbi.com/view?r=eyJrIjoiY2E3OGUxZjUtYmNkMy00NzUyLTg2ZmMtM2QzYzkxNWY0NDg1IiwidCI6IjdiNWNiZGU0LTI2N2YtNDVmOS05ZWYyLThlOTZmNTViNWFkMSIsImMiOjl9',
    'Comoros': 'https://stopcoronavirus.km/',
    'Cote_dIvoire_One': 'http://info-covid19.gouv.ci/',
    'Cote_dIvoire_Two': 'https://www.sante.gouv.ci/welcome',
    'Equatorial_Guinea': 'https://guineasalud.org/estadisticas/',
    'Ethiopia': 'https://www.moh.gov.et/site/',
    'Gabon': 'https://infocovid.ga/',
    'Gambia': 'https://app.powerbi.com/view?r=eyJrIjoiNGIxZjAxYTYtMzY3Zi00MjU5LWFhYTItZDZmODgzZDI5ZWNjIiwidCI6IjFhMWJjYzBhLTc0ZmQtNDM3YS1hMGI0LWJlMzYzNWIxYmU0OCJ9',
    'Kenya': 'http://www.health.go.ke/press-releases/',
    'Madagascar': 'http://www.sante.gov.mg/ministere-sante-publique/',
    'Nigeria': 'https://covid19.ncdc.gov.ng/',
    'Senegal': 'http://www.sante.gouv.sn/Actualites',
    'Sierra_Leone': 'https://mohs.gov.sl/covid-19/',
    'South_Africa_One': 'https://sacoronavirus.co.za/',
    'South_Africa_Two': 'https://www.nicd.ac.za/media/alerts/',
    # 'Uganda': 'https://covid19.gou.go.ug/',  # TODO: another scraper for it
    'Zambia': 'http://znphi.co.zm/'
}

POSTS = [
    'Monaco', 'San_Marino',
    'Algeria', 'Angola', 'Comoros', 'Cote_dIvoire_Two', 'Burkina_Faso',
    'Kenya', 'Madagascar', 'Senegal', 'South_Africa_One', 'South_Africa_Two'
]

WGET_DOWNLOADS = [
    'Andorra', 'Armenia', 'Azerbaijan', 'Belarus', 'Bulgaria', 'Czechia',
    'France', 'Germany', 'Gibraltar', 'Greece', 'Kyrgyzstan',
    'Luxembourg', 'North_Macedonia', 'Romania', 'Russia', 'Spain',
    'Switzerland', 'Ukraine', 'Uzbekistan'
]

WGET_DOWNLOADS_AFRO = [
    'Cote_dIvoire_One', 'Equatorial_Guinea', 'Ethiopia', 'Nigeria',
    'Sierra_Leone', 'Uganda'
]

SELENIUM_DOWNLOADS = [
    'Latvia', 'Lithuania', 'Montenegro',
    'Poland', 'Portugal', 'United_Kingdom'
]

SELENIUM_DOWNLOADS_2 = [
    'Estonia', 'Israel', 'Kosovo'
]

SELENIUM_DOWNLOADS_AFRO = [
    'Botswana', 'Cape_Verde', 'Gambia', 'Gabon', 'Zambia'
]

CSVS = {
    'Austria': ';',
    'Malta': ',',
    'Netherlands': ';',
    'Slovakia': ';',
    'Italy': None
}

CSVS_AFRO_WHO = [
    'Chad', 'Eswatini', 'Lesotho', 'Malawi', 'Mali', 'Mauritius', 'Namibia',
    'Nigerr', 'Seychelles', 'Zimbabwe', 'Botswana', 'Uganda'
]

DELAY = 15

NUM_RETRIES = 2

XPATHS = {
    'Austria': "//div[@data-key='dpPositivGetestet' and contains(text(), '1.4')]",
    'Estonia': "//div[@class='QFReadout QFUpperBound QFDisabled']",
    'France': "//span[@member='conf_j1' and @class='cellSpan']",
    'Italy': "//*[contains(text(), 'Totale casi')]",
    # 'Israel': "//h3[contains(text(),'מאומתים חדשים אתמול')]",
    # 'Israel': "//h3[contains(text(),'נפטרים מצטבר')]",  # deaths
    'Israel': "//h3[contains(text(),'אחוז נבדקים חיוביים אתמול')]",
    # 'Kosovo': "//h5[contains(text(),'Raste')]",
    'Kosovo': "//*[text()='\n      Gjithsej\n  ']",
    'Latvia': "//span[contains(text(),'Saslimušo skaits')]",
    # 'Lithuania': "//span[contains(text(),'Iš viso buvusių/esamų atvejų skaičius')]",
    'Lithuania': "//span[contains(text(),'Iš viso buvusių/esamų')]",
    'Montenegro': "//*[//span[contains(text(), 'UKUPAN BROJ OBOLJELIH')] and //div[@class='igc-textual-text innertext']]",
    # 'Poland': "//strong[contains(text(),'osoby zakażone od 4 marca 2020')]",
    'Poland': "//strong[contains(text(),'od 4 marca 2020')]",
    'Portugal': "//div[@class='responsive-text flex-vertical flex-fix allow-shrink indicator-top-text']",
    'Romania': "//*[@style='fill: rgb(230, 0, 0); stroke-width: 2px; font-size: 160px; line-height: normal;']",
    'United_Kingdom': "//a[@id='value-item-people_tested_positive-total-cumcasesbypublishdate-1_modal']",
    'Botswana': "//div[contains(text(), 'Total Confirmed Botswana Cases')]",
    'Cape_Verde': "//*[contains(@aria-label, 'Nº  de Casos Confirmados') and contains(@aria-label, '.')]",
    'Gabon': "//strong[contains(text(), 'CAS CONFIRMÉS')]",
    'Gambia': "//*[contains(@aria-label, 'Total Cases') and contains(@aria-label, '.')]",
    'Zambia': "//*"
}

SLEEPS = {
    'Italy': 10,
    'Kosovo': 4,
    'Portugal': 15,
    'Cape_Verde': 5,
    'Zambia': 4
}

LOG_FILES = [
    'log_wgets.txt', 'log_wgets_afro.txt',
    'log_selenium.txt', 'log_selenium_2.txt', 'log_selenium_afro.txt',
    'log_posts.txt', 'log_csvs.txt', 'log_csvs_afro_who.txt'
]

LOGGER_BACKUP_COUNT = 20

GENERATED_NUMBERS_PATH = 'logs/numbers_generated.json'


def before_wait_israel(browser):
    try:
        element = WebDriverWait(browser, 5).until(
            EC.presence_of_element_located((
                By.XPATH,
                "//div[@class='btn-x-close']"
            ))
        )
        button = element.find_element_by_css_selector('button')
        button.click()
    except TimeoutException:
        pass


def before_wait_gabon(browser):
    try:
        element = WebDriverWait(browser, 5).until(
            EC.presence_of_element_located((
                By.XPATH,
                "//*[contains(text(), 'Tout refuser')]"
            ))
        )
        element.click()
    except TimeoutException:
        pass


BEFORE_WAIT = {
    'Israel': before_wait_israel,
    'Gabon': before_wait_gabon
}
