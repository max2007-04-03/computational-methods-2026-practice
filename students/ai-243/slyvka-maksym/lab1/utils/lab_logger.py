import logging
import sys
import os
import io
import inspect


def custom_logger(name: str, overwrite: bool = False) -> logging.Logger:
    """
    Creates and configures a logger that outputs to the console (stdout) and a file.

    :param name: Name of the logger (will also be used as the filename, e.g., 'lab1' -> 'lab1.log').
    :param overwrite: If True, the log file will be overwritten on start. Defaults to False (append mode).
    :return: Configured logging.Logger instance.
    """
    caller_frame = inspect.stack()[1]
    caller_filename = caller_frame.filename
    caller_dir = os.path.dirname(os.path.abspath(caller_filename))

    log_file_path = os.path.join(caller_dir, f"{name}.log")

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    if logger.handlers:
        logger.handlers.clear()

    formatter = logging.Formatter(
        fmt="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # File handler — always UTF-8
    file_mode = "w" if overwrite else "a"
    file_handler = logging.FileHandler(log_file_path, mode=file_mode, encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    # Console handler — UTF-8 safe on Windows
    if hasattr(sys.stdout, 'buffer'):
        console_stream = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace', line_buffering=True)
    else:
        console_stream = sys.stdout
    console_handler = logging.StreamHandler(console_stream)
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger
