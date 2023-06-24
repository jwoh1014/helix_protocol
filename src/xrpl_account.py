import json
from datetime import datetime

# from time import sleep
from pprint import pprint
from xrpl.clients import JsonRpcClient
from xrpl.wallet import generate_faucet_wallet
from xrpl.wallet import Wallet
from xrpl.models.requests import AccountObjects, AccountInfo
from xrpl.models.response import Response
from xrpl.models.transactions import Payment, EscrowCreate, EscrowFinish, EscrowCancel
from xrpl.utils import datetime_to_ripple_time
from xrpl.transaction import autofill_and_sign, send_reliable_submission
from xrpl.account import get_balance

from utils import address

JSON_RPC_URL = "https://s.altnet.rippletest.net:51234"


class XrplAccount:
    """
    XrplAccount Class provides functionalities to interact with the XRP Ledger.
    This includes generating a new wallet, loading an existing wallet from file,
    and sending XRP to a specific address.

    Attributes:
        client: An instance of JsonRpcClient to interact with the XRP Ledger.
        wallet: An instance of Wallet representing the current wallet.
    """

    def __init__(self, client: JsonRpcClient, wallet_path: str = "") -> None:
        """
        Constructs all the necessary attributes for the XRPL object.

        Args:
            wallet_path (str): The path to the file that stores the wallet information.
        """
        self._client = client
        self._wallet: Wallet = None  # type: ignore
        if wallet_path != "":
            self.load_wallet(wallet_path)

    def generate_wallet(self, wallet_path: str) -> Wallet:
        """
        Generates a new wallet and saves the wallet information to a file.

        Args:
            wallet_path (str, optional): The path to the file to store the wallet information.
        """
        self._wallet = generate_faucet_wallet(self._client, debug=True)

        with open(wallet_path, "w", encoding="UTF-8") as file:
            json.dump(self._wallet.__dict__, file)

        return self._wallet

    def load_wallet(self, wallet_path: str) -> Wallet:
        """
        Loads the wallet information from a file and constructs a new Wallet instance.

        Args:
            wallet_path (str): The path to the file that stores the wallet information.
        """
        with open(wallet_path, "r", encoding="UTF-8") as file:
            wallet_info = json.load(file)

        self._wallet = Wallet(
            seed=wallet_info["seed"],
            sequence=wallet_info["sequence"],
            algorithm=wallet_info["algorithm"],
        )

        return self._wallet

    def get_wallet(self) -> Wallet:
        """
        Returns:
            Wallet: The current wallet.
        """
        return self._wallet

    def get_classic_address(self) -> address:
        """
        Returns:
            address: classic address of the wallet
        """
        return address(self._wallet.classic_address)

    def fetch_balance(self) -> int:
        """
        Retrieves the balance of the current wallet.

        Returns:
            int: The balance of the current wallet in XRP.
        """
        if self._wallet is None:
            raise Exception("Wallet is not loaded or generated.")

        return get_balance(self._wallet.classic_address, self._client)

    def get_account_objects(self) -> list[dict]:
        """_summary_

        Returns:
            list[dict]: _description_
        """
        account_objects_request = AccountObjects(account=self.get_classic_address())
        account_objects = (self._client.request(account_objects_request)).result["account_objects"]
        return account_objects

    def get_account_info(self) -> dict:
        """_summary_

        Returns:
            dict: _description_
        """
        account_info_request = AccountInfo(account=self.get_classic_address())
        account_info = (self._client.request(account_info_request)).result
        return account_info

    def get_escrow_objects(self) -> list[dict]:
        """_summary_

        Returns:
            list[dict]: _description_
        """
        escrow_objects_request = AccountObjects(account=self.get_classic_address())
        escrow_objects = (self._client.request(escrow_objects_request)).result["account_objects"]
        return escrow_objects

    def send_xrp(self, destination_address: address, amount: str | int) -> Response:
        """
        Sends XRP to a specific address.

        Args:
            destination_address (address): The address to send XRP to.
            amount (str): The amount of XRP to send.

        Returns:
            Response: The response from the XRP Ledger.

        """
        payment_tx = Payment(
            account=self.get_classic_address(),
            amount=str(amount),
            destination=destination_address,
        )

        signed_payment_tx = autofill_and_sign(payment_tx, self._wallet, self._client)

        response = send_reliable_submission(signed_payment_tx, self._client)

        return response

    def create_escrow(
        self,
        destination_address: address,
        amount: str | int,
        finish_after: datetime,
        cancel_after: datetime = None,  # type: ignore
    ) -> Response:
        """
        Creates an escrow payment to a specific address.

        Args:
            destination_address (address): The address to send the escrow payment to.
            amount (str | int): The amount of XRP to send.
            finish_after (datetime): The time after which the escrow can be finished.
            cancel_after (datetime, optional): The time after which the escrow can be cancelled. Defaults to None.

        Returns:
            Response: The response from the XRP Ledger.
        """
        finish_after = datetime_to_ripple_time(finish_after)  # type: ignore
        if cancel_after is not None:
            cancel_after = datetime_to_ripple_time(cancel_after)  # type: ignore

        create_tx = EscrowCreate(
            account=self.get_classic_address(),
            destination=destination_address,
            amount=str(amount),
            finish_after=finish_after,  # type: ignore
            cancel_after=cancel_after,  # type: ignore
        )

        signed_create_tx = autofill_and_sign(create_tx, self._wallet, self._client)
        create_escrow_response = send_reliable_submission(signed_create_tx, self._client)

        # account_objects_request = AccountObjects(account=self.wallet.classic_address)
        # account_objects = (self.client.request(account_objects_request)).result["account_objects"]

        # print("Escrow object exists in current account:")
        # print(account_objects)

        return create_escrow_response

    def finish_escrow(self, offer_sequence: int) -> Response:
        """
        Finishes an escrow transaction.

        Args:
            offer_sequence (int): The sequence number of the offer.

        Returns:
            Response: The response from the XRP Ledger.
        """
        finish_tx = EscrowFinish(
            account=self.get_classic_address(),
            owner=self.get_classic_address(),
            offer_sequence=offer_sequence,
        )

        signed_finish_tx = autofill_and_sign(finish_tx, self._wallet, self._client)
        finish_escrow_response = send_reliable_submission(signed_finish_tx, self._client)

        return finish_escrow_response

    def cancel_escrow(self, offer_sequence: int) -> Response:
        """
        Cancels an escrow transaction.

        Args:
            offer_sequence (int): The sequence number of the offer.

        Returns:
            Response: The response from the XRP Ledger.
        """
        cancel_tx = EscrowCancel(
            account=self.get_classic_address(),
            owner=self.get_classic_address(),
            offer_sequence=offer_sequence,
        )

        signed_cancel_tx = autofill_and_sign(cancel_tx, self._wallet, self._client)
        cancel_escrow_response = send_reliable_submission(signed_cancel_tx, self._client)

        return cancel_escrow_response

    def __str__(self) -> str:
        """
        Returns a string representation of the XRPL object.

        Returns:
            str: A string representing the XRPL object.
        """
        return f"XRPL\nclient_url={self._client.url}\nwallet=\n{self._wallet}"

    def __dict__(self) -> dict:
        """
        Returns a dictionary representation of the XRPL object.

        Returns:
            dict: A dictionary representing the XRPL object.
        """
        return {
            "client": self._client,
            "wallet": self._wallet,
        }


if __name__ == "__main__":
    xrpl_client = JsonRpcClient(JSON_RPC_URL)
    test_account = XrplAccount(client=xrpl_client, wallet_path="database/wallet.json")
    dest_account = XrplAccount(client=xrpl_client, wallet_path="database/destination.json")
    # dest_address = dest_account.get_wallet().classic_address
    # print(test_account)
    # print(dest_account)
    # print(test_account.fetch_balance())
    # res = test_account.send_xrp(dest_address, "100000")
    # print(type(res))
    # account_objs_req = AccountObjects(account=test_account.wallet.classic_address)
    # account_objs = (test_account.client.request(account_objs_req)).result["account_objects"]
    # pprint(account_objs)
    # print(test_account.fetch_balance())
    # print(dest_account.fetch_balance())

    # res = test_account.escrow_payment(
    #     dest_account.get_wallet().classic_address, "100000", datetime.now() + timedelta(seconds=30)
    # )
    # pprint(res)

    # pprint(test_account.finish_escrow(res.result["Sequence"]))
    # print(test_account.fetch_balance())
    # print(dest_account.fetch_balance())
    pprint(test_account.get_account_info())


# TODO: Add functionality to check if the wallet is ready for the transaction
# TODO: Add delegation for the transaction
# TODO: Add functionality to check if the transaction is successful
# TODO: Connect DB to store the wallet information
# TODO: Dockerize the application
