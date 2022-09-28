import json
from index import *

if __name__ == "__main__":
    app = MyFirstApp()
    print(app.approval_program)
    print(app.clear_program)
    print(json.dumps(app.contract.dictify()))
    # TODO: Create json file for abi