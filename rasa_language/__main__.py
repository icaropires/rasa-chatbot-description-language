import pathlib
import json
from sys import argv, exit

import click
from . import __version__ as version
from .parser import parse as parse_src
from .rasa_language import RasaLanguage


@click.command()
@click.argument("src_file", type=click.File("r"))
@click.argument("bot_dir")
def main(src_file, bot_dir):
    lang = RasaLanguage()
    lang.process(src_file.read())

    path = pathlib.Path(bot_dir) / "data" / "nlu.json"

    with open(path, "w") as f_out:
        json.dump(
            lang.nlu, f_out, ensure_ascii=False, indent=4, sort_keys=True
        )
        click.secho("NLU file generated succesfully!", fg="green", bold=True)


if __name__ == "__main__":
    main()
