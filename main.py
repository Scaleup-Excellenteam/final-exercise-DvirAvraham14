import os.path
import sys
import asyncio
from controller import Controller


app = Controller(*sys.argv[1:])
asyncio.run(app.run())
