from typing import Dict
from datetime import datetime

from xrpl.clients import JsonRpcClient
from xrpl.wallet import Wallet

from xrpl_account import XrplAccount
from ico_project import IcoProject
from launchpad_user import LaunchpadUser
from utils import address


class Admin(XrplAccount):
    def __init__(self, client: JsonRpcClient, wallet_path: str):
        super().__init__(client, wallet_path)

        self.ico_projects: Dict[str, IcoProject] = {}
        self.users: Dict[address, LaunchpadUser] = {}

    def create_ico_project(
        self, project_name: str, start_date: datetime, end_date: datetime, goal_amount: int
    ):
        """_summary_

        Args:
            project_name (str): _description_
            start_date (str): _description_
            end_date (str): _description_
            goal_amount (int): _description_
        """
        wallet = Wallet.create()
        ico_project = IcoProject(project_name, start_date, end_date, goal_amount, wallet)
        self.ico_projects[project_name] = ico_project

    def close_ico_project(self, project_name: str):
        """_summary_

        Args:
            project_name (str): _description_
        """
        ico_project = self.ico_projects[project_name]
        if ico_project.end_date > datetime.now():
            return
        if ico_project.is_goal_reached():
            ico_project._wallet.send_xrp(ico_project.current_amount, self.get_classic_address())
