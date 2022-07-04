from click.testing import CliRunner
import pytest

from src import cdt as cdt


@pytest.fixture(scope="module")
def runner():
    return CliRunner()

@pytest.fixture
def common_compound():
    return 'ATP'

def test_actualize_atp(runner, common_compound):
    result = runner.invoke(cdt.cli, ['actualize', common_compound])
    
    assert result.exit_code == 0
    assert result.output == """-------------------------------------
|              name | value         |
|-----------------------------------|
|          compound | ATP           |
|              name | ADENOSINE-... |
|           formula | C10 H16 N5... |
|             inchi | InChI=1S/C... |
|         inchi_key | ZKHQWZAMYR... |
|            smiles | c1nc(c2c(n... |
| cross_links_count | 22            |
-------------------------------------
"""


def test_default_hello(runner):
    result = runner.invoke(cdt.cli, input='\n')
    assert result.exit_code == 0
    print(result.output)
    expected = 'greet whom? [world]: \nHello world!\n'
    assert result.output == expected