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
    'Malta': 'https://raw.githubusercontent.com/COVID19-Malta/COVID19-Data/master/COVID-19%20Malta%20-%20Aggregate%20Data%20Set.csv',
    'Monaco': 'https://www.gouv.mc/Actualites',
    # 'Montenegro': 'https://www.covidodgovor.me/me/statistika',  # JS that wget can't load
    'Montenegro': 'https://e.infogram.com/_/lQ4CDrD827kOcRBewceO?src=embed',
    'Netherlands': 'https://data.rivm.nl/covid-19/COVID-19_aantallen_gemeente_per_dag.csv',
    # 'North_Macedonia': 'http://iph.mk/category/informacii/',  # PDFs with info
    'Poland': 'https://rcb-gis.maps.arcgis.com/apps/dashboards/fc789be735144881a5ea2c011f6c9265',
    # 'Romania': 'https://instnsp.maps.arcgis.com/apps/dashboards/5eced796595b4ee585bcdba03e30c127',
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
    'Luxembourg', 'North_Macedonia', 'Russia', 'Ukraine', 'Uzbekistan'
]

SELENIUM_DOWNLOADS = [
    'Israel', 'Kosovo', 'Latvia', 'Lithuania', 'Montenegro', 'Poland', 'Romania'
]

CSVS = {
    'Malta': ',',
    'Netherlands': ';'
}

DELAY = 15

NUM_RETRIES = 3

XPATHS = {
    'Israel': "//h3[contains(text(),'מאומתים חדשים אתמול')]",
    'Kosovo': "//h5[contains(text(),'Raste')]",
    'Latvia': "//span[contains(text(),'Saslimušo skaits')]",
    'Lithuania': "//span[contains(text(),'Iš viso buvusių/esamų atvejų skaičius')]",
    'Montenegro': "//*[//span[contains(text(), 'UKUPAN BROJ OBOLJELIH')] and //div[@class='igc-textual-text innertext']]",
    'Poland': "//strong[contains(text(),'osoby zakażone od 4 marca 2020')]",
    'Romania': "//*[@style='fill: rgb(230, 0, 0); stroke-width: 2px; font-size: 160px; line-height: normal;']"
}
