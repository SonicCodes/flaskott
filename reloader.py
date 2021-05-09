import asyncio
import threading
import ctypes
import time

from watchgod import awatch
from flask import Flask
import traceback


def terminate_thread(thread: threading.Thread):
    if not thread.is_alive():
        return
    exc = ctypes.py_object(SystemExit)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(
        ctypes.c_long(thread.ident), exc)
    if res == 0:
        raise ValueError("nonexistent thread id")
    elif res > 1:
        ctypes.pythonapi.PyThreadState_SetAsyncExc(thread.ident, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")


def run_on_thread(executor) -> threading.Thread:
    thread = threading.Thread(target=executor)
    thread.daemon = True
    thread.start()
    return thread


def time_ms():
    return time.perf_counter_ns() // 1000000


def time_diff(start: int):
    return f"{int(time_ms() - start)}ms"


def init(app, file, host='0.0.0.0', port=5000):
    was_error = [False]
    server_thread = threading.Thread(target=lambda: app.run(host=host, port=port, debug=False))
    server_thread.daemon = True
    server_thread.start()

    def executor():
        start = time_ms()

        def tell_end():
            if was_error[0]:
                print(f"🎉 The last error was recovered in {time_diff(start)}.")
            else:
                print(f"⚡ Reloaded your server in {time_diff(start)}.")
            was_error[0] = False

        try:
            exec(open(file, mode="r").read(), {
                "flask_instance": app,
                "tell_end": tell_end
            })
        except Exception as ex:
            traceback.print_exc()
            was_error[0] = True
            print(f"💀 Something went wrong in {time_diff(start)}.")

    current_task: list[threading.Thread] = [
        run_on_thread(executor)]

    async def main():
        async for _ in awatch(file):
            terminate_thread(current_task[0])
            current_task[0] = run_on_thread(executor)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())


def pre_setup(local) -> Flask:
    local.get('flask_instance').view_functions.clear()
    return local.get('flask_instance')


def post_setup(local):
    local.get("tell_end")()
    while True:
        pass
