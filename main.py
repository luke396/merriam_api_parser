"""Main, please set environment variable 'MERRIAM_WEBSTER_DICTIONARY_KEY' first."""

import asyncio

from merriam_api_parser.utility import main

if __name__ == "__main__":
    asyncio.run(main())
