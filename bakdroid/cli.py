from importlib import metadata
import click
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

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
@click.option('--password', '-p', help='Password to decrypt the backup file')
@click.option('--verbose', '-v', is_flag=True, help='Enable verbose output')
def unpack(input_file: Path, output_file: Path, password: str, verbose: bool):
    """
    Unpack a backup file.

    INPUT_FILE: Path to the input backup file (e.g., backup.en.ab)
    OUTPUT_FILE: Path to the output tar file
    """
    from bakdroid.unpacker import Unpacker

    if verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    try:
        Unpacker(input_file, output_file).unpack(password)
        click.echo(f"Unpacked {input_file} to {output_file}")
    except Exception as e:
        if verbose:
            logger.exception(e)
        click.echo(f"Error: {e}")
        exit(1)

if __name__ == "__main__":
    cli()