#!/usr/bin/env python

import os
import click
import subprocess
from utils import ensure_dir_exists

@click.command()

@click.option("--img_path",
                default="images",
                help="Folder to load base images from.",
                required=True)

@click.option("--cppn_img_path",
                default="cppn_images",
                help="Folder to save cppn images into.",
                required=True)
def main (img_path=None, cppn_img_path=None):
    imgs = os.listdir(img_path)
    imgs = [ i for i in imgs if i.endswith(".jpg") ]

    ensure_dir_exists(cppn_img_path)

    for img in imgs:
        print(f"Processing {img}")
        proc = subprocess.Popen(
                [ "cppn"
                , "new"
                , "--net_size",     "15"
                , "--z_dim",        "20"
                , "--activations", "tanh,softplus,tanh,tanh,tanh,softplus,tanh,tanh,tanh,tanh"
                , "--colours",      "3"
                , "--out",          f"{cppn_img_path}/{img}"
                , "match"
                , "--image",        f"{img_path}/{img}"
                , "--steps",        "2000"
                , "--log_every",    "2000" # Only log once.
                ])
        proc.communicate()


if __name__ == "__main__":
    main()
