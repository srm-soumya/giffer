import cv2
import imageio as io
import numpy as np
import textwrap
from pathlib import Path
from pygifsicle import optimize
from PIL import Image, ImageDraw, ImageFont
from typing import List, Callable

TEXTWRAP = 15  # Decides the wrap size of the text
DURATION = [0.12] * 26 + [1] + [1] + [0.5] + [2.5] * 4 # Decides the duration a particular frame stays in vision
L1,U1,L2,U2 = 140, 260, 28, 38


def rescale(l1: int, u1: int, l2: int, u2: int) -> Callable[[int], int]:
    '''Returns a function that maps range l1 -> u1 to u2 -> l1'''
    denom = (u1 - l1)

    def _inner(n):
        num = (u1 - n) / denom
        return int(num * (u2 - l2)) + l2

    return _inner


def wrapper(text: str, width: int = TEXTWRAP) -> str:
    '''Splits text into smaller sequences'''
    return "\n".join(textwrap.wrap(text, width=width))


def draw_caption(image: np.ndarray, data: dict, captions: List[dict], FONT: dict) -> np.ndarray:
    '''Draws text on an Image.

    Input:
        image: Image to be modified
        data: tag => language mapping
        captions: List of tags with their metadata
        FONT: font
        scale: Mapper to decide on the actual printed size of the text

    Returns:
        Image with text drawn on it
    '''
    _image = Image.fromarray(image)
    draw = ImageDraw.Draw(_image)
    scale = rescale(L1, U1, L2, U2)

    for c in captions:
        caption = wrapper(data[c['caption']])
        font = ImageFont.truetype(font=str(FONT['family']), size=30)
        size = scale(draw.textsize(caption, font=font)[0])
        size = size if size <= 40 else 100
        font = ImageFont.truetype(font=str(FONT['family']), size=size)
        draw.text(c['point'], caption, fill=c['fill'], font=font)

    return np.array(_image)


def giffer(file: Path, data: dict, template: dict, FONT: dict, save: str = 'test.gif') -> None:
    '''Modify the contents of a GIF to regional languages.

    Input:
        file: GIF input file
        data: tag => language mapping
        template: Instructions on where to position the text
        FONT: Font family
        save: Path to save the modified GIF
    '''
    gif = io.mimread(file)
    frames = []

    for (i, frame) in enumerate(gif):
        frame = cv2.cvtColor(frame, cv2.COLOR_RGBA2RGB)
        if str(i) in template:
            frame = draw_caption(frame, data, captions=template[str(i)], FONT=FONT)

        frames.append(frame)

    io.mimwrite(save, frames, duration=DURATION)
    optimize(str(save))
