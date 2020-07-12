CantusCorpus v0.1
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
| CantusCorpus version             | 0.1                  |
| Corpus generated on              | 12 July 2020         |
| Cantus database scraped on       | ?                    |
| Number of chants                 | 497071               |
| Number of sources                | 640                  |
| Number of genres                 | 57                   |
| Number of provenances            | 219                  |
| Number of feasts                 | 1828                 |

License
-------

The CantusCorpus is released under a 
[CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/) license, 
just like the Cantus Database itself.

Tables
------

Below you find an overview of all fields in each table. For some fields we have automatically computed value frequencies.


### Chant


| Column       | Type | Description                                        |
|--------------|------|----------------------------------------------------|
| id           | str  | A globally unique, and human-readable id of the chant of the form  `chant000253`. These are *not* the ids used by the Cantus database and may not be consistent across CantusCorpus versions. See `orig_ids.csv` for the mapping of ids to Cantus database ids. |
| incipit      | str  | incipit of the chant                               |
| cantus_id    | str  | See http://cantus.uwaterloo.ca/description#Cantus%20ID%20Number |
| mode         | str  | Mode of the chant; see http://cantus.uwaterloo.ca/description#Mode |
| finalis      | str  | The final note of the chant, used e.g. when the mode is unclear.  See http://cantus.uwaterloo.ca/description#Finalis |
| differentia  | str  | See http://cantus.uwaterloo.ca/description#Differentia |
| siglum       | str  |                                                    |
| position     | str  | Liturgical role of a chant;  see http://cantus.uwaterloo.ca/description#Position |
| folio        | str  | folio or page in the manuscript where the chant is found,  see http://cantus.uwaterloo.ca/description#Folio |
| sequence     | str  | Order in which the chant is found on the page or folio side. See http://cantus.uwaterloo.ca/description#Sequence |
| marginalia   | str  | additional clarification of the location of the chant on the  folio or page; see http://cantus.uwaterloo.ca/description#Marginalia |
| cao_concordances |      |                                                    |
| feast_id     | str  | id of feast                                        |
| genre_id     | str  | id of the liturgical genre                         |
| office_id    | int  | id of the office                                   |
| source_id    | str  | id of source                                       |
| melody_id    |      |                                                    |
| drupal_path  | str  | URL to Cantus website page of chant                |
| full_text    | str  | Full text in a standardized spelling.  See http://cantus.uwaterloo.ca/description#Fulltext |
| full_text_manuscript | str  | Full text in the manuscript spelling. This also includes barlines, or missing texts, etc. See http://cantus.uwaterloo.ca/description#MSSpelling or the [Volpiano protocols](http://cantus.uwaterloo.ca/sites/default/files/documents/2.%20Volpiano%20Protocols.pdf) |
| volpiano     | str  | Transcription of the melody in the Volpiano typeface. See http://cantus.uwaterloo.ca/description#Volpiano and the [Volpiano protocols](http://cantus.uwaterloo.ca/sites/default/files/documents/2.%20Volpiano%20Protocols.pdf) |
| notes        | str  | Indexing notes, see http://cantus.uwaterloo.ca/description#IndexingNotes |

#### Values of `chant.mode`

| Value        | Count | Perc. | Description                              |
|--------------|------:|------:|------------------------------------------|
| *            | 105738 |   21% |                                          |
| 8            | 69198 |   14% |                                          |
| 1            | 57782 |   12% |                                          |
| 7            | 45893 |    9% |                                          |
| 4            | 33048 |    7% |                                          |
| 2            | 29485 |    6% |                                          |
| *Others*     | 117083 |   24% | `3`, `?`, `r`, `5`, `6`, `6T`, `4T`, `1S`, `2T`, `1T`, `8S`, `2S`, `3S`, `6S`, `5S`, `7S`, `8*`, `4S`, `1*`, `G`, `7*`, `Gd`, `4*`, `8?`, `7T`, `Gc`, `?S`, `D`, `Da`, `E`, `5T`, `3*`, `2*`, `8T`, `1?`, `4?`, `7?`, `3T`, `6*`, `?T`, `F`, `M`, `5*`, `2?`, `3?`, `ad`, `6?`, `Fa`, `5?`, `7/8`, `EE`, `td`, `Ea`, `1/2`, `5T/6T`, `1T/2T`, `8C`, `4A`, `*4`, `3/4`, `DF`, `7,8`, `DE`, `S`, `1,2`, `5,6`, `c`, `*1`, `5/6`, `?*`, `6T?`, `1T/3T`, `*8`, `Ec`, `7T?`, `FC`, `*6`, `*3`, `*2`, `2 - 1`, `3,4`, `Eb`, `todo`, `3T/4T`, `Fc`, `2T*`, `*5`, `*7`, `cd`, `R`, `2T?`, `1T?`, `F1`, `P`, `?4`, `EG`, `6T*`, `?pb 6T`, `ac`, `5C`, `4s`, `8T?`, `IT`, `Ge`, `DG`, `Ga`, `r?`, `84`, `5*?`, `4t`, `2/2T`, `5T?`, `c2`, `CF`, `4/`, `4T?`, `3s`, `3.2`, `8 7`, `6F`, `7B`, `3.1`, `r*`, `7*?`, `1 - 2`, `7a`, `? 2`, `5T*`, `7s`, `I`, `5/7?`, `G?`, `8 - 7`, `8/5?`, `a` |
| *None*     | 38844 |    8% | |

#### Frequencies of `chant.feast_id` values

| Value        | Count | Perc. | Description                              |
|--------------|------:|------:|------------------------------------------|
| feast_1202   |  8645 |    2% | Christmas Day                            |
| feast_0227   |  7008 |    1% | Common of several Martyrs                |
| feast_0552   |  6677 |    1% | Epiphany                                 |
| feast_0198   |  6428 |    1% | Common of Apostles                       |
| feast_0500   |  6151 |    1% | Sundays, Ferial Office                   |
| feast_1416   |  6058 |    1% | Purification of Mary (Candlemas)         |
| feast_0093   |  5800 |    1% | Assumption of Mary                       |
| feast_0258   |  5791 |    1% | Common of one Martyr                     |
| feast_0475   |  5731 |    1% | 5th Sunday of Lent (Passion Sunday)      |
| feast_0933   |  5719 |    1% | Dedication of a Church                   |
| feast_1548   |  5645 |    1% | Stephen the First Martyr                 |
| feast_0983   |  5523 |    1% | John the Baptist                         |
| feast_0091   |  5488 |    1% | Ascension Thursday                       |
| feast_0719   |  5444 |    1% | Holy Thursday (Maundy Thursday)          |
| feast_1150   |  5371 |    1% | Michael the Archangel (Michaelmas)       |
| feast_0390   |  5369 |    1% | 1st Sunday of Advent                     |
| feast_0994   |  5362 |    1% | John the Evangelist                      |
| feast_1056   |  5272 |    1% | Laurence, Martyr                         |
| feast_1283   |  5055 |    1% | All Saints' Day                          |
| feast_1321   |  4971 |    1% | Paul, Apostle                            |
| *Others*     | 371189 |   75% |  |
| *None*     |  8374 |    2% | |

#### Frequencies of `chant.genre_id` values

| Value        | Count | Perc. | Description                              |
|--------------|------:|------:|------------------------------------------|
| genre_a      | 205409 |   41% | Antiphon                                 |
| genre_r      | 102443 |   21% | Responsory                               |
| genre_v      | 94482 |   19% | Responsory verse                         |
| genre_w      | 35594 |    7% | Versicle                                 |
| genre_h      | 17840 |    4% | Hymn                                     |
| genre_i      | 10086 |    2% | Invitatory antiphon                      |
| *Others*     | 27248 |    5% | `Antiphon verse`, `Gradual`, `Alleluia`, `Psalm`, `Offertory`, `Communion`, `Introit`, `Gradual verse`, `Introit verse`, `Invitatory psalm (when fully written out and notated)`, `Tract verse`, `Offertory verse`, `Sequence`, `Hymn verse`, `Lesson (when fully written out and notated)`, `Kyrie`, `Tract`, `Tropus`, `Gloria`, `Agnus dei`, `Communion verse`, `Sanctus`, `Dramatic element (used for items of liturgical drama that are not otherwise rubricked)`, `Alleluia verse`, `Varia within Holy Week`, `Varia`, `Credo`, `Prefatio (when written out and notated)`, `Ite missa est`, `Verse for the Preces (Old Hispanic)`, `"Miscellaneous" (a descriptor used in the earliest versions of Cantus for the Te Deum, Versus in Triduo, prosulae - to be replaced by Va=Varia)`, `Litany`, `Sequence verse`, `Benedicamus domino`, `Canticle verse`, `Litany verse`, `Canticle`, `Pater noster`, `Unknown, ambiguous, unidentifiable, illegible`, `Preces (Old Hispanic)` |
| *None*     |  3969 |    1% | |

#### Frequencies of `chant.source_id` values

| Value        | Count | Perc. | Description                              |
|--------------|------:|------:|------------------------------------------|
| source_309   |  8396 |    2% | Arras, Bibliothèque municipale, 893 (olim 465) |
| source_390   |  8109 |    2% | Worcester, Cathedral - Music Library, F.160 (olim 1247) (with hymnal) |
| source_633   |  7628 |    2% | Worcester, Cathedral - Music Library, F.160 (olim 1247) (facsimile) |
| *Others*     | 432115 |   87% |  |
| *None*     | 40823 |    8% | |

#### Values of `chant.volpiano`

| Value        | Count | Perc. | Description                              |
|--------------|------:|------:|------------------------------------------|
| *Others*     | 63628 |   13% |  |
| *None*     | 433443 |   87% | |
### Century


| Column       | Type | Description                                        |
|--------------|------|----------------------------------------------------|
| id           | str  | A globally unique, human readable id of the form 'period_0900_0999' |
| name         | str  | A description of the period, such as "9th century (875–900)" |
| century      | int  | Which century the period lies in. The period 850–874 lies in the 9th  century and has value `9`. |
| start        | int  | The starting year of the period.                   |
| end          | int  | The ending year of the period. This is inclusive, so the 15th century ends in the year 1499. |
| duration     | int  | The duration of the period in years: 25, 50 or 100 years |
### Feast


| Column       | Type | Description                                        |
|--------------|------|----------------------------------------------------|
| id           | str  | A globally unique, human readable feast ID of the form `feast_1234` |
| name         | str  | Name of the feast,  see http://cantus.uwaterloo.ca/description#Liturgical%20Occasion%20/%20Feast |
| description  | str  |                                                    |
| date         | str  | Date of the feast, e.g. `Aug.16`                   |
| month        | int  | month of the feast as an integer                   |
| day          | int  | day of the month as an integer                     |
| feast_code   | int  | a code for the feast                               |
| notes        | str  |                                                    |
### Genre


| Column       | Type | Description                                        |
|--------------|------|----------------------------------------------------|
| id           | str  | A globally unique id for the genre, of the form `genre_name`, where name is a lower-cased version of the name abbreviation name. So `genre_r` is  responsory, `genre_tcv` a tract verse, etc. |
| name         | str  | An abbreviation for the chant genre; see also http://cantus.uwaterloo.ca/genre |
| description  | str  |                                                    |
| mass_or_office | list | Part of the office, mass or both?                  |
### Indexer


| Column       | Type | Description                                        |
|--------------|------|----------------------------------------------------|
| id           | str  | A globally unique id for the indexer, of the form `indexer_123` |
| family_name  | str  | The family name of the indexer. Other personal information, such as the given name, institution, city and country have been omitted. |
| drupal_path  | str  | A URL to the indexer page on the Cantus site       |
### Notation


| Column       | Type | Description                                        |
|--------------|------|----------------------------------------------------|
| id           | str  | A globally unique id of the form `notation_122`    |
| name         | str  | Type of notation used                              |
### Office


| Column       | Type | Description                                        |
|--------------|------|----------------------------------------------------|
| id           | str  | A globally unique id of the form `office_name` where name is the  abbreviation used by Cantus. So `office_l` is the lauds, `office_mi` the  mass, etc. |
| name         | str  |                                                    |
| description  | str  |                                                    |
### Provenance


| Column       | Type | Description                                        |
|--------------|------|----------------------------------------------------|
| id           | str  | a globally unique id of the form `provenance_123`  |
| name         | str  |                                                    |
### Segment


| Column       | Type | Description                                        |
|--------------|------|----------------------------------------------------|
| id           |      |                                                    |
| name         |      |                                                    |
### Siglum


| Column       | Type | Description                                        |
|--------------|------|----------------------------------------------------|
| id           | str  | a globally unique id of the form siglum_123        |
| name         | str  |                                                    |
| description  | str  |                                                    |
### Source


| Column       | Type | Description                                        |
|--------------|------|----------------------------------------------------|
| id           | str  |                                                    |
| title        | str  |                                                    |
| description  | str  |                                                    |
| rism         | str  |                                                    |
| date         | str  |                                                    |
| century      | str  |                                                    |
| century_id   |      | id of the century                                  |
| provenance   | str  |                                                    |
| provenance_detail | str  |                                                    |
| provenance_id | str  |                                                    |
| segment      | str  |                                                    |
| segment_id   | str  |                                                    |
| summary      | str  |                                                    |
| indexing_notes | str  |                                                    |
| liturgical_occasions | str  |                                                    |
| indexing_date | str  |                                                    |
| drupal_path  | str  |                                                    |

### orig_id

This table maps CantusCorpus ids to the original ids used by the the Cantus API.

Changelog v0.1
-------------------

- Test
