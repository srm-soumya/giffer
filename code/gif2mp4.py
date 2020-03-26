import subprocess
from pathlib import Path


def process(folder: Path):
    for gif in folder.glob('*.gif'):
        subprocess.call(
            f'ffmpeg -i {folder/gif.stem}.gif -movflags faststart -pix_fmt yuv420p -vf "scale=trunc(iw/2)*2:trunc(ih/2)*2" {folder/gif.stem}.mp4', shell=True)


if __name__ == '__main__':
    process(Path('out'))
