import click
import logging
import os

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"),
                    format='%(asctime)s [%(levelname)s] %(message)s')
log = logging.getLogger(__name__)


@click.command()
def build():
    log.info('Starting Grafana Dashboards Builder')


if __name__ == '__main__':
    # pylint: disable=no-value-for-parameter, unexpected-keyword-arg
    build()
