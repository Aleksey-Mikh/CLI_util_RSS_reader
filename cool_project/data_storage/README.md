Package description
===
This package contains modules that working with the storage and the storage itself.

## Format of the storage:

    storage/
        2021-09/
            2021-09-18/
                2021-10-18_https___lenta_ru_rss.json
            2021-09-19/
                2021-10-19_https___lenta_ru_rss.json
        2021-10/
            ...

The storage is divided into folders: 
the first level folder name formed from the year and month in the form of - `%Y-%m`, 
the second level folder name formed from the year, month and day in the form of - `%Y-%m-%d`.

The news is stored in a JSON file format in the form - `%Y-%m-%d_source_name.json`.
In the source name, all symbols that are not letters or numbers are replaced to `_`.


##storage_manager.py
The module contains Managers for work with storage.


##working_with_storage.py
The module contains an interface for working with Storage.