import asyncio
import tqdm
from ffr import (send_request_to_ffr, extract_set_cookie, )
from parser import (extract_comittees_name_and_id, extract_committee_detail, )

ffr_data = {}


async def get_committee_detail(loop, committee_id):
    html, headers = await send_request_to_ffr(loop,
                                              {'code_pratiquer': committee_id})
    details, clubs = extract_committee_detail(html, committee_id,
                                              extract_set_cookie(headers))
    ffr_data[committee_id] = {**ffr_data[committee_id], **details}
    return clubs


async def get_committees_name_and_id(loop):
    html, _ = await send_request_to_ffr(loop)
    committees = extract_comittees_name_and_id(html)
    for _id, name in committees:
        ffr_data[_id] = {'name': name, 'clubs': {}}


async def wait_with_progress(coros):
    for f in tqdm.tqdm(asyncio.as_completed(coros), total=len(coros)):
        await f


if __name__ == "__main__":
    loop = asyncio.get_event_loop()

    print("Retrieve the name and id of the committees.")
    loop.run_until_complete(asyncio.wait({get_committees_name_and_id(loop)}))

    print("Retrieve the details of the committees.")
    detail_coros = {get_committee_detail(loop, id) for id in ffr_data.keys()}
    loop.run_until_complete(wait_with_progress(detail_coros))
