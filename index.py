from pyteal import *
from beaker.client import *
from beaker.application import *
from beaker.decorators import *

class MyFirstApp(Application):
    
    app_sum: Final[ApplicationStateValue] = ApplicationStateValue(
        stack_type=TealType.uint64
    )

    account_sum: Final[AccountStateValue] = AccountStateValue(
        stack_type=TealType.uint64
    )

    @create
    def create(self):
        return self.initialize_application_state()

    @opt_in
    def opt_in(self):
        return self.initialize_account_state()

    # save into global app storage
    @external(authorize=Authorize.only(Global.creator_address()))
    def sum(self, first_number: abi.Uint64, second_number: abi.Uint64):
        return self.app_sum.set(first_number.get() + second_number.get())

    # save into local account storage
    @external
    def sumAndSave(self, a: abi.Uint64, b: abi.Uint64):
        return self.account_sum.set(a.get() + b.get())

