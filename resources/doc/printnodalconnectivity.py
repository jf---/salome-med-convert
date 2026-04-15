import string
import sys

import medcoupling as medc

from medconverter.engine.connectivity import ConnectivityRenumberer

letters = list(string.ascii_uppercase)

name = sys.argv[1].upper()

c = ConnectivityRenumberer(name)


def sequence(el):

    nb = el
    for i in letters:
        nb = nb.replace(i, "")

    nb = int(nb)
    nodes = 1 + medc.DataArrayInt(list(range(nb)))

    return c.external_to_medcoupling(getattr(medc, "NORM_%s" % el), nodes)


for i in sorted(getattr(c, ("_%s" % name).lower())):
    seq = sequence(i)
    line = "{" + ",".join(map(str, seq)) + "}"
    print(i, line)
