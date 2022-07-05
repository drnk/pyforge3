from click.testing import CliRunner
import pytest

from src import cdt as cdt
from src.cdt import SUPPORTED_COMPOUNDS


@pytest.fixture(scope="module")
def runner():
    return CliRunner()


@pytest.fixture
def common_compound():
    return 'ATP'


@pytest.fixture
def unsupported_compound():
    return 'WWW'


def test_actualize_common(runner, common_compound):
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


def test_actualize_common_full(runner, common_compound):
    result = runner.invoke(
        cdt.cli, ['actualize', '--full', common_compound])

    assert result.exit_code == 0
    expected = """-----------------------------------------------------------------------------------
|              name | value                                                       |
|---------------------------------------------------------------------------------|
|          compound | ATP                                                         |
|              name | ADENOSINE-5'-TRIPHOSPHATE                                   |
|           formula | C10 H16 N5 O13 P3                                           |
|             inchi | InChI=1S/C10H16N5O13P3/c11-8-5-9(13-2-12-8)15(3-14-5)10-7(1 |
|                   | 7)6(16)4(26-10)1-25-30(21,22)28-31(23,24)27-29(18,19)20/h2- |
|                   | 4,6-7,10,16-17H,1H2,(H,21,22)(H,23,24)(H2,11,12,13)(H2,18,1 |
|                   | 9,20)/t4-,6-,7-,10-/m1/s1                                   |
|         inchi_key | ZKHQWZAMYRWXGA-KQYNXXCUSA-N                                 |
|            smiles | c1nc(c2c(n1)n(cn2)C3C(C(C(O3)COP(=O)(O)OP(=O)(O)OP(=O)(O)O) |
|                   | O)O)N                                                       |
| cross_links_count | 22                                                          |
-----------------------------------------------------------------------------------
"""
    assert result.output == expected


def test_actualize_unsupported(runner, unsupported_compound):
    result = runner.invoke(
        cdt.cli, ['actualize', unsupported_compound]
    )

    assert result.exit_code == 0
    expected = """Compound WWW is not supported
Supported compounds are: ADP, ATP, STI, ZID, DPM, XP9, 18W, 29P
"""
    assert result.output == expected


def test_actualize_empty(runner):
    result = runner.invoke(
        cdt.cli, ['actualize']
    )

    assert result.exit_code == 2
    expected_ending = "Error: Missing argument 'COMPOUND'."
    assert result.output.strip().split('\n').pop() == expected_ending


def test_supported(runner):
    result = runner.invoke(
        cdt.cli, ['supported']
    )

    expected_strings = set(SUPPORTED_COMPOUNDS)
    expected_strings.add('Next compounds are supported by cdt:')

    output_set = set([s.strip() for s in result.output.split('\n') if s.strip()])
    assert result.exit_code == 0
    assert output_set == expected_strings


def test_remove_common(runner, common_compound):
    # actualize the information about compound
    result = runner.invoke(cdt.cli, ['actualize', common_compound])
    assert result.exit_code == 0

    # check that summary is present at local db
    result = runner.invoke(cdt.cli, ['ls'])
    assert common_compound in result.output

    # remove the compound summary from local db
    result = runner.invoke(cdt.cli, ['remove', common_compound])
    expected = f"Compound {common_compound} succesfully removed."
    assert result.output.strip() == expected

    # try again to remove the same compound from local db
    result = runner.invoke(cdt.cli, ['remove', common_compound])
    expected = f"Compound {common_compound} summary is missing "\
        "in local database. Nothing to remove."
    assert result.output.strip() == expected
