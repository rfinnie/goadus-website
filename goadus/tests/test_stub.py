# SPDX-PackageName: goadus-website
# SPDX-PackageSupplier: Ryan Finnie <ryan@finnie.org>
# SPDX-PackageDownloadLocation: https://github.com/finnix/goadus-website
# SPDX-FileCopyrightText: © 2020 Ryan Finnie <ryan@finnie.org>
# SPDX-License-Identifier: MPL-2.0

import unittest
import warnings


class TestStub(unittest.TestCase):
    def test_stub(self):
        # pytest doesn't like a tests/ with no tests
        warnings.warn("Remove this file once unit tests are added")
