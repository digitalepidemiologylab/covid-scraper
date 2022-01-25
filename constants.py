WEBSITES = {
    # 'Andorra': 'https://www.govern.ad/coronavirus',
    'Andorra': 'https://www.govern.ad/covid/taula.php',
    'Armenia': 'https://e.infogram.com/71d42d9d-504e-4a8b-a697-f52f4178b329?src=embed',
    'Azerbaijan': 'https://koronavirusinfo.az/az',
    # 'Austria': 'https://covid19-dashboard.ages.at/',
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
    # 'Israel': 'https://datadashboard.health.gov.il/COVID-19/general',  # Hard to load
    'Kosovo': 'https://covid19-rks.net/',  # JS
    # 'Kyrgyzstan': 'http://med.kg/ru/informatsii.html',
    'Kyrgyzstan': 'http://med.kg',
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
    'Portugal': 'https://esriportugal.maps.arcgis.com/apps/dashboards/01bb26e8a53847338f1d508da7e7924a',
    # 'Romania': 'https://instnsp.maps.arcgis.com/apps/dashboards/5eced796595b4ee585bcdba03e30c127',
    'Russia': 'https://стопкоронавирус.рф',
    'San_Marino': 'https://www.iss.sm/on-line/home/archivio-ufficio-stampa-iss.html',
    'Slovakia': 'https://raw.githubusercontent.com/Institut-Zdravotnych-Analyz/covid19-data/main/DailyStats/OpenData_Slovakia_Covid_DailyStats.csv',
    'Spain': 'https://www.mscbs.gob.es/profesionales/saludPublica/ccayes/alertasActual/nCov-China/situacionActual.htm',
    'Switzerland': 'https://www.covid19.admin.ch/en/epidemiologic/case?geo=CH&time=total&rel=abs&geoView=table',
    'Ukraine': 'https://covid19.gov.ua/',
    'United_Kingdom': 'https://coronavirus.data.gov.uk/details/cases?areaType=overview&areaName=United%20Kingdom',
    'Uzbekistan': 'https://coronavirus.uz/ru'
}

POSTS = [
    'Monaco', 'San_Marino'
]

WGET_DOWNLOADS = [
    'Andorra', 'Armenia', 'Azerbaijan', 'Belarus', 'Bulgaria', 'Czechia',
    'France', 'Germany', 'Gibraltar', 'Greece', 'Kyrgyzstan',
    'Luxembourg', 'North_Macedonia', 'Russia', 'Spain',
    'Switzerland', 'Ukraine', 'Uzbekistan'
]

SELENIUM_DOWNLOADS = [
    'Austria', 'Estonia', 'Israel', 'Kosovo', 'Latvia', 'Lithuania', 'Montenegro',
    'Poland', 'Portugal', 'Romania', 'United_Kingdom'
]

CSVS = {
    'Malta': ',',
    'Netherlands': ';',
    'Slovakia': ';',
    'Italy': None
}

DELAY = 15

NUM_RETRIES = 3

XPATHS = {
    'Austria': "//div[@data-key='dpPositivGetestet' and contains(text(), '1.4')]",
    'Estonia': "//div[@class='QFReadout QFUpperBound QFDisabled']",
    'France': "//span[@member='conf_j1' and @class='cellSpan']",
    'Italy': "//*[contains(text(), 'Totale casi')]",
    'Israel': "//h3[contains(text(),'מאומתים חדשים אתמול')]",
    'Kosovo': "//h5[contains(text(),'Raste')]",
    'Latvia': "//span[contains(text(),'Saslimušo skaits')]",
    'Lithuania': "//span[contains(text(),'Iš viso buvusių/esamų atvejų skaičius')]",
    'Montenegro': "//*[//span[contains(text(), 'UKUPAN BROJ OBOLJELIH')] and //div[@class='igc-textual-text innertext']]",
    'Poland': "//strong[contains(text(),'osoby zakażone od 4 marca 2020')]",
    'Portugal': "//div[@class='responsive-text flex-vertical flex-fix allow-shrink indicator-top-text']",
    'Romania': "//*[@style='fill: rgb(230, 0, 0); stroke-width: 2px; font-size: 160px; line-height: normal;']",
    'United_Kingdom': "//a[@id='value-item-people_tested_positive-total-cumcasesbypublishdate-1_modal']"
}

SLEEPS = {
    'Italy': 10,
    'Portugal': 7,
}

LOGGER_BACKUP_COUNT = 20

GENERATED_NUMBERS_PATH = 'logs/numbers_generated.json'
