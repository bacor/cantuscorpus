# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Author: Bas Cornelissen
# Copyright © 2019 Bas Cornelissen
# Licence: MIT
# -----------------------------------------------------------------------------
"""Generate the CantusCorpus"""
import os
import logging
import glob
import shutil
import re
import yaml

import pandas as pd
from collections import Counter
from helpers import read_gzip_json
import numpy as np
import datetime

# CantusCorpus version
__version__ = '0.2'

SRC_DIR = os.path.dirname(__file__)
ROOT_DIR = os.path.abspath(os.path.join(SRC_DIR, os.path.pardir))
SCRAPE_DIR = os.path.join(ROOT_DIR, 'scrape')
DIST_DIR = os.path.join(ROOT_DIR, 'dist')
OUTPUT_DIR = os.path.join(DIST_DIR, f'cantuscorpus-v{__version__}')
CSV_DIR = os.path.join(OUTPUT_DIR, 'csv')
TMP_DIR = os.path.join(OUTPUT_DIR, 'tmp')

# Three types are ignored: portfolio, source_status, segment
TYPES = [
    'century',
    'chant',
    'feast',
    'genre',
    'indexer',
    'notation',
    'office',
    'provenance',
    'siglum',
    'source'
]

FOREIGN_IDS = [
    'feast_id',
    'source_id',
    'office_id',
    'genre_id',
    'century_id',
    'provenance_id',
    'segment_id'
]

table_structure_fn = os.path.join(SRC_DIR, 'table_structure.yml')
with open(table_structure_fn, 'r') as stream:
    TABLE_STRUCTURE = yaml.safe_load(stream)

###

def relpath(path, start=ROOT_DIR):
    return os.path.relpath(path, start=start)

def read_resources(scrape_name):
    """Read out the scraped resources (the gzipped json files) and return them 
    as one big Pandas DataFrame with all possible fields as columns. This 
    dataframe is later split into multiple dataframes by type.

    Parameters
    ----------
    scrape_name : str
        Name of the scraping session

    Returns
    -------
    pd.DataFrame
        A dataframe with all resources
    """
    logging.info('Reading out the scraped resources...')
    pattern = os.path.join(SCRAPE_DIR, scrape_name, 'pages', '*.json.gz')
    page_filenames = sorted(glob.glob(pattern))
    if len(page_filenames) == 0:
        raise Warning('No pages found!')
    resources = {}
    for page_fn in page_filenames:
        page = read_gzip_json(page_fn)
        resources.update(page['resources'])
    df = pd.DataFrame(resources).T
    df.index.name = 'orig_id'
    df.sort_index(inplace=True)
    del df['id']
    return df

def sample_dev_resources(resources):
    types = resources['type'].unique()
    ids = []
    for resource_type in types:
        subset = resources.query(f'type=="{resource_type}"')
        sample_size = min(len(subset), 500)
        ids.extend(list(subset.sample(sample_size).index))
    df = resources.loc[ids,:]
    return df.sort_index()

def generate_dev_resources(resources_fn):
    """Generate a small resources.csv file containing a random sample of 
    resources of all types. This is used for development purposes, as loading
    the complete dataframe takes a significant amount of time.

    Parameters
    ----------
    resources_fn : str
        Filename of the full resources csv file

    Returns
    -------
    pd.DataFrame
        The development subset
    """
    resources = pd.read_csv(resources_fn, index_col=0)
    types = resources['type'].unique()
    ids = []
    for resource_type in types:
        subset = resources.query(f'type=="{resource_type}"')
        sample_size = min(len(subset), 500)
        ids.extend(list(subset.sample(sample_size).index))
    df = resources.loc[ids,:]
    output_dir = os.path.dirname(resources_fn)
    df.to_csv(os.path.join(output_dir, 'dev-resources.csv'))
    return df

###

def parse_century_name(name):
    """Extract the start and end year from a century name. The years are 
    corrected to be inclusive: the second half of the 10th century is 950–999, 
    and not 950–1000.

    >>> parse_century_name("09th century")
    [800, 899]
    >>> parse_century_name("16th century (1575-1600)")
    [1575, 1599]
    >>> parse_century_name("12th century (1st half)")
    [1100, 1149]
    >>> parse_century_name("14th century (2nd half)")
    [1350, 1399]

    Parameters
    ----------
    name : str
        The name of the century

    Returns
    -------
    list
        A list with the start and end year
    """
    # https://regex101.com/r/WxtCb5/3
    pattern = r'(\d{1,2})th century( (\(((\d+)-(\d+)|((2nd|1st) half))\)))?'
    matches = re.match(pattern, name)
    if not matches: raise Exception('Could not parse name')
    century = (int(matches[1]) - 1) * 100

    # A full century
    if matches[2] is None:
        period = [century, century+99]
    # Contains a start and end
    if matches[5] is not None:
        period = [int(matches[5]), int(matches[6])-1]
    # Contains 2nd or 1st
    if matches[8] is not None:
        if matches[8] == '1st':
            period = [century, century+49]
        elif matches[8] == '2nd':
            period = [century+50, century+99]
    return period

def parse_feast_date(date):
    """Parse the date format in the feasts table
    
    >>> parse_feast_date('Feb.24')
    [2, 24]
    >>> parse_feast_date('Jul.4')
    [7, 4]
    >>> parse_feast_date(None)
    [None, None]

    Parameters
    ----------
    date : str
        The date, e.g. Feb.24

    Returns
    -------
    list
        month and day as integers
    """
    if pd.isnull(date): return [None, None]
    try:
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 
                'Oct', 'Nov', 'Dec']
        month, day = date.split('.')
        month_int = months.index(month) +  1
        day_int = int(day)
        return [month_int, day_int]
    except:
        return [None, None]
 
### Processors
# Every processor should take a table dataframe and at least add an id column
# The index should not be changed

def process_table_default(df, rtype):
    if 'name' in df.columns:
        df.sort_values('name', inplace=True)
    id_length = int(np.ceil(np.log10(len(df))))
    id_pattern = f'{rtype}_{{i:0{id_length}d}}'
    df['id'] = [id_pattern.format(i=i) for i in range(1, len(df)+1)]
    return df

def process_table_century(df, **kwargs):
    periods = list(df['name'].map(parse_century_name))
    ids = [f'century_{start:04d}_{end:04d}' for start, end in periods]
    df['id'] = ids
    df['start'] = np.array(periods)[:, 0]
    df['end'] = np.array(periods)[:, 1]
    df['duration'] = df['end'] - df['start'] + 1
    df['century'] = np.floor(df['start'] / 100).astype(int) + 1
    return df
   
def process_table_feast(df, **kwargs):
    dates = np.array(df['date'].map(parse_feast_date).to_list())
    df['month'] = dates[:, 0]
    df['day'] = dates[:, 1]
    df.sort_values('name', inplace=True)
    df['id'] = [f'feast_{i:04d}' for i in range(1, len(df)+1)]
    return df

def process_table_genre(df, **kwargs):
    df['id'] = 'genre_' + (
        df['name'].str.replace('[\[\]\/]', '').str.lower())

    # Add a suffix to duplicated genre names
    df.sort_values('description', ascending=True, inplace=True)
    duplicates = df.id[df.id.duplicated()].values
    for duplicate in duplicates:
        index = df[df.id == duplicate].iloc[1:, :].index
        for i, idx in enumerate(index):
            df.loc[index, 'id'] += f'_{i+1}'
    return df

def process_table_indexer(df, **kwargs):
    df.sort_values('family_name', inplace=True)
    df['id'] = [f'indexer_{i:03d}' for i in range(1, len(df)+1)]
    cols = ['institution', 'city', 'country', 'display_name', 'given_name']
    df.drop(cols, axis='columns', inplace=True)
    return df

def process_table_office(df, **kwargs):
    df.sort_values('name', inplace=True)
    df['id'] = [f'office_{name.lower()}' for name in df['name']]
    return df

def process_table_source(df, **kwargs):
    df = process_table_default(df, 'source')
    segments = {
        'CANTUS Database': 'cantus',
        'Bower Sequence Database': 'bower'
    }
    del df['segment_id']
    df['segment'] = df['segment'].map(lambda segm: segments.get(segm, segm))
    return df

def process_table_chant(df, **kwargs):
    df.sort_values('incipit', inplace=True)
    df['id'] = [f'chant_{i:06d}' for i in range(1, len(df)+1)]
    cols = ['feast', 'feast_desc', 'genre', 'office', 'source']
    df.drop(cols, axis='columns', inplace=True)
    return df

###

def extract_table_of_type(resources, rtype):
    logging.info(f'Extracting type={rtype}')
    table = resources.query(f'type=="{rtype}"').copy()

    # Process the table: add ids, possible other columns, and sort
    processor = globals().get(f'process_table_{rtype}', process_table_default)
    table = processor(table, rtype=rtype)
    table = table.reset_index().set_index('id').sort_index()
    assert table.index.is_unique

    # Drop empty columns
    del table['type']
    allowed_columns = [field['name'] for field in TABLE_STRUCTURE[rtype]['fields']]
    allowed_columns.append('orig_id')
    for column in table.columns:
        column_is_empty = table[column].isna().all()
        if column not in allowed_columns:
            if column_is_empty:
                del table[column]
            else:
                logging.warning(f'* Column {column} is not empty!')

    return table

def update_foreign_ids(table, orig_ids):
    foreign_id_cols = [col for col in table.columns if col in FOREIGN_IDS]
    if len(foreign_id_cols) == 0: 
        return table

    # Temporarily rename the index, as there is also an 'id' column in orig_ids
    table.index.name = '__index'
    table.reset_index(inplace=True)
    for foreign_id in foreign_id_cols:
        table = table.merge(orig_ids, 
            left_on=foreign_id, right_on='orig_id', how='left')
        # Replace the foreign id by the matching 'ids' in orig_id: the new ids
        del table[foreign_id]
        table[foreign_id] = table['id']
        del table['id']
        del table['orig_id']
    table.set_index('__index', inplace=True)
    table.index.name = 'id'
    return table
     
def generate_corpus(scrape_name):
    
    # Step 1
    resources = read_resources(scrape_name)
    resources_fn = os.path.join(TMP_DIR, f'resources-{scrape_name}.csv')
    resources.to_csv(resources_fn)
    logging.info(f'Stored resources temporarily to {relpath(resources_fn)}')
    resources = pd.read_csv(resources_fn, index_col=0)

    # After extracting all resources, you can generate a subset with resources
    # of all types to speed up the development process
    # dev_resources_fn = os.path.join(TMP_DIR, 'dev-resources.csv')
    # dev_resources = sample_dev_resources(resources)
    # dev_resources.to_csv(dev_resources_fn)
    # resources = pd.read_csv(dev_resources_fn, index_col=0)

    # Step 2
    orig_ids = {}
    for rtype in TYPES:
        table = extract_table_of_type(resources, rtype=rtype)
        orig_ids.update(table['orig_id'].to_dict())
        del table['orig_id']
        table_fn = os.path.join(CSV_DIR, f'{rtype}.csv')
        table.to_csv(table_fn)
        logging.info(f'* Stored table for type {rtype} to {relpath(table_fn)}')

    # Step 4: Store original ids
    orig_ids = pd.Series(orig_ids).sort_index()
    orig_ids.name = 'orig_id'
    orig_ids.index.name = 'id'
    orig_ids_fn = os.path.join(CSV_DIR, 'orig_id.csv')
    orig_ids.to_csv(orig_ids_fn)
    logging.info(f'Stored original ids to {relpath(orig_ids_fn)}')
    
    # Step 5: update foreign ids and reorder the columns
    logging.info('Updating foreign ids and reordering columns...')
    orig_ids = orig_ids.reset_index()
    for rtype in TYPES:
        table_fn = os.path.join(CSV_DIR, f'{rtype}.csv')
        table = pd.read_csv(table_fn, index_col=0)
        table = update_foreign_ids(table, orig_ids)
        if rtype in TABLE_STRUCTURE:
            order = [field['name'] for field in TABLE_STRUCTURE[rtype]['fields'] if field['name'] != 'id']
            assert set(table.columns) == set(order)
            table = table[order]
        table.to_csv(table_fn)

    chant = pd.read_csv(os.path.join(CSV_DIR, 'chant.csv'), index_col=0)
    has_volpiano = chant.volpiano.isna() == False
    sample = chant.loc[has_volpiano, :].sample(n=2000, random_state=0).sort_index()
    sample_fn = os.path.join(CSV_DIR, 'chant-demo-sample.csv')
    sample.to_csv(sample_fn)
    logging.info(f'Stored a random sample of 2000 chants to {relpath(sample_fn)}')

###

class ReadmeWriter(object):

    def __init__(self):
        """"""
        # Set up output directories
        if not os.path.exists(CSV_DIR):
            raise Exception('CSV directory not found')

        # Load all csv files
        self.tables = {}
        for rtype in TABLE_STRUCTURE:
            table_fn = os.path.join(CSV_DIR, f'{rtype}.csv')
            table = pd.read_csv(table_fn, index_col=0)
            self.tables[rtype] = table

    def table_structure(self, table_name):
        """Create a Markdown table describing the structure a database table:
        the columns, what values they take, and so on."""
        columns_to_report = []
        lines = []
        lines.append('| Column       | Type | Description                                        |')
        lines.append('|--------------|------|----------------------------------------------------|')
        fields = TABLE_STRUCTURE[table_name]['fields']
        for column in fields:
            name = column.get('name', '')
            dtype = column.get('dtype', '')
            description = column.get('description', '').strip()
            lines.append(f'| {name: <12} | {dtype: <4} | {description: <50} |')

        for column in fields:
            if not 'report_value_counts' in column:
                continue
            table = self.tables[table_name]
            column_name = column['name']
            value_counts = pd.value_counts(table[column_name])
            value_descriptions = column.get('value_descriptions', {})
            title = f'#### Values of `{table_name}.{column_name}`\n'
            if 'value_description_table' in column:
                value_descriptions = self.tables[column['value_description_table']]
                title = f'#### Frequencies of `{table_name}.{column_name}` values\n'

            lines.append('')
            lines.append(title)
            lines.append('| Value        | Count | Perc. | Description                              |')
            lines.append('|--------------|------:|------:|------------------------------------------|')

            others_count = 0
            other_values = []
            min_freq = column.get('report_min_freq', 0)
            for value, count in value_counts.iteritems():
                perc = count / len(table) * 100

                if perc <= min_freq:
                    others_count += count
                    if 'value_description_table' in column:
                        template = column['value_description_template']
                        description = template.format(description=value_descriptions.loc[value, :])
                        other_values.append(f'`{description}`')
                    else:
                        other_values.append(f'`{value}`')
                    continue

                if 'value_description_table' in column:
                    template = column['value_description_template']
                    description = template.format(description=value_descriptions.loc[value, :])
                else:
                    description = value_descriptions.get(value, '')
                lines.append(f'| {value: <12} | {count: >5} | {perc: >4.0f}% | {description: <40} |')
            
            if others_count > 0:
                perc = others_count / len(table) * 100
                values = ", ".join(other_values) if column.get('report_other_values', True) else ''
                lines.append(f'| *Others*     | {others_count: >5} | {perc: >4.0f}% | {values} |')

            missing = len(table) - sum(value_counts)
            perc = missing / len(table) * 100
            lines.append(f'| *None*     | {missing: >5} | {perc: >4.0f}% | |')
        return '\n'.join(lines)

    def get_changelog(self):
        """Export the changes in changelog.csv as a markdown list"""
        changelog = pd.read_csv(os.path.join(SRC_DIR, 'changelog.csv'))
        new_changes = changelog.query(f'version=={__version__}')
        lines = []
        for i, (version, change) in new_changes.iterrows():
            line = f'- {change}'
            lines.append(line)
        return '\n'.join(lines)

    def get_tables(self):
        output = ''
        for table_name, props in TABLE_STRUCTURE.items():
            output += f'\n### {table_name.title()}\n'
            output += props.get('description', '') + '\n\n'
            output += self.table_structure(table_name)
        return output

    def write_readme(self, cantus_scrape_date="?"):
        """Write the README for a release of the GregoBase Corpus using the 
        template file `readme_template.md`."""
        logging.info('Writing README file...')
        now = datetime.datetime.now()
        corpus_date = now.strftime("%d %B %Y")
        
        template_kws = {
            'version': __version__,
            'cantus_scrape_date': cantus_scrape_date,
            'corpus_date': corpus_date,
            'changelog': self.get_changelog(),
            'tables': self.get_tables()
        }

        for rtype in TABLE_STRUCTURE:
            template_kws[f'num_{rtype}'] = len(self.tables[rtype])

        with open(os.path.join(SRC_DIR, 'readme_template.md'), 'r') as handle:
            template = handle.read()
            readme = template.format(**template_kws)
        
        readme_fn = os.path.join(OUTPUT_DIR, 'README.md')
        with open(readme_fn, 'w') as handle:
            handle.write(readme)

###

def compress_corpus():
    """Compress the output directory, and put the archive inside it."""
    archive_fn = os.path.join(DIST_DIR, f'cantuscorpus-v{__version__}')
    shutil.make_archive(archive_fn, 'zip', OUTPUT_DIR)
    source_fn = f'{archive_fn}.zip'
    target_fn = os.path.join(OUTPUT_DIR, f'cantuscorpus-v{__version__}.zip')
    logging.info(f"Compressing the corpus: {os.path.relpath(target_fn, start=OUTPUT_DIR)}")
    os.rename(source_fn, target_fn)

###
 
def main():
    # Clear output_dir before starting logging to that directory
    if os.path.exists(OUTPUT_DIR):
        shutil.rmtree(OUTPUT_DIR)
    os.makedirs(OUTPUT_DIR)
    if not os.path.exists(CSV_DIR):
        os.makedirs(CSV_DIR)
    if not os.path.exists(TMP_DIR):
        os.makedirs(TMP_DIR)

    # Set up logging
    log_fn = os.path.join(OUTPUT_DIR, 'corpus-generation.log')
    logging.basicConfig(filename=log_fn,
                        filemode='w',
                        format='%(levelname)s %(asctime)s %(message)s',
                        datefmt='%d-%m-%y %H:%M:%S',
                        level=logging.INFO)
    logging.info(f'Start generating CantusCorpus v{__version__}')
    logging.info(f"> Output directory: '{relpath(OUTPUT_DIR)}'")

    # Go
    generate_corpus('2020-07-09-scrape-v0.1')
    writer = ReadmeWriter()
    writer.write_readme()
    shutil.rmtree(TMP_DIR)
    compress_corpus()

if __name__ == '__main__':
    # import doctest
    # doctest.testmod()
    main()
