#!/usr/bin/env python

import os
import click
import subprocess
from utils import ensure_dir_exists
import pandas as pd

@click.command()

@click.option("--csv_path",
                default="out.csv",
                help="CSV file to read data from.",
                required=True)

@click.option("--cppn_img_path",
                default="cppn_images",
                help="Folder to save cppn images into.",
                required=True)
def main (csv_path=None, cppn_img_path=None):

    data = pd.read_csv(csv_path)
    imgs   = data["img"].tolist()
    titles = data["title"].tolist()

    ensure_dir_exists(cppn_img_path)

    for title, img in zip(titles, imgs):
        filename = os.path.basename(img)
        print(f"Processing {title}, image = {img}")
        proc = subprocess.Popen(
                [ "cppn"
                , "new"
                , "--net_size",     "15"
                , "--z_dim",        "20"
                , "--activations", "tanh,softplus,tanh,tanh,tanh,softplus,tanh"
                , "--colours",      "3"
                , "--out",          f"{cppn_img_path}/{filename}"
                , "match"
                , "--image",        f"{img}"
                , "--steps",        "1000"
                , "--log_every",    "1000" # Only log once.
                ])
        proc.communicate()


if __name__ == "__main__":
    main()
