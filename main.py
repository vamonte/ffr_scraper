import asyncio
from ffr import send_request_to_ffr
from parser import exract_comittees_name_and_id

ffr_data = {}


async def get_committees_name_and_id(loop):
    html, _ = await send_request_to_ffr(loop)
    committees = exract_comittees_name_and_id(html)
    for _id, name in committees:
        ffr_data[_id] = {'name': name, 'clubs': {}}


if __name__ == "__main__":
    loop = asyncio.get_event_loop()

    print("Retrieve the name and id of the committees.")
    loop.run_until_complete(asyncio.wait({get_committees_name_and_id(loop)}))
