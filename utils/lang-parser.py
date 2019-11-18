#!/usr/bin/env python3
"""
This module parsers the text file at

 https://www.iana.org/assignments/language-subtag-registry/language-subtag-registry

to a Swift dictionary with key: value defined as language subtag : language(s)

Usage:

$ python3 lang-parser.py [PATH to IANA language subtag registry text file]

The script writes `SwiftLangDict.swift` in the working directory.  This file
includes filtered IANA data as a Swift formatted dictionary.

Please refer to the source below for the data filters that are used during
parsing of the IANA data file.
"""

import os
import re
import sys


def main(argv):
    raw_lang_filepath = argv[0]
    if not os.path.exists(raw_lang_filepath):
        sys.stderr.write(f"{raw_lang_filepath} is not a path to a valid file.")
        sys.exit(1)

    # regular expressions
    regex_subtag = re.compile(r"Subtag:\s(?P<subtag>.*)")
    regex_lang = re.compile(r"Description:\s(?P<lang>.*)")

    raw_lang_list = []
    deprecated_lang_list = []
    redundant_lang_list = []
    extlang_lang_list = []
    script_list = []
    region_list = []
    active_lang_list = []
    lang_subtag_dict = {}

    # first pass to filter deprecated lang subtags
    with open(raw_lang_filepath, "r") as f:
        raw_text = f.read()
        raw_lang_list = raw_text.split("%%\n")
        for lang in raw_lang_list:
            # remove deprecated subtags
            if "Deprecated:" in lang:
                deprecated_lang_list.append(lang)
            # remove grandfathered / redundant tags
            # see https://www.w3.org/International/articles/language-tags/#grandfathered
            elif "Type: grandfathered" in lang or "Type: redundant" in lang:
                redundant_lang_list.append(lang)
            # remove extlang tags (rationale: not primary languages)
            elif "Type: extlang" in lang:
                extlang_lang_list.append(lang)
            # remove scripts (rationale: not languages)
            elif "Type: script" in lang:
                script_list.append(lang)
            # remove regions (rationale: not languages)
            elif "Type: region" in lang:
                region_list.append(lang)
            # header of file includes date of spec file
            # print that and do not include in list of lang subtags
            elif "File-Date:" in lang:
                print(f"{lang}")
            else:
                active_lang_list.append(lang)

    # Report the number of filtered items by category
    print(f"Filtered {len(deprecated_lang_list)} deprecated language Subtags...")
    print(
        f"Filtered {len(redundant_lang_list)} grandfathered / redundant language Tags..."
    )
    print(f"Filtered {len(extlang_lang_list)} extended language tags...")
    print(f"Filtered {len(script_list)} script tags...")
    print(f"Filtered {len(region_list)} region tags...")

    # parse the language data for subtags and language descriptions
    for a_lang in active_lang_list:
        st_search = regex_subtag.search(a_lang)
        subtag = st_search.group("subtag")
        if ".." in subtag:
            # there are subtag ranges that are private use area
            # exclude these from the final set of subtags
            print(f"Filtered subtag range '{subtag}'...")
        else:
            lang_search_list = regex_lang.findall(a_lang)
            language_description = "; ".join(lang_search_list)
            language_description = language_description.replace('"', "'")
            lang_subtag_dict[subtag] = language_description

    # compose Swift source from the parsed data
    swift_lang_dict = "let langDict = [\n"
    sorted_lang_keys = sorted(lang_subtag_dict)

    for k in sorted_lang_keys:
        swift_lang_dict += f'    "{k}": "{lang_subtag_dict[k]}",\n'

    swift_lang_dict += "]\n"

    with open("SwiftLangDict.swift", "w") as f:
        f.write(swift_lang_dict)


if __name__ == "__main__":
    main(sys.argv[1:])
