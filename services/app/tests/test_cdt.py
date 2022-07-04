from click.testing import CliRunner
import pytest

from .. import main as cdt


@pytest.fixture(scope="module")
def runner():
    return CliRunner()

@pytest.fixture
def common_compound():
    return 'ATP'

def test_actualize_atp(runner, common_compound):
    result = runner.invoke(cdt.main, ['--name','Amy'])
    assert result.exit_code == 0
    assert result.output == 'Hello Amy!\n'


def test_default_hello(runner):
    result = runner.invoke(hll.main, input='\n')
    assert result.exit_code == 0
    print(result.output)
    expected = 'greet whom? [world]: \nHello world!\n'
    assert result.output == expected