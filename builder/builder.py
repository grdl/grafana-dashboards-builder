import click
from pathlib import Path
from grafanalib import _gen

ROOT_DIR = '.'


@click.command()
@click.argument('input-dir', type=click.Path(exists=True, file_okay=False))
@click.argument('output-dir', type=click.Path(file_okay=False), default='out')
def build(input_dir, output_dir):

    # TODO: can this be checked in click.argument callback?
    if input_dir == output_dir:
        raise click.BadArgumentUsage("'OUTPUT_DIR' can't be the same as 'INPUT_DIR'.")

    click.echo('Starting Grafana Dashboards Builder')

    load_dashboards(input_dir)


def load_dashboards(input_dir):
    """
    Load .dashboard.py files into a dictionary where keys are first level directories.
    Keys represent Grafana folders, but since Grafana allows only a single level of folder nesting we "flatten" dashboard.py files
    even if they're nested in multiple directories.

    Example:
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

    for path in Path(str(input_dir)).rglob(f'*{_gen.DASHBOARD_SUFFIX}'):
        try:
            dashboard = _gen.load_dashboard(path)
        except _gen.DashboardError:  # raised when file does not define 'dashboard' attribute
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


if __name__ == '__main__':
    build()  # pylint: disable=no-value-for-parameter, unexpected-keyword-arg
