import sys
import imageio as io
from pathlib import Path


def split_and_store(path: str):
    '''Splits the GIS into its individual components.'''
    f = Path(path)
    Path(f'{f.parent}/frames').mkdir(exist_ok=True)

    for (i,frame) in enumerate(io.mimread(f)):
        io.imwrite(f'{f.parent}/frames/{f.stem}_{i}.tiff', frame)


if __name__ == "__main__":
    split_and_store(sys.argv[1])
