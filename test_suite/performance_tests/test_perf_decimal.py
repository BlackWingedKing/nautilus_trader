# -------------------------------------------------------------------------------------------------
# <copyright file="test_perf_decimal.py" company="Nautech Systems Pty Ltd">
#  Copyright (C) 2015-2020 Nautech Systems Pty Ltd. All rights reserved.
#  The use of this source code is governed by the license as found in the LICENSE.md file.
#  https://nautechsystems.io
# </copyright>
# -------------------------------------------------------------------------------------------------

import decimal
import unittest

from nautilus_trader.core.decimal import Decimal
from nautilus_trader.model.objects import Price

from test_kit.performance import PerformanceProfiler


_PRECISION_5_CONTEXT = decimal.Context(prec=5)
_BUILTIN_DECIMAL1 = decimal.Decimal('1.00000')
_BUILTIN_DECIMAL2 = decimal.Decimal('1.00001')

_DECIMAL1 = Decimal(1.00000, 5)
_DECIMAL2 = Decimal(1.00001, 5)


class PriceInitializations:

    @staticmethod
    def make_builtin_decimal():
        decimal.Decimal('1.23456')

    @staticmethod
    def make_decimal():
        Decimal(1.23456, 5)

    @staticmethod
    def float_comparisons():
        # x1 = 1.0 > 2.0
        # x2 = 1.0 >= 2.0
        x3 = 1.0 == 2.0

    @staticmethod
    def float_arithmetic():
        x1 = 1.0 * 2.0

    @staticmethod
    def decimal_comparisons():
        # x1 = _DECIMAL1.value > _DECIMAL2.value
        # x2 = _DECIMAL1.value >= _DECIMAL2.value
        # x3 = _DECIMAL1.value == _DECIMAL2.value

        # x1 = _DECIMAL1.gt(_DECIMAL2)
        # x2 = _DECIMAL1.ge(_DECIMAL2)
        # x3 = _DECIMAL1.eq(_DECIMAL1)

        x3 = _DECIMAL1 == 1.0
        # x3 = _DECIMAL1.eq_float(1.0)

    @staticmethod
    def decimal_arithmetic():
        # x0 = _DECIMAL1 + 1.0
        x1 = _DECIMAL1 * 1.0

    @staticmethod
    def builtin_decimal_comparisons():
        x1 = _BUILTIN_DECIMAL1 > _BUILTIN_DECIMAL2
        x2 = _BUILTIN_DECIMAL1 >= _BUILTIN_DECIMAL2
        x3 = _BUILTIN_DECIMAL1 == _BUILTIN_DECIMAL2

    @staticmethod
    def make_price():
        Price(1.23456, 5)

    @staticmethod
    def make_price_from_string():
        Price.from_string('1.23456')


class DecimalPerformanceTests(unittest.TestCase):

    def test_builtin_decimal_size(self):

        result = PerformanceProfiler.object_size(_BUILTIN_DECIMAL1)
        # Object size test: <class 'nautilus_trader.core.decimal.Decimal'> is 48 bytes
        self.assertTrue(result == 104)

    def test_decimal_size(self):

        result = PerformanceProfiler.object_size(_DECIMAL1)
        # Object size test: <class 'nautilus_trader.core.decimal.Decimal'> is 48 bytes
        self.assertTrue(result <= 104)

    def test_decimal_to_string(self):

        result = PerformanceProfiler.profile_function(_DECIMAL1.to_string, 5, 1000000)
        # ~221ms (221710μs) minimum of 3 runs @ 1000000 iterations
        self.assertTrue(result < 0.25)

    def test_make_builtin_decimal(self):

        result = PerformanceProfiler.profile_function(PriceInitializations.make_builtin_decimal, 5, 1000000)
        # ~236ms (236837μs) minimum of 3 runs @ 1000000 iterations
        self.assertTrue(result < 0.3)

    def test_make_decimal(self):

        result = PerformanceProfiler.profile_function(PriceInitializations.make_decimal, 5, 1000000)
        # ~170ms (170577μs) minimum of 3 runs @ 1000000 iterations
        self.assertTrue(result < 0.2)

    def test_make_price(self):

        result = PerformanceProfiler.profile_function(PriceInitializations.make_price, 5, 1000000)
        # ~332ms (332406μs) minimum of 3 runs @ 1000000 iterations
        self.assertTrue(result < 0.4)

    def test_float_comparisons(self):

        result = PerformanceProfiler.profile_function(PriceInitializations.float_comparisons, 5, 1000000)
        # ~61ms (60721μs) average over 3 runs @ 1000000 iterations
        self.assertTrue(result < 0.1)

    def test_decimal_comparisons(self):

        result = PerformanceProfiler.profile_function(PriceInitializations.decimal_comparisons, 5, 1000000)
        # ~80ms (80051μs) minimum of 3 runs @ 1000000 iterations
        self.assertTrue(result < 0.1)

    def test_builtin_decimal_comparisons(self):

        result = PerformanceProfiler.profile_function(PriceInitializations.builtin_decimal_comparisons, 5, 1000000)
        # ~160ms (162997μs) minimum of 3 runs @ 1000000 iterations
        self.assertTrue(result < 0.2)

    def test_float_arithmetic(self):

        result = PerformanceProfiler.profile_function(PriceInitializations.float_arithmetic, 5, 1000000)
        # ~49ms (61914μs) average over 3 runs @ 1000000 iterations
        self.assertTrue(result < 0.1)

    def test_decimal_arithmetic(self):

        result = PerformanceProfiler.profile_function(PriceInitializations.decimal_arithmetic, 5, 1000000)
        # ~124ms (125350μs) average over 3 runs @ 1000000 iterations
        self.assertTrue(result < 0.15)