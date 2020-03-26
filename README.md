# Giffer : Templatize GIFs.

### Why?

This code is to setup to create Multilingual GIFs for increasing the awareness of COVID-19 pandemic. 

### Dependencies:

    For Ubuntu, use `conda env create -f environment.yml`.
    For Windows, most of the code setup should work. Will soon update with `yml` file.

### How to run?

Navigate to code and run `distance.py`. This reads a csv file and calls `giffer` function with a base template and content with its structure (`frame numbers & content`).

### How it Works?

We write on a GIF with empty template. For example, look at `data/gifs/distance.gif`.

For text-overflow issues, we use `textwrapper` library.

We divide the GIF into frames and enter information at particular frames. For example, 

        content = {
        "27": {
            'captions': [
                {'caption': wrapper(OC0), 'point': (475, 275), 'fill': (0,0,0), 'font_size': 150}
        ]},
        "30": {
            'captions': [
                {'caption': wrapper(OC1), 'point': (190, 100), 'fill': (0,0,0), 'font_size': 30},
                {'caption': wrapper(OC2), 'point': (525, 100), 'fill': (0,0,0), 'font_size': 30}
        ]}
                }


Here `27, 33` are frame numbers. `point` is where you start writing the content.
