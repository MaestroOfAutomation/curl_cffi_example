import asyncio
import requests
from curl_cffi import requests as cffi_requests

from constants import URL, HEADERS


def print_result(name, response):
    print(f"{name} Status Code:", response.status_code)
    print(f"{name} Response Text:", response.text[:128] + "..." if len(response.text) > 128 else response.text)

def requests_example():
    response = requests.get(URL, headers=HEADERS)
    print_result("Requests", response)

def curl_cffi_example(impersonate: str | None):
    response = cffi_requests.get(URL, headers=HEADERS, impersonate=impersonate)
    print_result("cURL CFFI", response)

async def main():
    print("--- Requests Example ---")
    requests_example()
    print("\n--- cURL CFFI [W/O impersonate] Example ---")
    curl_cffi_example(impersonate=None)
    print("\n--- cURL CFFI [with impersonate] Example ---")
    curl_cffi_example(impersonate='chrome')

if __name__ == "__main__":
    asyncio.run(main())