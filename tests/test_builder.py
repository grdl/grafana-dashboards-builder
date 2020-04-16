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
        out_path = Path(builder.DEFAULT_OUT)

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


def test_builder_from_config_map():
    """
    When run with --from-configmap, output directory structure should be created based on the separator in dashboard filenames.
    When run without --from-configmap, outpout directory should contain only the DEFAULT_FOLDER.
    """

    runner = CliRunner()
    with runner.isolated_filesystem():
        in_path = Path('in')
        out_path = Path(builder.DEFAULT_OUT)

        in_path.mkdir()

        dash0 = in_path / 'dash0.dashboard.py'
        dash1 = in_path / f'dir1{builder.DIR_SEPARATOR}dash1.dashboard.py'
        dash2 = in_path / f'dir2{builder.DIR_SEPARATOR}-dash2.dashboard.py'
        dash3 = in_path / f'dir2{builder.DIR_SEPARATOR}dash3.dashboard.py'

        dash0.write_text(sample_dash.format(title='dash0'))
        dash1.write_text(sample_dash.format(title='dash1'))
        dash2.write_text(sample_dash.format(title='dash2'))
        dash3.write_text(sample_dash.format(title='dash3'))

        result = runner.invoke(builder.build, [str(in_path), '--from-configmap'])

        assert result.exit_code == 0
        assert (out_path / builder.DEFAULT_FOLDER).is_dir()
        assert (out_path / 'dir1').is_dir()
        assert (out_path / 'dir2').is_dir()

        assert (out_path / builder.DEFAULT_FOLDER / 'dash0.json').is_file()
        assert (out_path / 'dir1' / 'dash1.json').is_file()
        assert (out_path / 'dir2' / 'dash2.json').is_file()
        assert (out_path / 'dir2' / 'dash3.json').is_file()

        result = runner.invoke(builder.build, [str(in_path)])

        assert result.exit_code == 0
        assert (out_path / builder.DEFAULT_FOLDER).is_dir()
        assert not (out_path / 'dir1').is_dir()
        assert not (out_path / 'dir2').is_dir()

        assert (out_path / builder.DEFAULT_FOLDER / 'dash0.json').is_file()
        assert (out_path / builder.DEFAULT_FOLDER / 'dash1.json').is_file()
        assert (out_path / builder.DEFAULT_FOLDER / 'dash2.json').is_file()
        assert (out_path / builder.DEFAULT_FOLDER / 'dash3.json').is_file()
