import click
from . import __version__ as version
from .parser import parse as parse_src
from .rasa_language import RasaLanguage


@click.command()
@click.argument("src_file", type=click.File("r"))
@click.argument("bot_dir")
def main(src_file, bot_dir):
    lang = RasaLanguage()

    click.echo("Processing files...")
    lang.process(src_file.read())
    lang.dump_files(bot_dir)


if __name__ == "__main__":
    main()
