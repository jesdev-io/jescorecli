from jescorecli import config
from jescorecli.common import CLI_PREFIX_CLIENT, CLI_PREFIX_MCU
from jescorecli.jescorecli import CjescoreCli


class FakeSerial:
    def __init__(self, *args, **kwargs):
        self.lines = iter([b"[job]: value\n", CLI_PREFIX_MCU.encode() + b"\n"])
        self.written = []

    def flush(self):
        pass

    def setRTS(self, value):  # noqa: N802
        self.rts = value

    def write(self, data):
        self.written.append(data)

    def readline(self):
        return next(self.lines, b"")


class SerialFactory:
    def __init__(self):
        self.instances = []

    def __call__(self, *args, **kwargs):
        serial = FakeSerial(*args, **kwargs)
        self.instances.append(serial)
        return serial


def test_command_returns_lines_without_printing(monkeypatch, capsys):
    factory = SerialFactory()
    monkeypatch.setattr("jescorecli.jescorecli.serial.Serial", factory)

    cli = CjescoreCli(port="/dev/test")
    assert cli.command("job arg") == ["[job]: value"]
    assert factory.instances[0].written == [b"job arg"]
    assert capsys.readouterr().out == ""


def test_terminal_session_preserves_cli_printing(monkeypatch, capsys):
    factory = SerialFactory()
    monkeypatch.setattr("jescorecli.jescorecli.serial.Serial", factory)
    config.config_cli_usage = True
    config.config_verbose = False

    cli = CjescoreCli(port="/dev/test", terminal=True)
    assert cli.uarttransceive("job arg") == ["[job]: value", CLI_PREFIX_MCU]
    assert capsys.readouterr().out == f"{CLI_PREFIX_CLIENT}\n[job]: value\n"
