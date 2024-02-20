import logging
from pathlib import Path

from safeeyes import utility

context = None


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
    safeeyes_presence_file = Path(utility.CONFIG_DIRECTORY) / "teamspresence"
    presence = safeeyes_presence_file.read_text()
    setting = f"presence_{presence.replace('-', '_')}"
    if context["plugin_settings"].get(setting, False):
        logging.info(f"Teams presence status is {presence}. Skipping break.")
        return True
    return False
