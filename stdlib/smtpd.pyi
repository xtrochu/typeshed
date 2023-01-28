import asynchat
import asyncore
import socket
import sys
from collections import defaultdict
from typing import Any
from typing_extensions import TypeAlias

if sys.version_info >= (3, 11):
    __all__ = ["SMTPChannel", "SMTPServer", "DebuggingServer", "PureProxy"]
else:
    __all__ = ["SMTPChannel", "SMTPServer", "DebuggingServer", "PureProxy", "MailmanProxy"]

_Address: TypeAlias = tuple[str, int]  # (host, port)

class SMTPChannel(asynchat.async_chat):
    COMMAND: int
    DATA: int

    command_size_limits: defaultdict[str, int]
    smtp_server: SMTPServer
    conn: socket.socket
    addr: Any
    received_lines: list[str]
    smtp_state: int
    seen_greeting: str
    mailfrom: str
    rcpttos: list[str]
    received_data: str
    fqdn: str
    peer: str

    command_size_limit: int
    data_size_limit: int

    enable_SMTPUTF8: bool
    @property
    def max_command_size_limit(self) -> int: ...
    def __init__(
        self,
        server: SMTPServer,
        conn: socket.socket,
        addr: Any,
        data_size_limit: int = ...,
        map: asyncore._MapType | None = None,
        enable_SMTPUTF8: bool = False,
        decode_data: bool = False,
    ) -> None: ...
    # base asynchat.async_chat.push() accepts bytes
    def push(self, msg: str) -> None: ...  # type: ignore[override]
    def collect_incoming_data(self, data: bytes) -> None: ...
    def found_terminator(self) -> None: ...
    def smtp_HELO(self, arg: str) -> None: ...
    def smtp_NOOP(self, arg: str) -> None: ...
    def smtp_QUIT(self, arg: str) -> None: ...
    def smtp_MAIL(self, arg: str) -> None: ...
    def smtp_RCPT(self, arg: str) -> None: ...
    def smtp_RSET(self, arg: str) -> None: ...
    def smtp_DATA(self, arg: str) -> None: ...
    def smtp_EHLO(self, arg: str) -> None: ...
    def smtp_HELP(self, arg: str) -> None: ...
    def smtp_VRFY(self, arg: str) -> None: ...
    def smtp_EXPN(self, arg: str) -> None: ...

class SMTPServer(asyncore.dispatcher):
    channel_class: type[SMTPChannel]

    data_size_limit: int
    enable_SMTPUTF8: bool
    def __init__(
        self,
        localaddr: _Address,
        remoteaddr: _Address,
        data_size_limit: int = ...,
        map: asyncore._MapType | None = None,
        enable_SMTPUTF8: bool = False,
        decode_data: bool = False,
    ) -> None: ...
    def handle_accepted(self, conn: socket.socket, addr: Any) -> None: ...
    def process_message(
        self, peer: _Address, mailfrom: str, rcpttos: list[str], data: bytes | str, **kwargs: Any
    ) -> str | None: ...

class DebuggingServer(SMTPServer): ...

class PureProxy(SMTPServer):
    def process_message(self, peer: _Address, mailfrom: str, rcpttos: list[str], data: bytes | str) -> str | None: ...  # type: ignore[override]

if sys.version_info < (3, 11):
    class MailmanProxy(PureProxy):
        def process_message(self, peer: _Address, mailfrom: str, rcpttos: list[str], data: bytes | str) -> str | None: ...  # type: ignore[override]
