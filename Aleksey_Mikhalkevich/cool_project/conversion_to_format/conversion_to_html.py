import os
import sys
from pathlib import Path

from jinja2 import Environment, PackageLoader, select_autoescape, FileSystemLoader

# from temp import LIST




def is_list(obj):
    return isinstance(obj, list)


def convert_to_html(data, path):
    path = Path(__file__).parent
    path = Path(path, "templates")
    env = Environment(
        loader=FileSystemLoader(path),
        autoescape=select_autoescape(["html"]),
        trim_blocks=True,
        lstrip_blocks=True,
    )

    content = {}
    content["title"] = "Feeds"
    content["feeds"] = [data]
    env.tests['is_list'] = is_list

    template = env.get_template("template.html")
    result = template.render(content)
    with open('temp.html', 'w', encoding="utf-8") as file:
        file.write(result)
