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

from nautilus_trader.model.events cimport AccountState
from nautilus_trader.model.orders.base cimport Order
from nautilus_trader.model.position cimport Position
from nautilus_trader.trading.account cimport Account


cdef class ReportProvider:
    cpdef object generate_orders_report(self, list orders)
    cpdef object generate_order_fills_report(self, list orders)
    cpdef object generate_positions_report(self, list positions)
    cpdef object generate_account_report(self, Account account)

    cdef dict _order_to_dict(self, Order order)
    cdef dict _position_to_dict(self, Position position)
    cdef dict _account_state_to_dict(self, AccountState event)
