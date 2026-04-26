import sys
if not sys.platform.startswith('win'):
    print("Skipping test on non-Windows platform")
    sys.exit(0)
import asyncio
import sys
if sys.platform.startswith('win'):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
async def main():
    proc = await asyncio.create_subprocess_exec("cmd", "/c", "echo", "hello", stdout=asyncio.subprocess.PIPE)
    out, _ = await proc.communicate()
    print(out.decode())
asyncio.run(main())