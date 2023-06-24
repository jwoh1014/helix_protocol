from datetime import datetime
from typing import Dict

from xrpl.wallet import Wallet

from utils import address, UserStatus, FundStatus


class IcoProject:
    """
    IcoProject class
    """

    def __init__(
        self,
        project_name: str,
        symbol_name: str,
        start_date: datetime,
        end_date: datetime,
        goal_amount: int,
        wallet: Wallet,
    ):
        self.project_name = project_name
        self.symbol_name = symbol_name
        self.start_date = start_date
        self.end_date = end_date
        self.goal_amount = goal_amount
        self.current_amount = 0
        self.token_amount = 0
        self.backers: Dict[address, UserStatus] = {}
        self._wallet = wallet

    def add_funding(self, backer: address, amount: int):
        """

        Args:
            backer (address): address of the backer
            amount (int): amount of XRP to fund
        """
        if amount <= 0:
            return
        self.current_amount += amount
        if backer in self.backers:
            self.backers[backer].funded_amount += amount
        else:
            self.backers[backer] = UserStatus(
                status=FundStatus.FUNDED, funded_amount=amount, claimed_amount=0, refunded_amount=0
            )

    def global_freeze_token(self):
        return

    def refund_tocken(self, backer_address: address, amount: int):
        """

        Args:
            backer_address (address): address of the backer
            amount (int): amount of XRP to be refunded as tokens
        """
        if amount <= 0:
            return
        self.current_amount -= amount
        if backer_address in self.backers:
            self.backers[backer_address].refunded_amount += amount
        else:
            self.backers[backer_address].status = FundStatus.REFUNDED
            self.backers[backer_address].funded_amount -= amount
            self.backers[backer_address].claimed_amount -= amount
            self.backers[backer_address].refunded_amount += amount

        # TODO: send tokens to backer via trustline

    def is_goal_reached(self) -> bool:
        """

        Returns:
            bool: _description_
        """
        return self.current_amount >= self.goal_amount

    def get_remaining_days(self) -> int:
        """_summary_

        Returns:
            int: _description_
        """
        remaining_days = (self.end_date - datetime.now()).days
        return max(0, remaining_days)

    def get_project_status(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        status = f"Project Name: {self.project_name}\n"
        status += f"Goal Amount: {self.goal_amount}\n"
        status += f"Current Amount: {self.current_amount}\n"
        status += f"Number of Backers: {len(self.backers)}\n"
        status += f"Goal Reached: {'Yes' if self.is_goal_reached() else 'No'}\n"
        status += f"Remaining Days: {self.get_remaining_days()}\n"
        return status

    def get_classic_address(self) -> str:
        """
        Returns:
            str: classic address of the wallet
        """
        return self._wallet.classic_address
