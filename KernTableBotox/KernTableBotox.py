# ----------------------------------------
# imports
# ----------------------------------------

import itertools
import time

from fontTools import ttLib
import click

from . import input_helpers

# ----------------------------------------
# constants
# ----------------------------------------


TARGETS = [".otf", ".woff", ".woff2", ".ttf"]

KERN_SUBSET = [
    ".notdef",
    "Eth",
    "eth",
    "Lslash",
    "lslash",
    "Scaron",
    "scaron",
    "Yacute",
    "yacute",
    "Thorn",
    "thorn",
    "Zcaron",
    "zcaron",
    "onehalf",
    "onequarter",
    "onesuperior",
    "threequarters",
    "threesuperior",
    "twosuperior",
    "brokenbar",
    "minus",
    "multiply",
    "space",
    "exclam",
    "quotedbl",
    "numbersign",
    "dollar",
    "percent",
    "ampersand",
    "quotesingle",
    "parenleft",
    "parenright",
    "asterisk",
    "plus",
    "comma",
    "hyphen",
    "period",
    "slash",
    "zero",
    "one",
    "two",
    "three",
    "four",
    "five",
    "six",
    "seven",
    "eight",
    "nine",
    "colon",
    "semicolon",
    "less",
    "equal",
    "greater",
    "question",
    "at",
    "A",
    "B",
    "C",
    "D",
    "E",
    "F",
    "G",
    "H",
    "I",
    "J",
    "K",
    "L",
    "M",
    "N",
    "O",
    "P",
    "Q",
    "R",
    "S",
    "T",
    "U",
    "V",
    "W",
    "X",
    "Y",
    "Z",
    "bracketleft",
    "backslash",
    "bracketright",
    "asciicircum",
    "underscore",
    "grave",
    "a",
    "b",
    "c",
    "d",
    "e",
    "f",
    "g",
    "h",
    "i",
    "j",
    "k",
    "l",
    "m",
    "n",
    "o",
    "p",
    "q",
    "r",
    "s",
    "t",
    "u",
    "v",
    "w",
    "x",
    "y",
    "z",
    "braceleft",
    "bar",
    "braceright",
    "asciitilde",
    "Adieresis",
    "Aring",
    "Ccedilla",
    "Eacute",
    "Ntilde",
    "Odieresis",
    "Udieresis",
    "aacute",
    "agrave",
    "acircumflex",
    "adieresis",
    "atilde",
    "aring",
    "ccedilla",
    "eacute",
    "egrave",
    "ecircumflex",
    "edieresis",
    "iacute",
    "igrave",
    "icircumflex",
    "idieresis",
    "ntilde",
    "oacute",
    "ograve",
    "ocircumflex",
    "odieresis",
    "otilde",
    "uacute",
    "ugrave",
    "ucircumflex",
    "udieresis",
    "dagger",
    "degree",
    "cent",
    "sterling",
    "section",
    "bullet",
    "paragraph",
    "germandbls",
    "registered",
    "copyright",
    "trademark",
    "acute",
    "dieresis",
    "AE",
    "Oslash",
    "yen",
    "ordfeminine",
    "ordmasculine",
    "ae",
    "oslash",
    "questiondown",
    "exclamdown",
    "guillemotleft",
    "guillemotright",
    "ellipsis",
    "uni00A0",
    "Agrave",
    "Atilde",
    "Otilde",
    "OE",
    "oe",
    "endash",
    "emdash",
    "quotedblleft",
    "quotedblright",
    "quoteleft",
    "quoteright",
    "ydieresis",
    "Ydieresis",
    "fraction",
    "Euro",
    "guilsinglleft",
    "guilsinglright",
    "fi",
    "fl",
    "daggerdbl",
    "periodcentered",
    "quotesinglbase",
    "quotedblbase",
    "perthousand",
    "Acircumflex",
    "Ecircumflex",
    "Aacute",
    "Edieresis",
    "Egrave",
    "Iacute",
    "Icircumflex",
    "Idieresis",
    "Igrave",
    "Oacute",
    "Ocircumflex",
    "Ograve",
    "Uacute",
    "Ucircumflex",
    "Ugrave",
    "dotlessi",
    "circumflex",
    "tilde",
    "macron",
    "breve",
    "dotaccent",
    "ring",
    "cedilla",
    "hungarumlaut",
    "ogonek",
    "caron",
    "ff",
    "ffi",
    "ffl",
    "commaaccent",
    "Abreve",
    "abreve",
    "Amacron",
    "amacron",
    "Aogonek",
    "aogonek",
    "Cacute",
    "cacute",
    "Ccaron",
    "ccaron",
    "Ccircumflex",
    "ccircumflex",
    "Cdotaccent",
    "cdotaccent",
    "Dcaron",
    "dcaron",
    "Dcroat",
    "dcroat",
    "uni0237",
    "Ecaron",
    "ecaron",
    "Edotaccent",
    "edotaccent",
    "Emacron",
    "emacron",
    "Eogonek",
    "eogonek",
    "Gbreve",
    "gbreve",
    "Gcircumflex",
    "gcircumflex",
    "Gcommaaccent",
    "gcommaaccent",
    "Gdotaccent",
    "gdotaccent",
    "Hbar",
    "hbar",
    "Hcircumflex",
    "hcircumflex",
    "Idotaccent",
    "i.dot",
    "idotaccent",
    "Imacron",
    "imacron",
    "Iogonek",
    "iogonek",
    "Jcircumflex",
    "jcircumflex",
    "Kcommaaccent",
    "kcommaaccent",
    "Lacute",
    "lacute",
    "Lcaron",
    "lcaron",
    "Lcommaaccent",
    "lcommaaccent",
    "Nacute",
    "nacute",
    "Ncaron",
    "ncaron",
    "Ncommaaccent",
    "ncommaaccent",
    "Ohungarumlaut",
    "ohungarumlaut",
    "Omacron",
    "omacron",
    "Racute",
    "racute",
    "Rcaron",
    "rcaron",
    "Rcommaaccent",
    "rcommaaccent",
    "Sacute",
    "sacute",
    "Scedilla",
    "scedilla",
    "Scircumflex",
    "scircumflex",
    "Scommaaccent",
    "scommaaccent",
    "Tcaron",
    "tcaron",
    "uni021A",
    "uni021B",
    "Tcommaaccent",
    "tcommaaccent",
    "Ubreve",
    "ubreve",
    "Uhungarumlaut",
    "uhungarumlaut",
    "Umacron",
    "umacron",
    "Uogonek",
    "uogonek",
    "Uring",
    "uring",
    "Zacute",
    "zacute",
    "Zdotaccent",
    "zdotaccent",
]

# ----------------------------------------
# helpers
# ----------------------------------------


def extract_kern_data(f):
    gpos = f.get("GPOS")

    # sort lookups index by feature tag

    features_to_lookup_index = {}
    for fea in gpos.table.FeatureList.FeatureRecord:
        features_to_lookup_index.setdefault(fea.FeatureTag, set())
        features_to_lookup_index[fea.FeatureTag] |= set(
            fea.Feature.LookupListIndex
        )
    feature_to_lookup = {}
    for fea, lookup_indexes in features_to_lookup_index.items():
        feature_to_lookup[fea] = []
        for i in lookup_indexes:
            feature_to_lookup[fea].append(gpos.table.LookupList.Lookup[i])

    # extract kern values

    kern = feature_to_lookup.get("kern", [])
    my_kern = {}
    for look in kern:
        for subtable in look.SubTable:
            # deal with extension subtables
            if hasattr(subtable, "ExtSubTable"):
                subtable = subtable.ExtSubTable
            # deal with glyph kerning
            if hasattr(subtable, "Format") and subtable.Format == 1:
                for i, pairSet in enumerate(subtable.PairSet):
                    for pairValueRecord in pairSet.PairValueRecord:
                        if pairValueRecord.Value1.XAdvance != 0:
                            my_kern[
                                (
                                    subtable.Coverage.glyphs[i],
                                    pairValueRecord.SecondGlyph,
                                )
                            ] = pairValueRecord.Value1.XAdvance

            # deal with group kerning
            if hasattr(subtable, "Format") and subtable.Format == 2:
                groups_1 = {}
                groups_2 = {}
                for glyph, group_index in subtable.ClassDef1.classDefs.items():
                    groups_1.setdefault(group_index, []).append(glyph)
                for glyph, group_index in subtable.ClassDef2.classDefs.items():
                    groups_2.setdefault(group_index, []).append(glyph)

                # index 0 class is implicit. Great.
                grouped = [
                    g for group in list(groups_1.values()) for g in group
                ]
                groups_1[0] = [
                    g for g in subtable.Coverage.glyphs if g not in grouped
                ]

                for index_1, record_1 in enumerate(subtable.Class1Record):
                    for index_2, record_2 in enumerate(record_1.Class2Record):
                        if (
                            record_2.Value1.XAdvance != 0
                            and index_1 in groups_1
                            and index_2 in groups_2
                        ):
                            my_kern[
                                (
                                    tuple(groups_1[index_1]),
                                    tuple(groups_2[index_2]),
                                )
                            ] = record_2.Value1.XAdvance

    return my_kern


def flatten_kern(kern_dict, MIN_KERN_VALUE=None):
    flat_kern = {}
    for p, v in kern_dict.items():
        if MIN_KERN_VALUE and (v < -MIN_KERN_VALUE or v > MIN_KERN_VALUE):
            if type(p[0]) is tuple:
                for flat in itertools.product(*p):
                    flat_kern[flat] = v
            else:
                flat_kern[p] = v
        elif not MIN_KERN_VALUE:
            if type(p[0]) is tuple:
                for flat in itertools.product(*p):
                    flat_kern[flat] = v
            else:
                flat_kern[p] = v
    return flat_kern


def filter_kern(kern_dict, max_length, subset_kern=None):
    sorted_pairs = sorted(
        list(kern_dict.keys()), key=lambda x: abs(kern_dict[x]), reverse=True
    )
    if subset_kern:
        filtered_pairs = [
            i
            for i in list(sorted_pairs)
            if i[0] in subset_kern and i[1] in subset_kern
        ]
    else:
        filtered_pairs = sorted_pairs
    return {pair: kern_dict[pair] for pair in filtered_pairs[:max_length]}


def build_kern_table(flat_kern_dict):
    # partly based on samples from Jeremie Hornus
    # https://github.com/sansplomb/RobofontTools/blob/master/GenerateFont/GenerateFont.py

    kern_table = ttLib.newTable("kern")
    kern_table.version = 0
    kern_table.kernTables = []

    pair_list = list(flat_kern_dict.items())
    final_len_kern_list = str(len(pair_list))
    # pair_list = pair_list[:10920]
    # print(len(pair_list))
    # 10920 is the maximum subtable len
    for subtable_data in chunk_list(pair_list, 10920):
        # print(len(subtable_data))
        subtable = ttLib.tables._k_e_r_n.KernTable_format_0()
        subtable.kernTable = {}
        subtable.coverage = 1
        subtable.format = 0
        subtable.version = 0

        for p in subtable_data:
            subtable[p[0]] = p[1]

        kern_table.kernTables.append(subtable)
    return kern_table, final_len_kern_list


def chunk_list(list_, chunk_length):
    for i in range(0, len(list_), chunk_length):
        yield list_[i : i + chunk_length]


# ----------------------------------------


@click.command()
@click.option(
    "-o",
    "--output_dir",
    default=None,
    help="Specify a path for the output directory",
    type=click.Path(exists=False),
)
@click.option(
    "-t",
    "--suffix_tag",
    default="_kerntable",
    help="Specify a tag for the output file name (default is _kerntable)",
    type=str,
)
@click.option("--no_suffix", is_flag=True, help="Save output in place")
@click.option(
    "--subfolder/--no_subfolder",
    default=False,
    help="process subfolders recursively",
)
@click.option(
    "-p",
    "--pair_limit",
    is_flag=False,
    flag_value="Flag",
    default=10920,
    help=(
        "Limit the total number of kern pairs to save"
        "\nIf no number is given default is 10920"
    ),
    type=int,
)
@click.option(
    "-m",
    "--min_kern_value",
    help="Remove all kern pairs below the given value",
    type=int,
)
@click.option(
    "-s",
    "--subset",
    is_flag=True,
    help="Subset kerning based on predetermined list of Latin characters",
)
@click.option(
    "-c",
    "--char_list",
    help="Subset based on comma-separated list of glyph names",
    type=str,
)
@click.option(
    "-l",
    "--char_file",
    help="Subset based on file containing a list of glyph names, one per line",
)
@click.argument("input_path", type=click.Path(exists=False))
def inject_kern_table(
    input_path,
    output_dir,
    suffix_tag,
    no_suffix,
    subfolder,
    pair_limit,
    min_kern_value,
    subset,
    char_list,
    char_file,
):
    t = time.time()
    print("Kern Table Injection")

    # walk the i,put directory
    input_dir, font_path = input_helpers.walk_input_path(
        input_path, target_extentions=TARGETS, recursive=subfolder
    )
    font_count = 0
    MIN_KERN_VALUE = 0
    MAX_KERN_PAIRS = 1000000
    for p in font_path:
        print(subset)

        if output_dir:
            out_path = input_helpers.output_file_to_another_folder(
                p, output_dir
            )
        else:
            out_path = p

        if no_suffix:
            outpath = out_path
        else:
            outpath = input_helpers.suffix_file(out_path, suffix_tag)

        f = ttLib.TTFont(p)
        my_kern = extract_kern_data(f)
        if min_kern_value:
            MIN_KERN_VALUE = min_kern_value
        flat_kern = flatten_kern(my_kern, MIN_KERN_VALUE)

        if pair_limit and (subset or char_list or char_file):
            MAX_KERN_PAIRS = pair_limit
        else:
            MAX_KERN_PAIRS = pair_limit
            flat_kern = filter_kern(
                flat_kern, max_length=MAX_KERN_PAIRS, subset_kern=None
            )

        if subset:
            flat_kern = filter_kern(
                flat_kern, max_length=MAX_KERN_PAIRS, subset_kern=KERN_SUBSET
            )
        elif char_list:
            CHARACTER_LIST = [s.strip() for s in char_list.split(",")]
            flat_kern = filter_kern(
                flat_kern,
                max_length=MAX_KERN_PAIRS,
                subset_kern=CHARACTER_LIST,
            )
        elif char_file:
            CHARACTER_LIST = []
            with open(char_file) as charFile:
                CHARACTER_LIST = [c.rstrip() for c in charFile]
            flat_kern = filter_kern(
                flat_kern,
                max_length=MAX_KERN_PAIRS,
                subset_kern=CHARACTER_LIST,
            )

        f["kern"], final_count = build_kern_table(flat_kern)
        f.save(outpath)
        f.close()
        print(("%s -> done" % p))
        print(
            "Final number of kern pairs in kern table for "
            + p
            + ": "
            + final_count
        )
        font_count += 1

    print("")
    print(
        (
            "All done: %s font processed in %s secs"
            % (font_count, time.time() - t)
        )
    )
