import json
import pandas as pd
from pathlib import Path
from typing import Dict, List, Text

from giffer import gifware, imgware

NAME = 'symptom'
DATA = Path('data')
FILE = f'covid-spread - {NAME}.csv'
CONFIG = f'{NAME}.json'
SRC = f'{NAME}.png'
SUFFIX = Path(SRC).suffix

# final - bengali, gujurati, hindi, odia, punjabi, urdu, marati
LANG = ['hindi', 'tamil', 'malayalam', 'telugu']


def bake_template(path: Path) -> dict:
    '''Designs the template string from the configuration file.
    Input:
        path: Configuration file
    Returns:
        Template

    eg:
    config
    {
        'num_frames': 2,
        'duration': "[1,3]",
        'tags': {
            'T1': {'frames': [1,2], 'box': [0,0,1,1], 'color': 'black'},
            'T2': {'frames': [2],   'box': [1,1,2,2], 'color': 'black'}
        }
    }

    template:
    {
        '1': [
            {'caption': 'T1', 'box': [0,0,1,1], 'color': 'black'}
        ]
        '2': [
            {'caption': 'T1', 'box': [0,0,1,1], 'color': 'black'},
            {'caption': 'T2', 'box': [1,1,2,2], 'color': 'black'}
        ]
    }

    '''
    config = json.load((path).open('r', encoding='utf-8'))

    vframes = set(frame for _, v in config['tags'].items() for frame in v['frames'])
    template = {
        'meta': {'duration': config['duration']}
    }
    for frame in vframes:
        template[str(frame)] = [{'caption': t, 'box': v['box'], 'fill': v['color']}
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
        template['meta']['lang'] = L

        if SUFFIX == '.gif':
            gifware(f'{DATA}/src/{SRC}', data[L].to_dict(), template, f'{OUT}/{L}.gif')
        else:
            imgware(f'{DATA}/src/{SRC}', data[L].to_dict(), template, f'{OUT}/{L}.png')


if __name__ == '__main__':
    main()
