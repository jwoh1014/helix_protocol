from typing import Dict

from xrpl.clients import JsonRpcClient
from xrpl_account import XrplAccount

from ico_project import IcoProject
from utils import UserStatus, FundStatus


class LaunchpadUser(XrplAccount):
    """_summary_
    LaunchpadUser Class
    """

    def __init__(self, client: JsonRpcClient, wallet_path: str):
        """

        Args:
            client (JsonRpcClient): xrpl client
            wallet_path (str): wallet json path
        """
        super().__init__(client=client, wallet_path=wallet_path)
        self.portfolio: Dict[str, IcoProject] = {}

    def fund_ico(self, ico_project: IcoProject, amount: int):
        """_summary_

        Args:
            ico_project(IcoProject): ico project to fund
            amount (int): amount of XRP to fund
        """
        if amount <= 0:
            return
        self.create_escrow(ico_project.get_classic_address(), amount, ico_project.end_date)
        self.portfolio[ico_project.project_name] = ico_project

        # TODO: check if balance is enough
        # TODO: delegation

    def claim_refund(self, ico_project: IcoProject):
        """_summary_

        Args:
            ico_project_ (str): _description_
        """
        if ico_project.is_goal_reached():
            self.portfolio[ico_project.project_name].backers[
                self.get_classic_address()
            ].status = FundStatus.CLAIMED
            return
