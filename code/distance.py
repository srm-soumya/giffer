import pandas as pd
from pathlib import Path

from giffer import giffer, wrapper

DATA = Path('data')
OUT = Path('out')

# final - bengali, gujurati, hindi, odia, punjabi, urdu, telugu

LANG = ['telugu']


def read_data(file: str) -> pd.DataFrame:
    '''Read a file using pandas'''
    return pd.read_csv(DATA/file, index_col='language', skiprows=[1])


def make_content(S: pd.Series) -> dict:
    return {
        "27": {
            'captions': [
                {'caption': wrapper(S.T1), 'point': (510, 300), 'fill': (
                    0, 0, 0), 'font_size': int(S.weight)}
            ]},
        "29": {
            'captions': [
                {'caption': wrapper(S.T2), 'point': (190, 100), 'fill': (
                    0, 0, 0), 'font_size': int(S.weight)}
            ]},
        "30": {
            'captions': [
                {'caption': wrapper(S.T2), 'point': (190, 100), 'fill': (
                    0, 0, 0), 'font_size': int(S.weight)},
                {'caption': wrapper(S.T3), 'point': (525, 100), 'fill': (
                    0, 0, 0), 'font_size': int(S.weight)}
            ]},
        "31": {
            'captions': [
                {'caption': wrapper(S.T2), 'point': (190, 100), 'fill': (
                    0, 0, 0), 'font_size': int(S.weight)},
                {'caption': wrapper(S.T3), 'point': (525, 100), 'fill': (
                    0, 0, 0), 'font_size': int(S.weight)},
                {'caption': wrapper(S.T4), 'point': (415, 560), 'fill': (
                    0, 0, 0), 'font_size': int(S.weight)}
            ]},
        "32": {
            'captions': [
                {'caption': wrapper(S.T2), 'point': (190, 100), 'fill': (
                    0, 0, 0), 'font_size': int(S.weight)},
                {'caption': wrapper(S.T3), 'point': (525, 100), 'fill': (
                    0, 0, 0), 'font_size': int(S.weight)},
                {'caption': wrapper(S.T4), 'point': (415, 560), 'fill': (
                    0, 0, 0), 'font_size': int(S.weight)},
                {'caption': wrapper(S.T5), 'point': (820, 640), 'fill': (
                    0, 0, 0), 'font_size': int(S.weight)}
            ]},
        "33": {
            'captions': [
                {'caption': wrapper(S.T2), 'point': (190, 100), 'fill': (
                    0, 0, 0), 'font_size': int(S.weight)},
                {'caption': wrapper(S.T3), 'point': (525, 100), 'fill': (
                    0, 0, 0), 'font_size': int(S.weight)},
                {'caption': wrapper(S.T4), 'point': (415, 560), 'fill': (
                    0, 0, 0), 'font_size': int(S.weight)},
                {'caption': wrapper(S.T5), 'point': (820, 640), 'fill': (
                    0, 0, 0), 'font_size': int(S.weight)}
            ]},
    }


def process():
    df = read_data('covid-spread - social-distance.csv')

    for L in LANG:
        print(f'Creating {L}.gif')
        FONT = {'family': DATA/'fonts'/'indic'/f'{L}.ttf'}
        giffer(f'{DATA}/gifs/distance.gif',
               make_content(df[L]), FONT, f'{OUT}/{L}.gif')


if __name__ == '__main__':
    process()
