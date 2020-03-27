import json
import pandas as pd
from pathlib import Path
from typing import Dict, List, Text

from giffer import gifware, imgware

DATA = Path('data')
FILE = 'covid-spread - social-distance.csv'
CONFIG = 'covid_spread.json'
SRC = 'covid_spread.gif'
SUFFIX = Path(SRC).suffix

# final - bengali, gujurati, hindi, odia, punjabi, urdu, marati
LANG = ['hindi', 'odia']


def bake_template(path: Path) -> dict:
    '''Designs the template string from the configuration file.
    Input:
        path: Configuration file
    Returns:
        Template

    eg:
    config
    {
        'num_frames': 2
        'tags': {
            'T1': [1,2], 'point': [0,0]
            'T2': [2],   'point': [1,1]
        }
    }

    template:
    {
        '1': [
            {'caption': 'T1', 'point': [0,0]}
        ]
        '2': [
            {'caption': 'T1', 'point': [0,0]},
            {'caption': 'T2', 'point': [1,1]}
        ]
    }

    '''
    config = json.load((path).open('r', encoding='utf-8'))

    vframes = set(frame for _, v in config['tags'].items() for frame in v['frames'])
    template = {
        'meta': {'duration': config['duration']}
    }
    for frame in vframes:
        template[str(frame)] = [{'caption': t, 'point': v['point'], 'fill': v['color'], 'size': v['size']}
                                for t, v in config['tags'].items() if frame in v['frames']]

    return template


def main():
    '''Runs the code for each language & generated a modified SRC for the same.'''
    data = pd.read_csv(DATA/FILE, index_col='language', skiprows=[1])
    template = bake_template(DATA/CONFIG)

    OUT = Path('out')/'gif' if SUFFIX == '.gif' else Path('out')/'image'
    OUT.mkdir(exist_ok=True)

    for L in LANG:
        print(f'Creating {L}{SUFFIX}')
        FONT = {'family': DATA/'fonts'/'indic'/f'{L}.ttf'}

        if SUFFIX == '.gif':
            gifware(f'{DATA}/src/{SRC}', data[L].to_dict(), template, FONT, f'{OUT}/{L}.gif')
        else:
            imgware(f'{DATA}/src/{SRC}', data[L].to_dict(), template, FONT, f'{OUT}/{L}.png')


if __name__ == '__main__':
    main()
