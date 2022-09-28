import pytest

from helpers.test_logs import describe

from algosdk.v2client.algod import AlgodClient
from beaker import client, sandbox

from index import MyFirstApp

accts = sandbox.get_accounts()
algod_client: AlgodClient = sandbox.get_algod_client()

@pytest.fixture(scope='session')
def creator_acc():
    return accts[0].address, accts[0].private_key, accts[0].signer

@pytest.fixture(scope='session')
def creator_app_client(creator_acc):
    _,_,signer = creator_acc
    app_client = client.ApplicationClient(algod_client, MyFirstApp(), signer=signer)
    return app_client

def test_empty_state(creator_app_client: client.ApplicationClient):
    describe("Should have empty global state after creating the application")
    creator_app_client.create()
    app_state = creator_app_client.get_application_state()
    assert(
        app_state["app_sum"] == 0
    )