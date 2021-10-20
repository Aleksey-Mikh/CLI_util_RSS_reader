import os
import sys
import pathlib

from jinja2 import Environment, PackageLoader, select_autoescape, FileSystemLoader

from temp import LIST


env = Environment(
    loader=FileSystemLoader('template'),
    autoescape=select_autoescape(["html"]),
    trim_blocks=True,
    lstrip_blocks=True,
)


def is_list(obj):
    return isinstance(obj, list)


content = {}
content["title"] = "Feeds"
content["feeds"] = LIST
env.tests['is_list'] = is_list

template = env.get_template("template.html")
result = template.render(content)

with open('temp.html', 'w', encoding="utf-8") as file:
    file.write(result)
