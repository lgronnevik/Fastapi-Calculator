import sys
import pytest
if not sys.platform.startswith('win'):
    pytest.skip("Skipping test on non-Windows platform", allow_module_level=True)
import asyncio
import sys
if sys.platform.startswith('win'):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
async def main():
    proc = await asyncio.create_subprocess_exec("cmd", "/c", "echo", "hello", stdout=asyncio.subprocess.PIPE)
    out, _ = await proc.communicate()
    print(out.decode())
asyncio.run(main())