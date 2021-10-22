from pathlib import Path

from jinja2 import Environment, select_autoescape, FileSystemLoader

from cool_project.cervices.print_functions import error_print, info_print

FILE_NAME = "feed.html"


def make_dir(path):
    if not Path(path).exists():
        p = Path(path)
        p.mkdir(parents=True)


def is_list(obj):
    return isinstance(obj, list)


def get_env():
    path = Path(__file__).parent
    path = Path(path, "templates")
    env = Environment(
        loader=FileSystemLoader(path),
        autoescape=select_autoescape(["html"]),
        trim_blocks=True,
        lstrip_blocks=True,
    )
    return env


def get_content(data, env):
    if not is_list(data[0]):
        data = [data]
    content = {
        "title": "Feeds",
        "feeds": data
    }
    env.tests["is_list"] = is_list
    return content


def convert_to_html(data, path, verbose):
    if verbose:
        info_print("Conversion to HTML started")

    env = get_env()
    content = get_content(data, env)
    template = env.get_template("template.html")
    result = template.render(content)
    path = Path(path)
    try:
        make_dir(path)
        with open(Path(path, FILE_NAME), "w", encoding="utf-8") as file:
            file.write(result)
        info_print(f"A feed in HTML format was saved on the path: {Path(path, FILE_NAME)}")
        if verbose:
            info_print("Conversion to HTML ended")
    except Exception:
        error_print("The entered path cannot be created")
