import builder
from grafanalib.core import Dashboard

sample_dash_1 = '''
from grafanalib.core import Dashboard
dashboard = Dashboard(
    title="dashboard1",
    rows = []
    )
'''

sample_dash_2 = '''
from grafanalib.core import Dashboard
dashboard = Dashboard(
    title="dashboard2",
    rows = []
    )
'''


def test_load_valid_dashboard(tmp_path):
    dash = tmp_path / 'dash.dashboard.py'
    dash.write_text(sample_dash_1)

    dashboards = builder.load_dashboards(tmp_path)

    assert len(dashboards) == 1
    assert len(dashboards[builder.ROOT_DIR]) == 1
    assert isinstance(dashboards[builder.ROOT_DIR][0], Dashboard)


def test_load_not_python(tmp_path):
    dash = tmp_path / 'dash.dashboard.py'
    dash.write_text('I am not a python file')

    dashboards = builder.load_dashboards(tmp_path)

    assert len(dashboards) == 0


def test_load_empty_file(tmp_path):
    dash = tmp_path / 'dash.dashboard.py'
    dash.write_text('')

    dashboards = builder.load_dashboards(tmp_path)

    assert len(dashboards) == 0


def test_load_wrong_extension(tmp_path):
    dash = tmp_path / 'dash.py'
    dash.write_text(sample_dash_1)

    dashboards = builder.load_dashboards(tmp_path)

    assert len(dashboards) == 0


def test_load_without_dashboard(tmp_path):
    dash = tmp_path / 'dash.dashboard.py'
    dash.write_text('import grafanalib')

    dashboards = builder.load_dashboards(tmp_path)

    assert len(dashboards) == 0


def test_load_multiple_files(tmp_path):
    dash1 = tmp_path / 'dash1.dashboard.py'
    dash2 = tmp_path / 'dash2.dashboard.py'
    dash1.write_text(sample_dash_1)
    dash2.write_text(sample_dash_2)

    dashboards = builder.load_dashboards(tmp_path)

    assert len(dashboards) == 1
    assert len(dashboards[builder.ROOT_DIR]) == 2


def test_load_nested_dirs(tmp_path):
    dir1 = tmp_path / 'dir1'
    dir2 = tmp_path / 'dir2'
    dir1.mkdir()
    dir2.mkdir()

    dash1 = dir1 / 'dash1.dashboard.py'
    dash2 = dir2 / 'dash2.dashboard.py'
    dash1.write_text(sample_dash_1)
    dash2.write_text(sample_dash_2)

    dashboards = builder.load_dashboards(tmp_path)

    assert len(dashboards) == 2
    assert len(dashboards['dir1']) == 1
    assert len(dashboards['dir2']) == 1
    assert builder.ROOT_DIR not in dashboards


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

    dash0.write_text(sample_dash_1)
    dash1.write_text(sample_dash_1)
    dash2.write_text(sample_dash_1)
    dash3.write_text(sample_dash_1)

    dashboards = builder.load_dashboards(tmp_path)

    assert len(dashboards) == 3
    assert len(dashboards[builder.ROOT_DIR]) == 1
    assert len(dashboards['dir1']) == 1
    assert len(dashboards['dir2']) == 2