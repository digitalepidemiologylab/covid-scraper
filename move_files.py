from datetime import datetime
import os
from pathlib import Path

from constants import WEBSITES
from helpers import Filename


if __name__ == '__main__':
    datetime_min = datetime(2021, 11, 9, 10, 30)
    datetime_max = datetime(2021, 11, 14, 11, 30)
    for country in WEBSITES.keys():
        ps = sorted([
            p.name
            for p in Path('data').iterdir()
            if p.name.startswith(f'{country.lower()}_') and
            Filename(p).in_between(datetime_min, datetime_max)])
        try:
            os.mkdir(f'data/{country.lower()}')
        except FileExistsError:
            continue
        for p in ps:
            os.rename(os.path.join(f'data', p), os.path.join(f'data/{country.lower()}', p))
        print(f'Moved files for {country}')
        