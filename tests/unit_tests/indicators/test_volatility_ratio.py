# -------------------------------------------------------------------------------------------------
#  Copyright (C) 2015-2021 Nautech Systems Pty Ltd. All rights reserved.
#  https://nautechsystems.io
#
#  Licensed under the GNU Lesser General Public License Version 3.0 (the "License");
#  You may not use this file except in compliance with the License.
#  You may obtain a copy of the License at https://www.gnu.org/licenses/lgpl-3.0.en.html
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
# -------------------------------------------------------------------------------------------------

import sys
import unittest

from nautilus_trader.indicators.volatility_ratio import VolatilityRatio
from tests.test_kit.providers import TestInstrumentProvider
from tests.test_kit.stubs import TestStubs


AUDUSD_SIM = TestInstrumentProvider.default_fx_ccy("AUD/USD")


class VolatilityCompressionRatioTests(unittest.TestCase):
    def setUp(self):
        # Fixture Setup
        self.vcr = VolatilityRatio(10, 100)

    def test_name_returns_expected_string(self):
        # Arrange
        # Act
        # Assert
        self.assertEqual("VolatilityRatio", self.vcr.name)

    def test_str_repr_returns_expected_string(self):
        # Arrange
        # Act
        # Assert
        self.assertEqual("VolatilityRatio(10, 100, SIMPLE, True, 0.0)", str(self.vcr))
        self.assertEqual("VolatilityRatio(10, 100, SIMPLE, True, 0.0)", repr(self.vcr))

    def test_initialized_without_inputs_returns_false(self):
        # Arrange
        # Act
        # Assert
        self.assertEqual(False, self.vcr.initialized)

    def test_initialized_with_required_inputs_returns_true(self):
        # Arrange
        # Act
        for _i in range(100):
            self.vcr.update_raw(1.00000, 1.00000, 1.00000)

        # Assert
        self.assertEqual(True, self.vcr.initialized)

    def test_handle_bar_updates_indicator(self):
        # Arrange
        indicator = VolatilityRatio(10, 100)

        bar = TestStubs.bar_5decimal()

        # Act
        indicator.handle_bar(bar)

        # Assert
        self.assertTrue(indicator.has_inputs)
        self.assertEqual(1.0, indicator.value)

    def test_value_with_no_inputs_returns_none(self):
        # Arrange
        # Act
        # Assert
        self.assertEqual(0, self.vcr.value)

    def test_value_with_epsilon_inputs_returns_expected_value(self):
        # Arrange
        epsilon = sys.float_info.epsilon
        self.vcr.update_raw(epsilon, epsilon, epsilon)

        # Act
        # Assert
        self.assertEqual(0, self.vcr.value)

    def test_value_with_one_ones_input_returns_expected_value(self):
        # Arrange
        self.vcr.update_raw(1.00000, 1.00000, 1.00000)

        # Act
        # Assert
        self.assertEqual(0, self.vcr.value)

    def test_value_with_one_input_returns_expected_value(self):
        # Arrange
        self.vcr.update_raw(1.00020, 1.00000, 1.00010)

        # Act
        # Assert
        self.assertEqual(1.0, self.vcr.value)

    def test_value_with_three_inputs_returns_expected_value(self):
        # Arrange
        self.vcr.update_raw(1.00020, 1.00000, 1.00010)
        self.vcr.update_raw(1.00020, 1.00000, 1.00010)
        self.vcr.update_raw(1.00020, 1.00000, 1.00010)

        # Act
        # Assert
        self.assertEqual(1.0, self.vcr.value)

    def test_value_with_close_on_high_returns_expected_value(self):
        # Arrange
        high = 1.00010
        low = 1.00000
        factor = 0

        # Act
        for _i in range(1000):
            high += 0.00010 + factor
            low += 0.00010 + factor
            factor += 0.00001
            close = high
            self.vcr.update_raw(high, low, close)

        # Assert
        self.assertEqual(0.9552015928322548, self.vcr.value, 2)

    def test_value_with_close_on_low_returns_expected_value(self):
        # Arrange
        high = 1.00010
        low = 1.00000
        factor = 0

        # Act
        for _i in range(1000):
            high -= 0.00010 + factor
            low -= 0.00010 + factor
            factor -= 0.00002
            close = low
            self.vcr.update_raw(high, low, close)

        # Assert
        self.assertEqual(0.9547511312217188, self.vcr.value)

    def test_reset_successfully_returns_indicator_to_fresh_state(self):
        # Arrange
        for _i in range(1000):
            self.vcr.update_raw(1.00010, 1.00000, 1.00005)

        # Act
        self.vcr.reset()

        # Assert
        self.assertFalse(self.vcr.initialized)
        self.assertEqual(0, self.vcr.value)
