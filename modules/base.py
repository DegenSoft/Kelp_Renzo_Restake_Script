class BaseModule:
    def __init__(self, web3, config):
        self.web3 = web3
        self.config = config

    async def run(self, private_key):
        raise NotImplementedError()
