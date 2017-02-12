import aiohttp

FFR_URL = 'https://annuaire.ffr.fr/index.php/annuaire'


def build_request_kwargs(data=None, headers=None):
    request_kwargs = {}
    if data:
        request_kwargs['data'] = data
    if headers:
        request_kwargs['headers'] = headers
    return request_kwargs


async def send_request_to_ffr(loop, data=None, headers=None):
    async with aiohttp.ClientSession(loop=loop) as session:
        req_kwargs = build_request_kwargs(data, headers)
        async with session.post(FFR_URL, **req_kwargs) as response:
            return await response.text(), response.headers
