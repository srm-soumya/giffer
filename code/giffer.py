import cv2
import imageio as io
import numpy as np
import textwrap
from pathlib import Path
from pygifsicle import optimize
from PIL import Image, ImageDraw, ImageFont
from typing import List, Callable
import pdb


def rescale(l1, u1, l2, u2):
    denom = (u1 - l1)

    def _inner(n):
        num = (u1 - n) / denom
        return int(num * (u2 - l2)) + l2

    return _inner


def wrapper(text: str, width: int = 17) -> str:
    '''Splits text into smaller sequences'''
    return "\n".join(textwrap.wrap(text, width=width))


def draw_caption(image: np.ndarray, captions: List[dict], F: dict, scale: Callable[[int], int]) -> np.ndarray:
    '''Adds captions as text on an Image'''
    _image = Image.fromarray(image)
    draw = ImageDraw.Draw(_image)

    for c in captions:
        font = ImageFont.truetype(font=str(F['family']), size=c['font_size'])
        size = scale(draw.textsize(c['caption'], font=font)[0])
        size = size if size <= 40 else 100
        font = ImageFont.truetype(font=str(F['family']), size=size)
        draw.text(c['point'], c['caption'], fill=c['fill'], font=font)

    return np.array(_image)


def giffer(file: Path, content: dict, F: dict, save: str = 'test.gif') -> None:
    '''Read a GIF, add the captions from the content & save the new GIF'''
    gif = io.mimread(file)
    frames = []
    scale = rescale(140, 260, 25, 38)

    for (i, frame) in enumerate(gif):
        idx = str(i)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGBA2RGB)
        if idx in content:
            frame = draw_caption(
                frame, captions=content[idx]['captions'], F=F, scale=scale)

        frames.append(frame)

    io.mimwrite(save, frames, duration=[0.12]*26 + [1] + [1] + [0.5] + [3]*4)
    optimize(str(save))
