"""
Show how console logging looks like.

Output used in screenshot in the readme in the Structlog GitHub repo and
<https://www.structlog.org/en/stable/development.html>.
"""

from dataclasses import dataclass
from wsgiref.validate import validator

import structlog
import logging

# Configure logging
structlog.configure(
    processors=[
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.dev.ConsoleRenderer()
    ],
    wrapper_class=structlog.make_filtering_bound_logger(logging.NOTSET),
    context_class=dict,
    logger_factory=structlog.PrintLoggerFactory(),
    cache_logger_on_first_use=True,
)

@dataclass
class SomeClass:
    x: int
    y: str


structlog.stdlib.recreate_defaults()  # so we have logger names

log = structlog.get_logger("some_logger")

log.debug("debugging is hard", a_list=[1, 2, 3])
log.info("informative!", some_key="some_value")
log.warning("uh-uh!")
log.error("omg", a_dict={"a": 42, "b": "foo"})
log.critical("wtf", what=SomeClass(x=1, y="z"))


log2 = structlog.get_logger("another_logger")


def make_call_stack_more_impressive():
    try:
        d = {"x": 42}
        print(SomeClass(d["y"], "foo"))
    except Exception:
        log2.exception("poor me")
    log.info("all better now!", stack_info=True)
    return 42

def test_show_off():
    value = make_call_stack_more_impressive()
    assert value == 42

make_call_stack_more_impressive()