import pytest

from helpers.test_logs import describe 

from algosdk.atomic_transaction_composer import (
    AccountTransactionSigner,
)
from algosdk.v2client.algod import AlgodClient
from beaker import client, sandbox, consts

from index import *

accts = sandbox.get_accounts()
algod_client: AlgodClient = sandbox.get_algod_client()


@pytest.fixture(scope="session")
def creator_acct() -> tuple[str, str, AccountTransactionSigner]:
    return accts[0].address, accts[0].private_key, accts[0].signer

@pytest.fixture(scope="session")
def second_acct() -> tuple[str, str, AccountTransactionSigner]:
    return accts[1].address, accts[1].private_key, accts[1].signer

@pytest.fixture(scope="session")
def creator_app_client(creator_acct) -> client.ApplicationClient:
    _, _, signer = creator_acct
    app_client = client.ApplicationClient(algod_client, MyFirstApp(), signer=signer)
    return app_client


def test_global_sum(creator_app_client: client.ApplicationClient):
    describe("Should add global state sum. Sender is the creator of the smart contract")
    creator_app_client.create()
    creator_app_client.fund(1 * consts.algo)
    first_number = 1
    second_number = 2
    creator_app_client.call(MyFirstApp.sum, first_number=first_number, second_number=second_number)
    app_state = creator_app_client.get_application_state()
    assert (
        app_state.get("app_sum") == first_number + second_number
    )

def test_global_sum_with_other_account(creator_app_client: client.ApplicationClient, second_acct):
    describe("Should fail when trying to update the global state doing the sum with an account dif from creator")
    _, _, signer = second_acct
    creator_app_client.create()
    second_acc_client = creator_app_client.prepare(signer=signer)
    
    first_number = 1
    second_number = 2

    # this should fail
    try:
        second_acc_client.call(MyFirstApp.sum, first_number=first_number, second_number=second_number)
    except LogicException as e:
        assert(
            "assert failed" in e.msg
        )