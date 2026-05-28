# SPDX-PackageName: goadus-website
# SPDX-PackageSupplier: Ryan Finnie <ryan@finnie.org>
# SPDX-PackageDownloadLocation: https://forge.colobox.com/rfinnie/goadus-website
# SPDX-FileCopyrightText: © 2020 Ryan Finnie <ryan@finnie.org>
# SPDX-License-Identifier: MPL-2.0

import random

from .baat import BAAT
from .werder import Werder


def make_api_key():
    return str(BAAT(prefix="goadus"))


def werder_name():
    w = Werder()
    return "{}-{}".format(w.werd(), int(random.uniform(0, 999)))
