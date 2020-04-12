import click
import logging
import os

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"), format='%(asctime)s [%(levelname)s] %(message)s')
log = logging.getLogger(__name__)


@click.command()
@click.argument('input-dir', type=click.Path(exists=True, file_okay=False))
@click.argument('output-dir', type=click.Path(file_okay=False), default='out')
def build(input_dir, output_dir):

    if input_dir == output_dir:
        raise click.BadArgumentUsage("'OUTPUT_DIR' can't be the same as 'INPUT_DIR'.")

    log.info('Starting Grafana Dashboards Builder')

    print(input_dir)


if __name__ == '__main__':
    build()  # pylint: disable=no-value-for-parameter, unexpected-keyword-arg
