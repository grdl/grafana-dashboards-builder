import builder
from grafanalib.core import Dashboard

sample_dash = '''
from grafanalib.core import Dashboard
dashboard = Dashboard(
    title="{title}",
    rows = []
    )
'''


def test_load_valid_dashboard(tmp_path):
    dash = tmp_path / 'dash.dashboard.py'
    dash.write_text(sample_dash.format(title='dash'))

    dashboards = builder.load_dashboards(str(tmp_path))

    assert len(dashboards) == 1
    assert len(dashboards[builder.DEFAULT_FOLDER]) == 1
    assert isinstance(dashboards[builder.DEFAULT_FOLDER][0], Dashboard)


def test_load_not_python(tmp_path):
    dash = tmp_path / 'dash.dashboard.py'
    dash.write_text('I am not a python file')

    dashboards = builder.load_dashboards(str(tmp_path))

    assert len(dashboards) == 0


def test_load_empty_file(tmp_path):
    dash = tmp_path / 'dash.dashboard.py'
    dash.write_text('')

    dashboards = builder.load_dashboards(str(tmp_path))

    assert len(dashboards) == 0


def test_load_wrong_extension(tmp_path):
    dash = tmp_path / 'dash.py'
    dash.write_text(sample_dash.format(title='dash'))

    dashboards = builder.load_dashboards(str(tmp_path))

    assert len(dashboards) == 0


def test_load_without_dashboard(tmp_path):
    dash = tmp_path / 'dash.dashboard.py'
    dash.write_text('import grafanalib')

    dashboards = builder.load_dashboards(str(tmp_path))

    assert len(dashboards) == 0


def test_load_multiple_files(tmp_path):
    dash1 = tmp_path / 'dash1.dashboard.py'
    dash2 = tmp_path / 'dash2.dashboard.py'
    dash1.write_text(sample_dash.format(title='dash1'))
    dash2.write_text(sample_dash.format(title='dash2'))

    dashboards = builder.load_dashboards(str(tmp_path))

    assert len(dashboards) == 1
    assert len(dashboards[builder.DEFAULT_FOLDER]) == 2


def test_load_nested_dirs(tmp_path):
    dir1 = tmp_path / 'dir1'
    dir2 = tmp_path / 'dir2'
    dir1.mkdir()
    dir2.mkdir()

    dash1 = dir1 / 'dash1.dashboard.py'
    dash2 = dir2 / 'dash2.dashboard.py'
    dash1.write_text(sample_dash.format(title='dash1'))
    dash2.write_text(sample_dash.format(title='dash2'))

    dashboards = builder.load_dashboards(str(tmp_path))

    assert len(dashboards) == 2
    assert len(dashboards['dir1']) == 1
    assert len(dashboards['dir2']) == 1
    assert builder.DEFAULT_FOLDER not in dashboards


def test_load_multiple_nested_dirs(tmp_path):
    dir1 = tmp_path / 'dir1'
    dir2 = tmp_path / 'dir2'
    dir3 = tmp_path / 'dir2' / 'dir3'
    dir1.mkdir()
    dir2.mkdir()
    dir3.mkdir()

    dash0 = tmp_path / 'dash0.dashboard.py'
    dash1 = dir1 / 'dash1.dashboard.py'
    dash2 = dir2 / 'dash2.dashboard.py'
    dash3 = dir3 / 'dash3.dashboard.py'

    dash0.write_text(sample_dash.format(title='dash0'))
    dash1.write_text(sample_dash.format(title='dash1'))
    dash2.write_text(sample_dash.format(title='dash2'))
    dash3.write_text(sample_dash.format(title='dash3'))

    dashboards = builder.load_dashboards(str(tmp_path))

    assert len(dashboards) == 3
    assert len(dashboards[builder.DEFAULT_FOLDER]) == 1
    assert len(dashboards['dir1']) == 1
    assert len(dashboards['dir2']) == 2


def test_load_general_folder(tmp_path):
    """
    If there are dashboards in the root of input_dir and inside the "General" default folder,
    they all should be loaded under the same DEFAULT_FOLDER key
    """

    general = tmp_path / 'General'
    general.mkdir()

    dash0 = tmp_path / 'dash0.dashboard.py'
    dash1 = general / 'dash1.dashboard.py'

    dash0.write_text(sample_dash.format(title='dash0'))
    dash1.write_text(sample_dash.format(title='dash1'))

    dashboards = builder.load_dashboards(str(tmp_path))

    assert len(dashboards) == 1
    assert len(dashboards[builder.DEFAULT_FOLDER]) == 2


def test_load_from_configmap(tmp_path):
    dash0 = tmp_path / 'dash0.dashboard.py'
    dash1 = tmp_path / f'dir1{builder.DIR_SEPARATOR}dash1.dashboard.py'
    dash2 = tmp_path / f'dir2{builder.DIR_SEPARATOR}-dash2.dashboard.py'
    dash3 = tmp_path / f'dir2{builder.DIR_SEPARATOR}dash3.dashboard.py'

    dash0.write_text(sample_dash.format(title='dash0'))
    dash1.write_text(sample_dash.format(title='dash1'))
    dash2.write_text(sample_dash.format(title='dash2'))
    dash3.write_text(sample_dash.format(title='dash3'))

    dashboards = builder.load_dashboards(str(tmp_path), from_configmap=True)

    assert len(dashboards) == 3
    assert len(dashboards[builder.DEFAULT_FOLDER]) == 1
    assert len(dashboards['dir1']) == 1
    assert len(dashboards['dir2']) == 2

    dashboards = builder.load_dashboards(str(tmp_path), from_configmap=False)

    assert len(dashboards) == 1
    assert len(dashboards[builder.DEFAULT_FOLDER]) == 4
