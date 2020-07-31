CantusCorpus v{version}
=================

The CantusCorpus is a corpus of plainchant intended specifically for 
computational research. It is essentially a research-friendly version dump of 
the [Cantus database](http://cantus.uwaterloo.ca/) [1]. The database was scraped 
using its API, and converted to easy-to use CSV files. For many chants,
transcriptions in the Volpiano format are included. These can be loaded into
[`music21`](https://web.mit.edu/music21/), a Python toolkit for computational 
musicology, using the library [`chant21`](https://github.com/bacor/chant21). 

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

[1] Cantus: A Database for Latin Ecclesiastical Chant -- Inventories of Chant 
Sources. Directed by Debra Lacoste (2011-), Terence Bailey (1997-2010), and Ruth
Steiner (1987-1996). Web developer, Jan Koláček (2011-). Available from 
<http://cantus.uwaterloo.ca/>. Accessed on {cantus_scrape_date}.

License
-------

The CantusCorpus is released under a 
[CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/) license, 
just like the Cantus Database itself.

Citation
--------

If you use this corpus in your research, please cite the Cantus Database
as [suggested on its website](http://cantus.uwaterloo.ca/citations):

    Cantus: A Database for Latin Ecclesiastical Chant -- Inventories of Chant 
    Sources. Directed by Debra Lacoste (2011-), Terence Bailey (1997-2010), and 
    Ruth Steiner (1987-1996). Web developer, Jan Koláček (2011-). Available 
    from <http://cantus.uwaterloo.ca/>. [date accessed].

Further please cite the paper describing the CantusCorpus, and please mention
which version of the corpus you used.

    todo

Versions
--------

As Cantus is being updated continuously, we plan to occasionaly release new 
versions of the CantusCorpus as well. All of these will be versioned,
can be downloaded from GitHub. 

Tables
------

Below you find an overview of all fields in each table. For some fields we have automatically computed value frequencies.

{tables}

### orig_id

This table maps CantusCorpus ids to the original ids used by the the Cantus API.

Changelog v{version}
-------------------

{changelog}
