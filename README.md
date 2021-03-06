# CPPN Bookshelf Generator

![](screenshot_1.png)


## Usage

1. Clone and install

```
git clone https://github.com/silky/cppn-bookshelf.git
cd cppn-bookshelf
# Make some kind of environment ...
pip install -r requirements.txt
```

2. Run `grab-books.py` with your (or someone elses!) goodreads id. You can
   find that by clicking `My Books` and copying the number out of the url.
   Here's what mine looks like: `https://www.goodreads.com/review/list/30456689`, so my ID is `30456689`.

```
./grab-books.py --goodreads_id ...
```

By default it looks at your `read` shelf, you can select a different shelf
with `--shelf to-read`, for example.

You will probably want to change the `--count` parameter to be the number of
books you have on the shelf. By default, it only does this for 10 books.


3. Run `compute-cppns`

```
./compute-cppns.py
```

(Note: This step might take a while, depending on how many books you have, as
it's the part that computes the cool-looking spine image, from the cover
image. It takes about 30 seconds per book, on my laptop.)

4. Run `make-page`

```
./make-page.py
```

5. Open the `index.html` in the `output/` folder!

You can change the look and feel of the html by investingating `make-page.py`.

Enjoy!
