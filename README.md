# COVID-19 Scraper

The scraper is created for the project a goal of which is to compare the times that the info on the COVID-19 cases and deaths is being updated **on official websites vs official social media** of the governments of countries around the world.

## Data loading categories

This scraper does not support social media (esp. Facebook which is difficult to scrape). As for the websites, there are 4 main categories:
- Websites with little to no JS
    - Loaded using `wget`
- Websites (esp. dashboards) with heavy JS
    - Loaded using `selenium` (Firefox driver that loads the page as if it were being opened in a browser)
- Websites with the info updated in a feed (which is usually a mixed feed, which means not only the COVID-19 stats get published there)
    - The feed is loaded using `wget`, then the contents of the relevant posts are loaded with `selenium`
- CSV tables
    - Loaded with `wget`

## Pipeline

The general pipeline looks like this.

(Its aim is to identify timestamps at which websites are updated with the new COVID-19 related info.)

First, the source is loaded following one of the above methods. Second, the contents are processed to identify the part relevant to reporting COVID-19 cases (deaths) in the HTML/CSV. Third, the contents of the newly downloaded website are compared to a previous download (both the outer relevant tag and the numbers, where applicable). Finally, if the contents match, the new download is deleted, and if not, preserved, with the timestamp and numbers written to `data/logs/numbers.json`.

For processing HTML, I use [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/), and for the CSVs, [pandas](https://pandas.pydata.org).

## Structure

The structure of the scripts is as follows.
- `constants.py`: constants needed around the other scripts
- `check_logs.py`: checks logs for periods of inactivity of the scraper
- `generate_numbers.py`: generates `data/logs/numbers_generated.json` using the collected HTML files in `data`
- `helpers.py`: helper functions
- `log_watcher.py`: monitors the logs and sends emails in case of errors (uses [AWS SES](https://aws.amazon.com/ses/))
- `move_files.py`: helps moving files to separate folders by country when they pile up (for storing)
- `scraper_fix.py`: helps manually fixing processing exceptions
    - E.g. when a website changes whe way they present the data, the parser fails, and a processing exception occurs that needs to be manually fixed.
- Helper classes
    - `soup_wgets.py`: `SoupWgets` class with static methods that process HTML for each country
    - `soup_selenium.py`: `SoupSelenium` class with static methods that process HTML for each country
    - `soup_posts.py`: `SoupPosts` class with class methods that process HTML for each country, click the relevant post, and process the post to get the info
    - `pandas_csvs.py`: `Csv` class with static methods that process CSV for each country
- Scraper scripts: `scraper_wgets.py`, `scraper_selenium.py`, `scraper_posts.py`, `scraper_csvs.py`
- `data`: saved sources
- `logs`: logs for each scraper
    - `numbers_generated.json`: the latest output of `generate_numbers.py`
        - It's more reliable than `numbers.json` bc this file is generated after manually dealing with all processing exceptions.
    - `numbers.json`: the file datetime info is automatically written to in the process of scraping (lacks processing exceptions)

## Installation

```bash
git clone https://github.com/digitalepidemiologylab/covid-scraper.git
cd covid-scraper
pip install -r requirements.txt
```

## Launching

I use a separate tmux screen for each scraper, and another one for the log watcher.