from typing import NewType
from enum import Enum
from dataclasses import dataclass


address = NewType("address", str)


class FundStatus(Enum):
    DEFAULT = 0
    FUNDED = 1
    CLAIMED = 2
    REFUNDED = 3


@dataclass
class UserStatus:
    status: FundStatus = FundStatus.DEFAULT
    funded_amount: int = 0
    claimed_amount: int = 0
    refunded_amount: int = 0
