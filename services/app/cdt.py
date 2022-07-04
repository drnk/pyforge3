import click
import logging
import requests
import sys

from more_itertools import chunked

from storage import CompoundSummary, Storage



LOGGING_LEVEL = logging.DEBUG
root = logging.getLogger()
root.setLevel(LOGGING_LEVEL)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(LOGGING_LEVEL)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
root.addHandler(handler)


SUPPORTED_COMPOUNDS = (
    'ADP', 'ATP', 'STI', 'ZID', 'DPM', 'XP9', '18W', '29P'
)

EBI_COMPOUND_SUMMARY_URL = 'https://www.ebi.ac.uk/pdbe/graph-api/compound/summary/{hetcode}'


def parse_compound_summary(data: dict) -> dict:
    """Filters summary data to leave the necessary only.

    Args:
        data: dictionary of compound summary information

    Returns:
        dict with necessary compound information
    """
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

def is_compound_supported(hetcode: str) -> bool:
    """Check if compound supported by `cdt`
    
    Args:
        hetcode: string code of compound
        
    Returns:
        True is supported and False if not
    """
    return hetcode in SUPPORTED_COMPOUNDS

def not_supported_info(hetcode: str) -> None:
    """Printing into terminal warning about unsupported compound.
    
    Args:
        hetcode: string code of compound
    """
    click.echo(click.style(f"Compound {hetcode} is not supported", bg='red', fg='white'))
    click.echo(f"Supported compounds are: {', '.join(SUPPORTED_COMPOUNDS)}")

def get_compound_summary(compound: str) -> dict:
    """Downloads compound summary info from PDB (Protein Data Bank) API

    For the reference:
        https://www.ebi.ac.uk/pdbe/graph-api/pdbe_doc/#api-Compounds-GetCompoundSummary
    
    Args:
        compound: hetcode of the compound 
    
    Returns:
        dict object with following keys:
            compound - Hetcode of the compound.
            name - The name of the chemical component.
            formula - The chemical formula of the component.
            inchi - The full INCHI of the component.
            inchi_key - INCHI key of the component.
            smiles - The SMILES representation of the component
                (could be multiple).
            cross_links_count - Quantity of cross references for this
                chemical component from other resources.
    
    Raises:
        ValueError: if 'compound' is not supported
        RuntimeError: if wearn't able to retreive information from 
            public API 

    """
    compound = compound.upper().strip()

    if not is_compound_supported(compound):
        raise ValueError(f"Compound '{compound}' is not supported yet. "\
            f"Please try supported ones: {str(SUPPORTED_COMPOUNDS)}")

    url = EBI_COMPOUND_SUMMARY_URL.format(hetcode=compound)
    r = requests.get(url)
    if r.status_code != 200:
        raise RuntimeError(f"Something goes wrong while retreiving "\
            f"information via url: {url}")

    return parse_compound_summary(r.json())


def prepare_compound_info(data: dict, full: bool = False) -> list:
    """Prepare ANSI representation of CompoundSummary data.
    
    Args:
        data: compound summary dictionary
        
    Returns:
        list of strings to print in ASCII manner into terminal
    """
    logging.debug(f"call prepare_compound_info(data={data}, full={full})...")

    C1_WIDTH = 17
    if full:
        C2_WIDTH = 79 - 13 - 7  # 59
        TMP = "| {:>17} | {:<59} |"
    else:
        C2_WIDTH = 13
        TMP = "| {:>17} | {:<13} |"

    s = []

    # table header
    s.append('-'*(2 + C1_WIDTH + 3 + C2_WIDTH + 2))
    s.append(TMP.format('name', 'value'))
    s.append('|' + '-'*(1 + C1_WIDTH + 3 + C2_WIDTH + 1) + '|')
    
    # table body
    for k, v in data.items():
        val = str(v)

        if not full: 
            s.append(TMP.format(k, v if len(val) < 14 else f"{val[:10]}..."))
        else:
            is_first = True
            for part in chunked(val, C2_WIDTH):
                name = k if is_first else ''
                s.append(TMP.format(name, ''.join(part)))
                
                if is_first:
                    is_first = False
    
    # table footer
    s.append('-'*(2 + C1_WIDTH + 3 + C2_WIDTH + 2))
    return s


# prepare decorator via click to pass Storage
# instance as a context object to the commands
pass_storage = click.make_pass_decorator(Storage)

@click.group()
@click.option("--verbose", "-v", is_flag=True, help="Enables verbose mode.")
@click.version_option("1.0")
@click.pass_context
def cli(ctx, verbose):
    """Compound-data-tool or CDT is a command line tool allows you to actualize
    the information about compounds.

    Args:
        ctx: click context (passed automatically by click)
        verbose: boolean value of additional output necessity
    """
    ctx.obj = Storage(debug=verbose)

@cli.command()
@click.argument("compound")
@click.option(
    '--full',
    is_flag=True,
    default=False,
    help="Show compound information without cutting long strings")
@pass_storage
def actualize(storage, compound, full):
    """Actualizing compound data from the open source APIs.

    This will retreive the information from www.ebi.ac.uk database and store it 
    locally for further use.

    Supported compounds are: ADP, ATP, STI, ZID, DPM, XP9, 18W, 29P
    """
    logging.debug(
        f"call command actualize(storage={storage}, "
        f"compound={compound}, full={full})")
    
    compound = compound.upper().strip()
    if not is_compound_supported(compound):
        not_supported_info(compound)
        return

    data = get_compound_summary(compound)

    for s in prepare_compound_info(data, full):
        click.echo(s)

    # storing the info to database
    summary = CompoundSummary(**data)
    storage.save(summary)

@cli.command()
def supported():
    """Information about supported compounds."""
    click.echo("Next compounds are supported by cdt:")
    for compound in SUPPORTED_COMPOUNDS:
        click.echo('  ' + compound)

@cli.command()
@click.argument("compound")
@click.option(
    '--full',
    is_flag=True,
    default=False,
    help="Show compound information without cutting long strings")
@pass_storage
def show(storage, compound, full=True):
    """Show compound summary from local data storage."""
    logging.info(f"Showing the summary data for '{compound}' compound")
    logging.debug(f"call show(storage={storage}, compound={compound}, full={full})...")
    
    full_info = bool(full)
    compound = compound.upper().strip()
    if not is_compound_supported(compound):
        not_supported_info(compound)
        return

    data = storage.get(compound)

    if not data:
        click.echo(f"We don't have a local copy of the {compound} summary.")
        click.echo(f"Run `cdt actualize {compound}` once to obtain the info.")
    else:
        for s in prepare_compound_info(data, full_info):
            click.echo(s)

if __name__ == '__main__':
    cli()