import re
import logging
from functools import lru_cache
from typing import Callable, Optional, Dict, Match

from fingerprints.types.data import TYPES
from fingerprints.constants import WS
from fingerprints.cleanup import clean_name_ascii

log = logging.getLogger(__name__)
NormFunc = Callable[[Optional[str]], Optional[str]]
ReplaceFunc = Callable[[Optional[str]], Optional[str]]


class Replacer(object):
    def __init__(self, replacements: Dict[str, str], remove: bool = False) -> None:
        self.replacements = replacements
        self.remove = remove
        forms = set(self.replacements.keys())
        if remove:
            forms.update(self.replacements.values())
        forms_sorted = sorted(forms, key=lambda ct: -1 * len(ct))
        forms_sorted = [re.escape(f) for f in forms_sorted]
        forms_regex = "\\b(%s)\\b" % "|".join(forms_sorted)
        self.matcher = re.compile(forms_regex, re.U | re.I)

    def get_canonical(self, match: Match[str]) -> str:
        if self.remove:
            return WS
        return self.replacements.get(match.group(1), match.group(1))

    def __call__(self, text: Optional[str]) -> Optional[str]:
        if text is None:
            return None
        return self.matcher.sub(self.get_canonical, text)


def normalize_replacements(norm_func: NormFunc) -> Dict[str, str]:
    replacements: Dict[str, str] = {}
    for type in TYPES["types"]:
        main_norm = norm_func(type["main"])
        if main_norm is None:
            log.warning("Main form is normalized to null: %r", type["main"])
            continue
        for form in type["forms"]:
            form_norm = norm_func(form)
            if form_norm is None:
                log.warning("Form is normalized to null [%r]: %r", type["main"], form)
                continue
            if form_norm == main_norm:
                continue
            if form_norm in replacements and replacements[form_norm] != main_norm:
                log.warning(
                    "Form has duplicate mains: %r (%r, %r)",
                    form,
                    replacements[form_norm],
                    main_norm,
                )
                continue
            replacements[form_norm] = main_norm
    return replacements


@lru_cache(maxsize=None)
def get_replacer(
    clean: NormFunc = clean_name_ascii, remove: bool = False
) -> ReplaceFunc:
    replacements = normalize_replacements(clean)
    return Replacer(replacements, remove=remove)


if __name__ == "__main__":
    get_replacer()
