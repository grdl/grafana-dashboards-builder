import builder
from pathlib import Path
from click.testing import CliRunner

sample_dash = '''
from grafanalib.core import Dashboard
dashboard = Dashboard(
    title="{title}",
    rows = []
    )
'''


def test_builder():
    runner = CliRunner()
    with runner.isolated_filesystem():
        in_path = Path('in')
        out_path = Path('out')

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

        result = runner.invoke(builder.build, [str(in_path)])

        assert result.exit_code == 0
        assert (out_path / builder.DEFAULT_FOLDER / 'dash0.json').is_file()
        assert (out_path / 'dir1').is_dir()
        assert (out_path / 'dir2').is_dir()
        assert not (out_path / 'dir3').is_dir()
        assert (out_path / 'dir1' / 'dash1.json').is_file()
        assert (out_path / 'dir2' / 'dash2.json').is_file()
        assert (out_path / 'dir2' / 'dash3.json').is_file()
