# Giffer : Templatize GIFs.

### Why?

This code is to setup to create Multilingual GIFs for increasing the awareness of COVID-19 pandemic. 

### Dependencies:

For Ubuntu, use `conda env create -f environment.yml`.
For Windows, most of the code setup should work. Will soon update with `yml` file.

### How to run?

Navigate to code and run `make`. This reads a csv file and calls `giffer` function with a base template and content with its structure (`frame numbers & content`).

### How it Works?

We write on a GIF with empty template. For example, look at `data/gifs/covid_spread.gif`.

For text-overflow issues, we use `textwrapper` library.

We divide the GIF into frames and enter information at particular frames. For example, 

{
  "num_frames": 34,
  "tags": {
    "T1": { "frames": [27],                 "point": [510, 300], "color":  "black"},
    "T2": { "frames": [29, 30, 31, 32, 33], "point": [190, 100], "color":  "black"},
    "T3": { "frames": [30, 31, 32, 33],     "point": [525, 100], "color":  "black"},
    "T4": { "frames": [31, 32, 33],         "point": [415, 560], "color":  "black"},
    "T5": { "frames": [32, 33],             "point": [820, 640], "color":  "black"}
  }
}


Here:
- `T1, T2, ..` are tags, that will contain the text from different languages.
- `[27, 28, 29..]` are frame numbers
- `point` is where you start writing the content
- `color` is fill color of text
