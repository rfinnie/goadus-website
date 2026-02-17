# SPDX-PackageName: goadus-website
# SPDX-PackageSupplier: Ryan Finnie <ryan@finnie.org>
# SPDX-PackageDownloadLocation: https://github.com/finnix/goadus-website
# SPDX-FileCopyrightText: © 2020 Ryan Finnie <ryan@finnie.org>
# SPDX-License-Identifier: MPL-2.0

import random

from .werder import Werder


def werder_api_key():
    w = Werder()
    return "-".join([w.werd() for _ in range(4)])


def werder_name():
    w = Werder()
    return "{}-{}".format(w.werd(), int(random.uniform(0, 999)))
