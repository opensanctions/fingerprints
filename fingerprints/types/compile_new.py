import yaml
from types import NoneType
from typing import Any, Dict, List, Optional, Set

from fingerprints.util import DATA_PATH

TYPES_PATH = DATA_PATH / "types.yml"


class CompanyType(object):
    def __init__(self, data: Dict[str, Any]) -> None:
        self.normal: Optional[str] = data.pop("normal", None)
        self.broader: Optional[str] = data.pop("broader", None)
        self.generic: Optional[str] = data.pop("generic", None)
        assert isinstance(self.generic, (NoneType, str)), self.normal
        self.aliases: List[str] = data.pop("aliases", [])


def verify() -> None:
    with open(TYPES_PATH, "r") as fh:
        data = yaml.load(fh, yaml.SafeLoader)
    cts: List[CompanyType] = []
    for item in data["company_types"]:
        ct = CompanyType(item)
        cts.append(ct)

    normals: Set[str] = set()
    generics: Set[str] = set()
    broaders: Set[str] = set()
    for ct in cts:
        if ct.normal:
            if ct.normal in normals:
                print("Duplicate normal: %r" % ct.normal)
            normals.add(ct.normal)
        if ct.generic:
            generics.add(ct.generic)
        if ct.broader:
            broaders.add(ct.broader)

    print("All generics: %r" % sorted(generics))


if __name__ == "__main__":
    verify()
