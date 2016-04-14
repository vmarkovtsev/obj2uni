import sys

PY2 = sys.version_info[0] == 2

if not PY2:
    from functools import reduce


def obj2uni(*seqs):
    """
    Maps each sequence from seqs to unicode strings with characters within
    range 0 - 0x10FFFF (0 - 0xFFFF on narrow Python 2.x builds - those
    not configured with --enable-unicode=ucs4).
    :param seqs: The sequences of arbitrary objects to map.
    :return: tuple <mapped strings>, <character to object mapping>
    """
    allobjs = reduce(set.union, map(set, seqs))
    uchr = chr if not PY2 else unichr
    try:
        uchr(0x100000)
        maxlen = 0x110000
    except ValueError:
        maxlen = 0x10000
    if len(allobjs) > maxlen:
        raise ValueError("Too large number of distinct objects (%d), maximum "
                         "is %d" % (len(allobjs), maxlen))
    mapping = {obj: uchr(i) for i, obj in enumerate(sorted(allobjs))}
    mapped = tuple("".join(mapping[obj] for obj in seq) for seq in seqs)
    inv_mapping = {char: obj for obj, char in mapping.items()}
    return mapped, inv_mapping
