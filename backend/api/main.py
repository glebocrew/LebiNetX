from uvicorn import run
from sys import argv, exit
from logger import Logger as Logger
from consts import START_LOG_PATH, DEFAULT_HOST, DEFAULT_PORT, RELOAD, FASTAPI_PATH

logger = Logger(path=START_LOG_PATH)

print(argv)

logger.log(
    "i",
    f"Starting uvicorn with args: {' '.join(argv[1:])}"
    if len(argv) > 1
    else "Starting uvicorn with default args",
)

host_flag_value = DEFAULT_HOST
port_flag_value = DEFAULT_PORT
reload_value = RELOAD

if len(argv) < 1:
    run()
if "-host" in argv:
    host_flag_index = argv.index("-host")
    try:
        host_flag_value = argv[host_flag_index + 1]
    except Exception as e:
        logger.log("f", "Host argument must have value, not only flag.")
        logger.log("f", f"Full error: {e}")
        logger.log("f", "Stopping server...")
        exit(-1)
if "-port" in argv:
    port_flag_index = argv.index("-port")
    try:
        port_flag_value = int(argv[port_flag_index + 1])
    except Exception as e:
        logger.log("f", "Port argument must be an integer value, not only flag.")
        logger.log("f", f"Full error: {e}")
        logger.log("f", "Stopping server...")
        exit(-1)
if "-debug" in argv:
    reload_value = True


if __name__ == "__main__":
    run(
        app=f"{FASTAPI_PATH}:app",
        host=host_flag_value,
        port=port_flag_value,
        reload=reload_value,
    )
