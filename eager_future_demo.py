from functools import partial, Placeholder as _

import asyncio

print(asyncio.Future)  # Will show if it's the C or Python version
print(asyncio.Task)

def callback_no_exc(fut, idx):
    print(f"callback_no_throw: {idx}")


def callback_with_exc(fut):
    print("callback_with_exception")
    raise RuntimeError("TEST EXCEPTION")


async def func(fut):
    try:
        print("func: entered")
        await fut
        print("func: done")
    except Exception as exc:
        print(f"func: EXCEPTION: {exc}")


async def main():
    loop = asyncio.get_running_loop()

    # Comment this in order to fallback to original behavior
    loop.set_future_factory(asyncio.eager_future_factory)

    # Demonstrate future that has result
    fut = loop.create_future()
    loop.create_task(func(fut))
    await asyncio.sleep(1)
    print("main: before set_result")
    fut.set_result(None)
    print("main: after set_result")

    # Demonstrate future with exception
    fut = loop.create_future()
    loop.create_task(func(fut))
    await asyncio.sleep(1)
    print("main: before set_exception")
    fut.set_exception(RuntimeError("FUTURE WITH EXCEPTION"))
    print("main: after set_exception")

    # Demonstrate future with done callbacks that may raise
    fut = loop.create_future()
    fut.add_done_callback(partial(callback_no_exc, _, 1))
    fut.add_done_callback(callback_with_exc)
    fut.add_done_callback(partial(callback_no_exc, _, 2))
    print("main: before set_result")
    fut.set_result(None)
    print("main: after set_result")


asyncio.run(main())
