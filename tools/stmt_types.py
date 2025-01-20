import csv
import yaml
import logging
from pprint import pprint
from types import NoneType
from typing import Any, Dict, List, Optional, Set
import click
from pathlib import Path

from fingerprints.util import DATA_PATH
from fingerprints.cleanup import clean_name_ascii
from fingerprints.types.replacer import Replacer

log = logging.getLogger("stmt_types")
TYPES_PATH = DATA_PATH / "types.yml"


def display_norm(text: str) -> str:
    return text


def compare_norm(text: str) -> Optional[str]:
    return clean_name_ascii(text) or ""


class CompanyType(object):
    def __init__(self, data: Dict[str, Any]) -> None:
        self.display: Optional[str] = data.pop("display", None)
        assert isinstance(self.display, (NoneType, str)), self.display
        self.compare: Optional[str] = data.pop("compare", None)
        assert isinstance(self.compare, (NoneType, str)), self.compare
        self.aliases: List[str] = data.pop("aliases", [])
        if len(data):
            log.warning("Unused keys: %r", list(data.keys()))


def load_replacers() -> Dict[str, Replacer]:
    with open(TYPES_PATH, "r") as fh:
        data = yaml.load(fh, yaml.SafeLoader)
    cts: List[CompanyType] = []
    for item in data["company_types"]:
        ct = CompanyType(item)
        cts.append(ct)

    display_replacements: Dict[str, str] = {}
    for ct in cts:
        if ct.display is None:
            continue
        for alias in ct.aliases:
            lalias = display_norm(alias).lower()
            norm = display_norm(ct.display)
            if alias in display_replacements and display_replacements[lalias] != norm:
                log.warning(
                    "Duplicate display alias [%r/%r]: %r",
                    display_replacements[lalias],
                    ct.display,
                    alias,
                )
            else:
                display_replacements[lalias] = norm
    # example = "limited liability company"
    # assert example not in display_replacements, display_replacements[example]
    # pprint(display_replacements)

    compare_replacements: Dict[str, str] = {}
    compare_norms: Set[str] = set()
    for ct in cts:
        if ct.compare is None:
            continue
        aliases = set([compare_norm(a) for a in ct.aliases])
        for alias in aliases:
            norm = compare_norm(ct.compare)
            compare_norms.add(norm)
            if alias in compare_replacements and compare_replacements[alias] != norm:
                log.warning(
                    "Duplicate compare alias [%r/%r]: %r %r",
                    compare_replacements[alias],
                    ct.compare,
                    alias,
                    ct.aliases,
                )
            else:
                compare_replacements[alias] = norm

    log.info("Comparison types (normalised): %r", sorted(compare_norms))

    return {
        "display": Replacer(display_replacements, ignore_case=True),
        "compare": Replacer(compare_replacements),
    }


def transform_row(
    replacers: Dict[str, Replacer], stmt: Dict[str, str]
) -> Optional[Dict[str, str]]:
    name = stmt["value"]
    display_name = display_norm(name)
    display_out = replacers["display"](display_name)

    compare_name = compare_norm(name)
    compare_out = replacers["compare"](compare_name)
    # Testing mode
    if display_name == display_out and compare_name == compare_out:
        # If both the display and compare outputs are the same as original, indicate that it's unadjusted
        return {
            "name": name,
            "lang": stmt["lang"],
            "display": display_out,
            "compare": compare_out,
            "entity": stmt["entity_id"],
        }
    # If there's any change, return None to indicate this row has been adjusted
    return None


@click.command()
@click.argument("stmt_csv", type=click.Path(exists=True))
@click.argument("out_csv", type=click.Path())
def parse(stmt_csv: Path, out_csv: Path):
    logging.basicConfig(level=logging.INFO)
    replacers = load_replacers()
    with open(stmt_csv, "r") as sfh:
        with open(out_csv, "w") as ofh:
            writer = csv.DictWriter(
                ofh, fieldnames=["name", "lang", "display", "compare", "entity"]
            )
            writer.writeheader()
            for i, stmt in enumerate(csv.DictReader(sfh)):
                if i % 1_000_000 == 0 and i > 0:
                    log.info(f"Processed {i} rows")

                # # Sample every tenth row:
                # if i % 10 == 0:
                #     continue
                if stmt["schema"] not in ("Organization", "Company"):
                    continue

                if stmt["prop_type"] != "name":
                    continue
                out = transform_row(replacers, stmt)
                if out is not None:
                    writer.writerow(out)


if __name__ == "__main__":
    parse()
