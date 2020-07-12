CantusCorpus v{version}
===========================

The CantusCorpus is a corpus of plainchant intended specifically for 
computational research. It is essentially a research-friendly version dump of 
the [Cantus database](http://cantus.uwaterloo.ca/). The database was scraped 
using its API, and converted to easy-to use CSV files. For many chants,
transcriptions in the Volpiano format are included. These can be loaded into
[music21](https://web.mit.edu/music21/), a Python toolkit for computational 
musicology, using the library `chant21`. 

| Summary                          |                      |
|----------------------------------|----------------------|
| CantusCorpus version             | {version: <20} |
| Corpus generated on              | {corpus_date: <20} |
| Cantus database scraped on       | {cantus_scrape_date: <20} |
| Number of chants                 | {num_chant: <20} |
| Number of sources                | {num_source: <20} |
| Number of genres                 | {num_genre: <20} |
| Number of provenances            | {num_provenance: <20} |
| Number of feasts                 | {num_feast: <20} |

License
-------

The CantusCorpus is released under a 
[CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/) license, 
just like the Cantus Database itself.

Tables
------

Below you find an overview of all fields in each table. For some fields we have automatically computed value frequencies.

{tables}

### orig_id

This table maps CantusCorpus ids to the original ids used by the the Cantus API.

Changelog v{version}
-------------------

{changelog}
