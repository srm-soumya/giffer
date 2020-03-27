import cv2
import imageio as io
import numpy as np
import textwrap
from pathlib import Path
from pygifsicle import optimize
from PIL import Image, ImageDraw, ImageFont
from typing import List, Callable, Union

TEXTWRAP = 17  # Decides the wrap size of the text
SIZE = 45
L1,U1,L2,U2 = 140, 260, 30, 38


def rescale(l1: int, u1: int, l2: int, u2: int) -> Callable[[int], int]:
    '''Returns a function that maps range l1 -> u1 to u2 -> l1'''
    denom = (u1 - l1)

    def _inner(n):
        num = (u1 - n) / denom
        return int(num * (u2 - l2)) + l2

    return _inner


def wrapper(text: str, width: Union[int, None] = TEXTWRAP) -> str:
    '''Splits text into smaller sequences'''
    return text if width is None else "\n".join(textwrap.wrap(text, width=width))


def draw_caption(image: Union[np.ndarray, None], data: dict, captions: List[dict], FONT: dict, gif: bool = True) -> np.ndarray:
    '''Draws text on an Image.

    Input:
        image: Image to be modified
        data: tag => language mapping
        captions: List of tags with their metadata
        FONT: font
        gif: Format of the input image

    Returns:
        Image with text drawn on it
    '''
    _image = Image.fromarray(image) if gif else image
    draw = ImageDraw.Draw(_image)
    scale = rescale(L1, U1, L2, U2)

    for c in captions:
        caption = wrapper(data[c['caption']])
        font = ImageFont.truetype(font=str(FONT['family']), size=c['size'])
        size = scale(draw.textsize(caption, font=font)[0])
        size = size if size < SIZE else 70
        if not gif:
            size = c['size']
        font = ImageFont.truetype(font=str(FONT['family']), size=size)
        draw.text(c['point'], caption, fill=c['fill'], font=font)

    return np.array(_image) if gif else _image


def gifware(file: Path, data: dict, template: dict, FONT: dict, save: str = 'test.gif') -> None:
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

    io.mimwrite(save, frames, duration=eval(template['meta']['duration']))
    optimize(str(save))


def imgware(file: Path, data: dict, template: dict, FONT: dict, save: str = 'test.gif') -> None:
    '''Modify the contents of an Image to regional languages.

    Input:
        file: Image input file
        data: tag => language mapping
        template: Instructions on where to position the text
        FONT: Font family
        save: Path to save the modified Image
    '''
    image = Image.open(file).convert('RGBA')
    image = draw_caption(image, data, captions=template["1"], FONT=FONT, gif=False)
    image.save(save, 'PNG')
