import click
import requests


SUPPORTED_COMPOUNDS = (
    'ADP', 'ATP', 'STI', 'ZID', 'DPM', 'XP9', '18W', '29P'
)

EBI_COMPOUND_SUMMARY_URL = 'https://www.ebi.ac.uk/pdbe/graph-api/compound/summary/{compound}'


def parse_compound_summary(data):
    res = dict()
    res['compound'] = tuple(data.keys())[0]

    details = data[res['compound']][0]
    res['name'] = details['name']
    res['formula'] = details['formula']
    res['inchi'] = details['inchi']
    res['inchi_key'] = details['inchi_key']
    res['smiles'] = details['smiles']
    res['cross_links_count'] = len(details['cross_links'])

    return res


def get_compound_summary(compound):

    compound = compound.upper().strip()

    if not compound in SUPPORTED_COMPOUNDS:
        raise RuntimeError(f"Compound '{compound}' is not supported yet. "\
            f"Please try supported ones: {str(SUPPORTED_COMPOUNDS)}")

    url = EBI_COMPOUND_SUMMARY_URL.format(compound=compound)
    r = requests.get(url)
    if r.status_code != 200:
        raise RuntimeError(f"Something goes wrong while retreiving "\
            f"information via url: {url}")

    return parse_compound_summary(r.json())
    
def prepare_compound_info(data):
    C1_WIDTH = 17
    C2_WIDTH = 13

    TMP = "| {:>17} | {:<13} |"
    s = []
    s.append('-'*(2 + C1_WIDTH + 3 + C2_WIDTH + 2))
    s.append(TMP.format('name', 'value'))
    s.append('|' + '-'*(1 + C1_WIDTH + 3 + C2_WIDTH + 1) + '|')
    for k, v in data.items():
        val = str(v)
        s.append(TMP.format(k, v if len(val) < 14 else f"{val[:10]}..."))
    s.append('-'*(2 + C1_WIDTH + 3 + C2_WIDTH + 2))
    return s


@click.group()
@click.option("--verbose", "-v", is_flag=True, help="Enables verbose mode.")
@click.version_option("1.0")
def cli(verbose):
    """Compound-data-tool or CDT is a command line tool allows you to actualize
    the information about compounds.

    """
    pass

@cli.command()
@click.argument("compound")
def actualize(compound):
    """Actualizing compound data from the open source APIs.

    This will retreive the information from www.ebi.ac.uk database and store it 
    locally for further use.

    Supported compounds are: ADP, ATP, STI, ZID, DPM, XP9, 18W, 29P
    """
    compound = compound.upper().strip()
    if not compound in SUPPORTED_COMPOUNDS:
        click.echo(click.style(f"Compound {compound} is not supported", bg='red', fg='white'))
        click.echo(f"Supported compounds are: {', '.join(SUPPORTED_COMPOUNDS)}")
        return

    data = get_compound_summary(compound)

    for s in prepare_compound_info(data):
        click.echo(s)

@cli.command()
def supported():
    """Information about supported compounds."""
    click.echo("Next compounds are supported by cdt:")
    for compound in SUPPORTED_COMPOUNDS:
        click.echo('  ' + compound)