import pytest
from algosdk.v2client.algod import AlgodClient
from beaker import sandbox, client
from helpers.test_logs import describe
from index import MyFirstApp

accts = sandbox.get_accounts()
algod_client: AlgodClient = sandbox.get_algod_client()

@pytest.fixture(scope='session')
def creator_acct():
    return accts[0].address, accts[0].private_key, accts[0].signer 

@pytest.fixture(scope='session')
def creator_app_client(creator_acct) -> client.ApplicationClient:
    _, _, signer = creator_acct
    app_client = client.ApplicationClient(algod_client, MyFirstApp(), signer=signer)
    return app_client

def test_local_state_without_opt_in(creator_app_client):
    describe("Should fail because current account does not opt in the application")
    creator_app_client.create()
    try:
        creator_app_client.call(MyFirstApp.sumAndSave, a=1, b=2)
    except client.LogicException as e:
        assert("has not opted i" in e.msg)

def test_local_state(creator_app_client: client.ApplicationClient):
    describe("Should append sum into account local storage")
    creator_app_client.create()
    creator_app_client.opt_in()
    creator_app_client.call(MyFirstApp.sumAndSave, a=1, b=2)
    curr_acc_state = creator_app_client.get_account_state()
    assert(
        curr_acc_state["account_sum"] == 3
    )

    
