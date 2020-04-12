import builder
from click.testing import CliRunner


def test_input_dir_is_a_directory(tmp_path):
    path = tmp_path / 'dashboards'
    path.mkdir()

    runner = CliRunner()
    result = runner.invoke(builder.build, [str(path)])

    assert result.exit_code == 0


def test_input_dir_is_a_file(tmp_path):
    path = tmp_path / 'dashboards'
    path.write_text('I am a file')

    runner = CliRunner()
    result = runner.invoke(builder.build, [str(path)])

    assert result.exit_code != 0
    assert f"Directory '{str(path)}' is a file" in result.output


def test_input_dir_is_missing(tmp_path):
    path = tmp_path / 'dashboards'

    runner = CliRunner()
    result = runner.invoke(builder.build, [str(path)])

    assert result.exit_code != 0
    assert f"Directory '{str(path)}' does not exist" in result.output


def test_output_dir_is_a_file(tmp_path):
    path_in = tmp_path / 'dashboards'
    path_in.mkdir()

    path_out = tmp_path / 'out'
    path_out.write_text('I am a file')

    runner = CliRunner()
    result = runner.invoke(builder.build, [str(path_in), str(path_out)])

    assert result.exit_code != 0
    assert f"Directory '{str(path_out)}' is a file" in result.output


def test_output_dir_is_the_same_as_input_dir(tmp_path):
    path_in = tmp_path / 'dashboards'
    path_in.mkdir()

    runner = CliRunner()
    result = runner.invoke(builder.build, [str(path_in), str(path_in)])

    assert result.exit_code != 0
    assert "'OUTPUT_DIR' can't be the same as 'INPUT_DIR'" in result.output
