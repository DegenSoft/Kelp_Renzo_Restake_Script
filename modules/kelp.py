# -*- coding: utf-8 -*-
from loguru import logger
from modules.base import BaseModule


class Kelp(BaseModule):
    async def run(self, private_key):
        logger.debug(self.config)
