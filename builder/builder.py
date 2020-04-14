import click
import shutil
from pathlib import Path
from grafanalib import _gen as generator

ROOT_DIR = '.'
DEFAULT_OUT = 'out'


@click.command()
@click.argument('input-dir', type=click.Path(file_okay=False, exists=True))
@click.argument('output-dir', type=click.Path(file_okay=False), default='out')
def build(input_dir, output_dir):

    # TODO: can this be checked in click.argument callback?
    if input_dir == output_dir:
        raise click.BadArgumentUsage("'OUTPUT_DIR' can't be the same as 'INPUT_DIR'.")

    click.echo('Starting Grafana Dashboards Builder')

    dashboards = load_dashboards(input_dir)
    generate_dashboards(dashboards, output_dir)


def load_dashboards(input_dir):
    """
    Load .dashboard.py files into a dictionary where keys are first level directories.
    Keys represent Grafana folders, but since Grafana allows only a single level of folder nesting we "flatten" dashboard.py files
    even if they're nested in multiple directories.

    :param input_dir str: Path to directory containing dashboard sources.

    :Example:

    For a following folder structure...

        input_dir/
            dash0.dashboard.py
            dir1/
                dash1.dashboard.py
            dir2/
                dash2.dashboard.py
                dir3/
                    dash3.dashboard.py

    ...a loaded dashboards dictionary should look like this:

        dashboards = {
            '.': [dash0],
            'dir1': [dash1],
            'dir2': [dash2, dash3]
        }
    """

    dashboards = {}

    for path in Path(input_dir).rglob(f'*{generator.DASHBOARD_SUFFIX}'):
        try:
            dashboard = generator.load_dashboard(str(path))
        except generator.DashboardError:  # raised when file does not define 'dashboard' attribute
            continue
        except SyntaxError:  # raised when file contains invalid Python code
            continue

        # key is the first level directory inside the input_dir in the dashboard path
        # if there are more nested dirs inside it, the key will still be the first-level one
        key = path.relative_to(str(input_dir)).parts[0]

        # if key is the same as filename it means file is not nested in any directory but directly under the input_dir
        if key == path.name:
            key = ROOT_DIR

        if key not in dashboards:
            dashboards[key] = []

        dashboards[key].append(dashboard)

    return dashboards


def generate_dashboards(dashboards, output_dir):
    """
    Generate and write dashboard json files into the output_dir. For each key in dashboards dict a new subfolder is created.
    If output_dir already exists it will be removed and recreated.
    """

    shutil.rmtree(output_dir, ignore_errors=True)   # Remove the output dir, don't raise errors if dir doesn't exist
    Path(output_dir).mkdir()

    for key in dashboards:
        subdir = output_dir / key
        subdir.mkdir(exist_ok=True)

        for dashboard in dashboards[key]:
            output_path = output_dir / key / f'{dashboard.title}.json'
            with open(output_path, 'w') as output:
                generator.write_dashboard(dashboard, output)


if __name__ == '__main__':
    build()  # pylint: disable=no-value-for-parameter, unexpected-keyword-arg
