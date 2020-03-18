#!/usr/bin/env python

import os
import re
import click
import numpy as np
import pandas as pd
from skimage import io
from utils import ensure_dir_exists

# Random collection of interesting Google fonts
raw_fonts = "Abril+Fatface|Aladin|Alegreya+Sans+SC|Bellota|Berkshire+Swash|Beth+Ellen|Caesar+Dressing|Cantata+One|Caveat|Cedarville+Cursive|Chonburi|Cinzel|Cinzel+Decorative|Cormorant+SC|Dosis|Fredoka+One|Gilda+Display|Gothic+A1|Happy+Monkey|Homemade+Apple|Josefin+Sans|Lacquer|Liu+Jian+Mao+Cao|Lora|Lustria|Mali|Merriweather|Metal+Mania|Nova+Mono|Passion+One|Pirata+One|Prata|Righteous|Rubik|Sail|Sen|Sirin+Stencil|Spectral+SC|UnifrakturMaguntia|Viaoda+Libre|Vidaloka|Yeseva+One"

fonts = raw_fonts.replace("+", " ").split("|")

@click.command()
@click.option("--csv_path",
                default="out.csv",
                help="CSV file from which to read data.",
                required=True)
@click.option("--html_folder",
                default="output/",
                help="Folder where we put the generated website.",
                required=True)
@click.option("--cppn_img_path",
                default="cppn_images",
                help="Path in which to find the CPPN images.",
                required=True)
@click.option("--seed",
                default=1,
                help="Change the seed to get different outputs.",
                required=True)
def main (csv_path, html_folder, cppn_img_path, seed):
    ensure_dir_exists(html_folder)

    data   = pd.read_csv(csv_path)
    imgs   = data["img"].tolist()
    titles = data["title"].tolist()

    css  = []
    html = []

    np.random.seed(seed)

    for i, (img, title) in enumerate(zip(imgs, titles)):
        # Attempt a simple title
        title = title.split(":")[0]
        title = re.sub("[\(\[].*?[\)\]]", "", title)
        
        font,  = np.random.choice(fonts, size=1)
        width  = 20 + np.random.randint(20)
        height = 120 + np.random.randint(80)

        filename = os.path.basename(img)
        
        avg    = average_colour(f"{cppn_img_path}/{filename}")
        colour = rgb_to_hex(text_colour(*avg))
        
        css_item = f"""#book-{i} {{
width: {width}px;
height: {height}px;
background-image: url(../{cppn_img_path}/{filename});
color: {colour};
font-family: "{font}";
}}
        """
        css.append(css_item)
        
        html_item = f"""<div class="book" id="book-{i}">
{title}
</div>"""
        
        html.append(html_item)

    
    # Write the main css
    with open(f"{html_folder}/generated.css", "w") as f:
        for c in css:
            f.write(c + "\n")

    books_html = "\n".join(html)
    html_content = f"""
<link href="https://fonts.googleapis.com/css?family={raw_fonts}&display=swap" rel="stylesheet">

<link rel="stylesheet" type="text/css" href="../base.css" />
<link rel="stylesheet" type="text/css" href="generated.css" />

<script src="../ext/textFit.min.js"></script>

<div class="shelf">
    {books_html}
</div>

<script type="text/javascript">
  textFit(document.getElementsByClassName('book'));
</script>
"""
    with open(f"{html_folder}/index.html", "w") as f:
        f.write(html_content)

    # Then the base stuff.


def rgb_to_hex (rgb):
    return "#{0:02x}{1:02x}{2:02x}".format(*[int(a) for a in rgb])


def text_colour (r, g, b):
    # https://graphicdesign.stackexchange.com/a/17562
    gamma = 2.2;
    L = 0.2126   * pow( r / 255, gamma )\
        + 0.7152 * pow( g / 255, gamma )\
        + 0.0722 * pow( b / 255, gamma )
        

    use_black = ( L > 0.5 )
    
    if use_black:
        return [0, 0, 0]
    else:
        return [255, 255, 255]


def crop_center (img,cropx,cropy):
    y, x, _ = img.shape
    startx  = x // 2 - (cropx // 2)
    starty  = y // 2 - (cropy // 2)
    return img[starty:starty+cropy, startx:startx+cropx]


def average_colour (path):
    """ Compute a simple pixel average. """
    img     = io.imread(path)

    # Because we only show part of the image, i.e. a rectangle aroud the
    # center, we need to compute the average colour across that section only;
    # as it might be quite different to the image itself. This isn't perfect,
    # but does the job.
    img     = crop_center(img, 100, 100)
    average = img.mean(axis=0).mean(axis=0)
    return average


if __name__ == "__main__":
    main()
