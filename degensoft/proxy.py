import asyncio
import re
from typing import Union
from degensoft.utils import force_sync
import aiohttp


def parse_proxy_string(input_str: str) -> Union[dict, None]:
    input_str = input_str.strip('http://').strip('https://').strip('/')
    pattern = re.compile(r"(?P<login>.*):(?P<password>.*?)@(?P<ip>.*):(?P<port>\d*)")
    match = pattern.match(input_str)
    if match:
        return match.groupdict()
    else:
        return None


def get_proxy_dict(proxy_data):
    """
    :param proxy_data: proxy dict
    :return: proxy dict to config requests and other http libs
    """
    if not proxy_data:
        return None
    proxy = f'{proxy_data["ip"]}:{proxy_data["port"]}'
    if "login" in proxy_data and "password" in proxy_data:
        proxy_auth = f'{proxy_data["login"]}:{proxy_data["password"]}@'
    else:
        proxy_auth = ''
    return {
        'http': f'http://{proxy_auth}{proxy}',
        'https': f'http://{proxy_auth}{proxy}'
    }


class MobileProxy:
    def __init__(self, proxy: str, ip_change_url: str = None, timeout: int = 10, stop_condition: asyncio.Event = None):
        self.proxy_line = proxy.strip('http://').strip('https://')
        self._proxy_data = parse_proxy_string(self.proxy_line)
        self.stop_condition = stop_condition if stop_condition else asyncio.Event()
        self.ip_change_url = ip_change_url
        self.timeout = aiohttp.ClientTimeout(total=timeout)

    @property
    def proxy_dict(self):
        return get_proxy_dict(parse_proxy_string(self.proxy_line))

    @property
    def proxy_url(self):
        return f'http://{self.proxy_line}'

    @property
    def login(self):
        return self._proxy_data['login']

    @property
    def password(self):
        return self._proxy_data['password']

    @property
    def host(self):
        return self._proxy_data['ip']

    @property
    def port(self):
        return self._proxy_data['port']

    async def get_ip(self) -> str:
        try:
            async with aiohttp.ClientSession(timeout=self.timeout) as session:
                async with session.get('https://ip.oxylabs.io/', proxy=f'http://{self.proxy_line}') as resp:
                    return (await resp.text()).strip()
        except Exception as exp:
            raise exp
            # return None

    def get_ip_sync(self) -> str:
        return force_sync(self.get_ip)()

    async def change_ip(self) -> Union[str, None]:
        if not self.ip_change_url:
            return
        start_ip = await self.get_ip()
        async with aiohttp.ClientSession() as session:
            while not self.stop_condition.is_set():
                async with session.get(self.ip_change_url) as resp:
                    resp_text = await resp.text()
                    # print(resp_text.strip())
                    new_ip = await self.get_ip()
                    if new_ip != start_ip:
                        return new_ip
                    await asyncio.sleep(15)

    def change_ip_sync(self) -> str:
        return force_sync(self.change_ip)()
