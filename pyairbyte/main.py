from airbyte.sources import get_source
from airbyte.caches.duckdb import DuckDBCache

SOURCE_NAME = 'source-file'
SOURCE_VERSION = '0.5.31'
SOURCE_CONFIG_FORMAT = 'csv'
SOURCE_CONFIG_PROVIDER = {'storage': 'local'}
SOURCE_CONFIG_FILE_DIRECTORY = '/source/jaffle-data/'
SOURCE_CONFIG_FILE_NAMES = [
    'raw_customers'
    , 'raw_items'
    , 'raw_orders'
    , 'raw_products'
    , 'raw_stores'
    , 'raw_supplies'
]

DESTINATION_DB_PATH = '/destination/dev.duckdb'
DESTINATION_DB_SCHEMA = 'raw'

nb_source = len(SOURCE_CONFIG_FILE_NAMES)
sources = [None] * nb_source

for i in range(nb_source): 
    source_file_name = SOURCE_CONFIG_FILE_NAMES[i]
    sources[i] = get_source(name=SOURCE_NAME, version=SOURCE_VERSION, config={
        'dataset_name': source_file_name
        , 'format': SOURCE_CONFIG_FORMAT
        , 'url': SOURCE_CONFIG_FILE_DIRECTORY + source_file_name + '.' + SOURCE_CONFIG_FORMAT
        , 'provider': SOURCE_CONFIG_PROVIDER
    })
    
    sources[i].check()


duckdb_cache = DuckDBCache(db_path=DESTINATION_DB_PATH, schema_name=DESTINATION_DB_SCHEMA)

for i, file_name in enumerate(SOURCE_CONFIG_FILE_NAMES): 
    sources[i].read(
        cache=duckdb_cache
        , streams=file_name
        , write_strategy='auto'
        , force_full_refresh=False
        , skip_validation=False
    )


# source-file, version="0.5.31"
# destination-duckdb, version="0.5.1"
# Im not using the destination connector because it uses Docker to run
# If you dont want to use pyairbyte but airbyte directly, use the provided version of the destination-duckdb, 
#                                   it support duckdb 1.2.1 (the version used in this project)