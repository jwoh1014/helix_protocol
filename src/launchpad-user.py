from xrpl_account import XrplAccount


class LaunchpadUser:
    """_summary_
    LaunchpadUser Class
    """

    def __init__(self, wallet_path: str):
        self.xrpl_account = XrplAccount(wallet_path)
