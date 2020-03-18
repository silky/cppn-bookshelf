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

2. Run `grab-books.py` with your goodreads id. You can find that by clicking
   `My Books` and copying the number out of the url. Here's what mine looks
   like: `https://www.goodreads.com/review/list/30456689`, so my ID is
   `30456689`.

```
./grab-books.py --goodreads_id ...
```

3. Run `compute-cppns`

```
./compute-cppns.py
```

(Note: This step might take a while, depending on how many books you have.)

4. Run `make-page`

```
./make-page.py
```

5. Open the `index.html` in the `output/` folder!
