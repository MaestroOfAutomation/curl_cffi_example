import asyncio
from time import monotonic

from curl_cffi.requests import AsyncSession


async def do_request(session: AsyncSession) -> None:
    started = monotonic()
    r = await session.get("https://api.ipify.org?format=json")
    elapsed = monotonic() - started
    print(f'Request took {elapsed:.2f} seconds: {r.json()}')


async def main():
    requests_count: int = 20

    started = monotonic()
    async with AsyncSession(impersonate="firefox") as session:
        await asyncio.gather(
            *[
                do_request(session=session)
                for _ in range(requests_count)
            ]
        )

    print(f'Made {requests_count} requests in {monotonic() - started:.2f} seconds')


if __name__ == "__main__":
    asyncio.run(main())