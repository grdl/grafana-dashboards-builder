import builder
from pathlib import Path
from grafanalib.core import Dashboard

sample_dash = '''
from grafanalib.core import Dashboard
dashboard = Dashboard(
    title="{title}",
    rows = []
    )
'''


def test_generate_single_dashboard(tmp_path):
    """
    Check if out_path contains a generated dashboard json with correct title.
    """

    out_path = tmp_path / builder.DEFAULT_OUT

    title = 'dash1'

    dash = tmp_path / 'dash.dashboard.py'
    dash.write_text(sample_dash.format(title=title))

    dashboards = builder.load_dashboards(tmp_path)
    builder.generate_dashboards(dashboards, out_path)

    generated_json = out_path / builder.DEFAULT_FOLDER / f'{title}.json'

    assert Path(generated_json).is_file()
    assert f'"title": "{title}"' in generated_json.read_text()


def test_out_dir_non_empty(tmp_path):
    """
    Check if out_path is correctly cleaned and contains only the newly generated files.
    """

    out_path = tmp_path / builder.DEFAULT_OUT
    out_path.mkdir()

    some_file = out_path / 'some.file'
    some_file.write_text('I should be removed')

    title = 'dash1'

    dash = tmp_path / 'dash.dashboard.py'
    dash.write_text(sample_dash.format(title=title))

    dashboards = builder.load_dashboards(tmp_path)
    builder.generate_dashboards(dashboards, out_path)

    generated_json = out_path / builder.DEFAULT_FOLDER / f'{title}.json'

    assert Path(generated_json).is_file()
    assert not Path(some_file).exists()
    assert f'"title": "{title}"' in generated_json.read_text()


def test_generating_multiple_dirs(tmp_path):
    """
    Check that for a following input dir...

        input_dir/
            dash0.dashboard.py
            dir1/
                dash1.dashboard.py
            dir2/
                dash2.dashboard.py
                dir3/
                    dash3.dashboard.py

    ...the output dir looks like this:

        output_dir/
            DEFAULT_FOLDER/
                dash0.json
            dir1/
                dash1.json
            dir2/
                dash2.json
                dash3.json
    """

    out_path = tmp_path / builder.DEFAULT_OUT
    in_path = tmp_path / 'in'
    in_path.mkdir()

    dir1 = in_path / 'dir1'
    dir2 = in_path / 'dir2'
    dir3 = in_path / 'dir2' / 'dir3'
    dir1.mkdir()
    dir2.mkdir()
    dir3.mkdir()

    dash0 = in_path / 'dash0.dashboard.py'
    dash1 = dir1 / 'dash1.dashboard.py'
    dash2 = dir2 / 'dash2.dashboard.py'
    dash3 = dir3 / 'dash3.dashboard.py'

    dash0.write_text(sample_dash.format(title='dash0'))
    dash1.write_text(sample_dash.format(title='dash1'))
    dash2.write_text(sample_dash.format(title='dash2'))
    dash3.write_text(sample_dash.format(title='dash3'))

    dashboards = builder.load_dashboards(in_path)
    builder.generate_dashboards(dashboards, out_path)

    assert (out_path / builder.DEFAULT_FOLDER / 'dash0.json').is_file()
    assert (out_path / 'dir1').is_dir()
    assert (out_path / 'dir2').is_dir()
    assert not (out_path / 'dir3').is_dir()
    assert (out_path / 'dir1' / 'dash1.json').is_file()
    assert (out_path / 'dir2' / 'dash2.json').is_file()
    assert (out_path / 'dir2' / 'dash3.json').is_file()
