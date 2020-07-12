CantusCorpus
============

The CantusCorpus is a corpus of plainchant intended specifically for 
computational research. It is essentially a research-friendly version dump of 
the [Cantus database](http://cantus.uwaterloo.ca/). The database was scraped 
using its API, and converted to easy-to use CSV files. For many chants,
transcriptions in the Volpiano format are included. These can be loaded into
[music21](https://web.mit.edu/music21/), a Python toolkit for computational 
musicology, using the library `chant21`. 

*Note: Even the latest version of the corpus will generally be out-dated, as*
*the Cantus database is updated continuously. CantusCorpus is intended only for*
*computational studies, where this is less of a problem. If you require*
*up-to-date information, please do not use this corpus, but use Cantus directly.*

Usage
-----

TODO: example of using the corpus with chant21

Citation
--------

If you use this corpus in your research, please cite the Cantus Database
as [suggested on its website](http://cantus.uwaterloo.ca/citations):

    Cantus: A Database for Latin Ecclesiastical Chant -- Inventories of Chant 
    Sources. Directed by Debra Lacoste (2011-), Terence Bailey (1997-2010), and 
    Ruth Steiner (1987-1996). Web developer, Jan Koláček (2011-). Available 
    from <http://cantus.uwaterloo.ca/>. [date accessed].

Further please cite the paper describing the CantusCorpus:

    todo

Versions
--------

As Cantus is being updated continuously, we plan to occasionaly release new 
versions of the CantusCorpus as well. All of these will be explicitly versioned,
can be downloaded from GitHub and referenced using a Zenodo DOI. 

Licence
-------

The CantusCorpus (the collection of `.csv` files) is released under a 
[CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/) license,
just like the Cantus Database itself. The Python code used to generate the 
corpus (the code in the `src/` directory) is released under an MIT license.

Generating the corpus
---------------------

The CantusCorpus is created automatically after scraping the Cantus API.
If you just want to use the corpus, you don't have to regenerate it yourself:
simply download one of the releases and you're good to go.
But if you want to generate the corpus yourself, you can of course do so.
All code and some instructions are available in the `src` directory.