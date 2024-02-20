import logging
from pathlib import Path

from safeeyes import utility

context = None
PRESENCE_FILE_PATH = (
    Path(utility.HOME_DIRECTORY) / ".local" / "share" / "safeeyes" / "teamspresence"
)


def init(ctx, safeeyes_config, plugin_config) -> None:
    global context
    context = ctx
    context["plugin_config"] = plugin_config


def on_pre_break(break_obj) -> bool:
    """Lifecycle method executes before the pre-break period."""
    return _should_skip_break()


def on_start_break(break_obj) -> bool:
    """Lifecycle method executes just before the break."""
    return _should_skip_break()


def _should_skip_break() -> bool:
    presence = PRESENCE_FILE_PATH.read_text()
    setting = f"presence_{presence.replace('-', '_')}"
    if setting not in context["plugin_config"]:
        logging.warning(f"{presence} is not a valid presence status.")
        return False
    if context["plugin_config"][setting]:
        logging.info(f"Teams presence status is {presence}. Skipping break.")
        return True
    logging.info(f"Teams presence status is {presence}. Break allowed.")
    return False
