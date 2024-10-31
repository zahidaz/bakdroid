from importlib import metadata
import click
from pathlib import Path


__version__ = metadata.version(__package__ or __name__)


@click.group()
@click.version_option(
    __version__, "-v", "--version", is_flag=True, message="%(version)s"
)

@click.pass_context
def cli(ctx):
    pass

@cli.command()
@click.argument('input_file', type=click.Path(exists=True, path_type=Path))
@click.argument('output_file', type=click.Path(path_type=Path))
@click.option('--password', prompt=True, hide_input=True, help='Password for decryption')
def unpack(input_file: Path, output_file: Path, password: str):
    """
    Unpack a backup file.

    INPUT_FILE: Path to the input backup file (e.g., backup.en.ab)
    OUTPUT_FILE: Path to the output tar file
    """
    from bakdroid.unpacker import Unpacker
    Unpacker(input_file, output_file).unpack(password)
    click.echo(f"Unpacked {input_file} to {output_file}")

if __name__ == "__main__":
    cli()