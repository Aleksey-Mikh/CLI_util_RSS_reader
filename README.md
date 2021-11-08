Project description 
===
Implemented Python RSS-reader using python 3.9.

RSS reader is a command-line utility that receives RSS URL and prints results in a human-readable format.


---
Quick start
---
      >>> rss_reader https://people.onliner.by/feed --limit 1

      ---------------------------------- Start Program ----------------------------------
      [INFO] Receiving the news was successful
      
      
      
      Feed source: https://people.onliner.by/feed
      Feed: Люди Onlíner
      
      -------------------------------------- News 1 -------------------------------------
      Title: Работник случайно слил в канализацию полторы тонны полуфабриката белорусског
      о коньяка. Отправлен под суд
      Date: Fri, 29 Oct 2021 15:00:13 +0300
      Link: https://people.onliner.by/2021/10/29/vylil-v-kanalizaciyu-poltory-tonny-belor
      usskogo-konyaka
      Category: Социум
      
      Description: Грустная история случилась весной прошлого года на минском «Кристалле»
      : мастер случайно отправил в канализацию 1622,13 литра коньяка. На работника завели
      уголовное дело за служебную халатность. Известно про этот случай стало после того,
      как было опубликовано решение суда.Читать далее…
      
      Media Object: https://content.onliner.by/news/thumbnail/a4be8e39b5616a231de7fa7960d
      81047.jpeg
      Extra Links: https://people.onliner.by/2021/10/29/vylil-v-kanalizaciyu-poltory-tonn
      y-belorusskogo-konyaka
      -----------------------------------------------------------------------------------
      
      ----------------------------------- Stop Program ----------------------------------
---

## Contents
***
1. [Installation](#Installation)
2. [Usage](#Usage)
3. [Format converter](#Format-converter)
    * [Converter to PDF](#Converter-to-PDF)
    * [Converter to HTML](#Converter-to-HTML)
4. [Storage](#Storage)
    * [Format of the storage](#Format-of-the-storage)
5. [Tests](#Tests)
6. [What's in the future](#What's-in-the-future)

---
## Installation
To install, you need to make a clone of the repository:
```
>>> git clone https://github.com/Aleksey-Mikh/Homework.git -b master
```
After that, you need to go to the CLI_util directory:
```
>>> cd your_path/CLI_util/
```
and install the utility:
```
>>> pip install -e .
```
Don't forget the dot at the end!
Now you can use the utility in two ways:
```
>>> python rss_reader.py https://people.onliner.by/feed --limit 1
```
or
```
>>> rss_reader https://people.onliner.by/feed --limit 1
```
If needed, add the path to the repo to the environment variable $PYTHONPATH. 
The script will be available from everywhere.

Linux:
```
>>> export PYTHONPATH="${PYTHONPATH}:<path to repo>"
```
Windows:
```
>>> set PYTHONPATH=%PYTHONPATH%;<path to repo>
```
[:arrow_up:Contents](#Contents)

---
## Usage
You can see the information about the utility using the following command:

      >>> rss_reader --help

      usage: rss_reader [-h] [--version] [--json] [--verbose] [--limit LIMIT] [--date DATE] [--to-html TO_HTML]
                        [--to-pdf TO_PDF] [--colorize]
                        [source]
      
      Pure Python command-line RSS reader.
      
      positional arguments:
        source             RSS URL
      
      optional arguments:
        -h, --help         show this help message and exit
        --version          Print version info
        --json             Print result as JSON in stdout
        --verbose          Outputs verbose status messages
        --limit LIMIT      Limit news topics if this parameter provided
        --date DATE        Take a date in %Y%m%d format. Example: 20191206
        --to-html TO_HTML  This argument receives the path where new HTML file will be saved.
        --to-pdf TO_PDF    This argument receives the path where new PDF file will be saved.
        --colorize         That will print the result of the utility in colorized mode.

You can see the version of the utility:
```
>>> rss_reader --version

Version 5.0.0
```
Argument `--version` will output the version despite other arguments:
```
>>> rss_reader https://people.onliner.by/feed --limit 1 --version

Version 5.0.0
```
When entering the `source` argument, the got page is parsed on the Internet,
if you specify the `--date some_date` argument, then the news is searched in the local storage
and an Internet connection is not required.

When you enter only `--date some_date`, the news will be searched for by the specified date. 
If the news is not found, an error will be returned:
```
>>> rss_reader --date 20210810

------------------------------------------ Start Program ------------------------------------------
[ERROR] No news was found for this date - 2021-08-10

------------------------------------------- Stop Program ------------------------------------------
```
If you enter `source` and `--date some_date` utility will search news by the got to date
and the got to site. If the news is not found, an error will be returned:
```
>>> rss_reader https://people.onliner.by/feed --date 20210810

-------------------------------------------------- Start Program -------------------------------------------------
[ERROR] No news was founded for this date: 20210810, and this source: https://people.onliner.by/feed

-------------------------------------------------- Stop Program --------------------------------------------------
```

If you want more information about how the program works you can enter the argument `--verbose`:

      >>> rss_reader https://people.onliner.by/feed --limit 4 --verbose 

      ---------------------------------------- Start Program ---------------------------------------
      [INFO] Start Scrapping
      
      [INFO] Count of news: 4
      
      [INFO] News received [1/4], percent of execution program=25%
      
      [INFO] News received [2/4], percent of execution program=50%
      
      [INFO] News received [3/4], percent of execution program=75%
      
      [INFO] News received [4/4], percent of execution program=100%
      
      [INFO] Receiving the news was successful
      
      [INFO] Stop Scrapping
      
      [INFO] Output news in standard format
      
      
      
      Feed source: https://people.onliner.by/feed
      Feed: Люди Onlíner
      
      ------------------------------------------- News 1 -------------------------------------------
      Title: Слишком тепло: в выходные до +18
      Date: Fri, 29 Oct 2021 18:00:23 +0300
      Link: https://people.onliner.by/2021/10/29/v-vyxodnye-do-18
      Category: Социум
      
      Description: После слишком холодного сентября наступает чересчур теплый ноябрь. Не уверены, чт
      о последовательность именно такая, но эти месяцы изначально перепутали местами. В общем, на за
      втра Белгидромет не исключает 18 градусов, это гораздо теплее нормы.Читать далее…
      
      Media Object: https://content.onliner.by/news/thumbnail/847f53a5b4f75a81f4312d021825dab9.jpeg
      Extra Links: https://people.onliner.by/2021/10/29/v-vyxodnye-do-18
      ----------------------------------------------------------------------------------------------
                                                        
                                                   ...      

      ------------------------------------------- News 4 -------------------------------------------
      Title: Работник случайно слил в канализацию полторы тонны полуфабриката белорусского коньяка.
      Отправлен под суд
      Date: Fri, 29 Oct 2021 15:00:13 +0300
      Link: https://people.onliner.by/2021/10/29/vylil-v-kanalizaciyu-poltory-tonny-belorusskogo-kon
      yaka
      Category: Социум
      
      Description: Грустная история случилась весной прошлого года на минском «Кристалле»: мастер сл
      учайно отправил в канализацию 1622,13 литра коньяка. На работника завели уголовное дело за слу
      жебную халатность. Известно про этот случай стало после того, как было опубликовано решение су
      да.Читать далее…
      
      Media Object: https://content.onliner.by/news/thumbnail/a4be8e39b5616a231de7fa7960d81047.jpeg
      Extra Links: https://people.onliner.by/2021/10/29/vylil-v-kanalizaciyu-poltory-tonny-belorussk
      ogo-konyaka
      ----------------------------------------------------------------------------------------------

      ---------------------------------------- Stop Program ----------------------------------------

When you enter the arguments `--to-pdf path` and `--to-html path`, 
conversion to the specified format will be executed in addition to the output. 
You can find more information [here](#Format-converter).


When you enter the `--json` argument, the console will output data in JSON format:

    [
        {
        "channel_title": channel_title,
        "source": source,
        },
        {
            "title": title,
            "date": pub_date,
            "link": link,
            "author": author,
            "category": list_categories,
            "description": description,
            "more_description": content_encoded,
            "comments": comments,
            "media_object": enclosure,
            "extra_links": guid,
            "source_feed": list_source,
        },
    ]
You can find more information [here](cool_project/cervices/README.md).

---
[:arrow_up:Contents](#Contents)

## Format converter
The utility supports the conversion of news into the following formats: HTML, PDF.

### Converter to PDF
When you enter the `--to-pdf path` argument, the `feed.pdf` file will be saved to the got path.
You can find more information [here](cool_project/conversion_to_format/README.md).

### Converter to HTML
When you enter the `--to-html path` argument, the `html.pdf` file will be saved to the got path.
You can find more information [here](cool_project/conversion_to_format/README.md).

---
[:arrow_up:Contents](#Contents)

## Storage
The utility uses caching of news with the ability to output them without an Internet connection.

### Format of the storage:

    storage/
        2021-09/
            2021-09-18/
                2021-10-18_https___lenta_ru_rss.json
            2021-09-19/
                2021-10-19_https___lenta_ru_rss.json
        2021-10/
            ...
You can find more information [here](cool_project/data_storage/README.md).

---
[:arrow_up:Contents](#Contents)

## Tests

      >>> pytest .\tests\ --cov=rss_reader --cov=.\cool_project\

      ======================================== test session starts =========================================
      platform win32 -- Python 3.9.7, pytest-6.2.5, py-1.10.0, pluggy-1.0.0
      rootdir: C:\Users\lehado01\PycharmProjects\EPAM_final_task\Homework\Aleksey_Mikhalkevich\CLI_util
      plugins: cov-3.0.0, mock-3.6.1
      collected 78 items                                                                                    
      
      tests\test_data_storage\test_storage_managers.py .......................                        [ 29%]
      tests\test_data_storage\test_working_with_storage.py ...                                        [ 33%]
      tests\test_rss_reader\test_rss_reader.py ........                                               [ 43%]
      tests\tests_conversion_to_format\test_conversion_to_html.py .......                             [ 52%]
      tests\tests_conversion_to_format\test_conversion_to_pdf.py .......                              [ 61%]
      tests\tests_serializers\test_serializers.py ............                                        [ 76%]
      tests\tests_services\test_data_output.py ........                                               [ 87%]
      tests\tests_services\test_decorators.py .......                                                 [ 96%]
      tests\tests_services\test_print_functions.py ...                                                [100%]
      
      ----------- coverage: platform win32, python 3.9.7-final-0 -----------
      Name                                                      Stmts   Miss  Cover
      -----------------------------------------------------------------------------
      cool_project\__init__.py                                      0      0   100%
      cool_project\cervices\__init__.py                             0      0   100%
      cool_project\cervices\data_output.py                         41      9    78%
      cool_project\cervices\decorators.py                          60      0   100%
      cool_project\cervices\print_functions.py                      6      0   100%
      cool_project\conversion_to_format\__init__.py                 0      0   100%
      cool_project\conversion_to_format\conversion_to_html.py      38      2    95%
      cool_project\conversion_to_format\conversion_to_pdf.py      102      4    96%
      cool_project\data_storage\__init__.py                         0      0   100%
      cool_project\data_storage\storage_managers.py               197      0   100%
      cool_project\data_storage\working_with_storage.py            53      0   100%
      cool_project\serializers\__init__.py                          0      0   100%
      cool_project\serializers\serializers.py                     132      3    98%
      rss_reader.py                                               100     11    89%
      -----------------------------------------------------------------------------
      TOTAL                                                       729     29    96%
      
      
      ========================================= 78 passed in 2.08s =========================================
---
[:arrow_up:Contents](#Contents)

## What's in the future
In the future, I'm going to upload the utility to PYPI and add more formats for conversions.


## Author
[GitHub](https://github.com/Aleksey-Mikh)

[linkedin](https://www.linkedin.com/in/aliaksei-mikhalkevich-b740b0201/)

MAIl - lehado67@gmail.com