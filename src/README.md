Generating the corpus
=====================

Below you find instructions for generating the Cantus corpus.
If you just want to use the corpus, simply download one of the releases:
you don't have to regenerate it yourself.

Requirements
------------

You can find the Python version used in `.python-version` and all dependencies 
are listed in `requirements.txt`. If you use `pyenv` and `venv` to manage Python
versions and virtual environments, do the following:

```python
# Install the right python version
pyenv install | cat .python-version

# Create a virtual environment
python -m venv env

# Activate the environment
source env/bin/activate

# Install dependencies
pip install -r requirements.txt
```

Overview
--------

Generating the corpus involves roughly three steps. First, you need to scrape 
the Cantus API and retrieve all resources. Second, export the resource to clean 
CSV files. Third, generate a README file and compress the corpus.

The script `scrape.py` performs the first part: it scrapes the Cantus API. 
Briefly, `https://abbot.uwaterloo.ca:8888/browse` lists all resources. The 
script requests each of those ~5000 pages successively and after some minor
postprocessing stores them as compressed json files in 
`scrape/scrape_name/pages`. Running this script will take a few hours.

The script `generate_corpus.py` takes care of the next two steps. First, it 
converts the compressed json files to one giant pandas DataFrame, which is then
split by type into several tables, for chants, sources, genres, etc. We then 
generate new ids for all items in a table. The ids used by the Cantus API are 
very long and unreadable, and this can be annoying in practice. The ids we 
generate are of the form `chant_123456`, `genre_a`, `source_0123`, etc. These
are globally unique, but also readable. The CantusCorpus ids are related to
the original ids in `orig_ids.csv`. Making new ids also means that we have to 
fix all cross-references (foreign keys). If a foreign key/cross-reference occurs
in a table, we don't include any other information from the foreign table. For
example, in `chants.csv` we find cross-references to sources via a `source_id`,
so we have omitted columns with, say, source title or description in the chants
table. Joining the CSV files on the `source_id` is straightforward using Pandas.

Finally, we automatically generate a README file containing some automatically
computed statistics about value frequencies. All this ends up in a directory 
`dists/cantuscorpus-v0.1`, which is zipped and released.

License
-------

The code for generating the corpus is released under an MIT license; see `src/LICENCE`.
Note that CantusCorpus itself is released under a different license.