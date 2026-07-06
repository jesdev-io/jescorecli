# -----------------------------------
# Name: jescorecli.py
# Author: jake-is-ESD-protected
# Date: 2024-03-01
# Description: jescore CLI API and callable arg-parsing.
# -----------------------------------

import argparse
import platform

import serial
from serial.tools import list_ports

from . import config
from .common import (
    CLI_PREFIX_CLIENT,
    CLI_PREFIX_MCU,
    CLI_VERBOSE_DEBUG_PREFIX,
    KNOWN_HOSTS,
    RESPONSE_OK,
    RESPONSE_TRX_OVER,
)


class CjescoreCli:
    def __init__(self, port, baudrate=115200, verbose=False) -> None:
        self.os_type = platform.system()
        self.baudrate = baudrate
        self.verbose = verbose
        self.port = port

    @classmethod
    def vprint(cls, printable, end='\n'):
        if config.config_verbose:
            print(CLI_VERBOSE_DEBUG_PREFIX, printable, end=end)

    @classmethod
    def cliprint(cls, printable, end='\n'):
        if config.config_cli_usage:
            print(printable, end=end)

    @classmethod
    def discoverports(cls):
        ports = list(list_ports.comports())
        descriptors = []
        for port in ports:
            for device, host in KNOWN_HOSTS.items():
                if host in port.hwid:
                    descriptors.append(f"{device} ({host} | {port.name}) ")
        return descriptors

    @classmethod
    def portautodetect(cls):
        ports = list(list_ports.comports())
        for port in ports:
            CjescoreCli.vprint(f"Found device: {port.hwid} on port {port.name}")
            for host in KNOWN_HOSTS.values():
                if host in port.hwid:
                    return CjescoreCli.__formatportforos(port.name)
        return None

    @classmethod
    def __formatportforos(cls, port):
        """Prefix the port with '/dev/' if the system is Linux."""
        if platform.system() == "Linux" and not port.startswith("/dev/"):
            return f"/dev/{port}"
        return port

    def uarttransceive(self, msg: str, port: str = None, waittime: float = 0.01, filt=None, keepopen=False) -> str:
        try:
            port_name = port if port else self.port
            CjescoreCli.vprint(f"Sending raw string '{msg}' to jescore on port {port_name}")
            ser = serial.Serial(port_name, baudrate=self.baudrate, timeout=waittime)
            ser.flush()
            ser.setRTS(False)
            ser.write(msg.encode())
            stat = ""
            returns = []
            if keepopen:
                while 1:
                    stat = ser.readline().decode('utf-8', errors="ignore").strip("\n\r\x00")
                    if stat != "":
                        if filt and not any(f in stat for f in filt):
                            continue
                        CjescoreCli.cliprint(stat, end=config.config_iteration_print_end)
            while RESPONSE_TRX_OVER not in stat:
                stat = ser.readline().decode('utf-8', errors="ignore").strip("\n\r\x00")
                if stat != "":
                    if RESPONSE_TRX_OVER in stat:
                        CjescoreCli.vprint(RESPONSE_OK)
                    returns.append(stat)
            if len(returns) != 1:
                CjescoreCli.cliprint(CLI_PREFIX_CLIENT)
            for s in returns:
                if CLI_PREFIX_MCU not in s:
                    if filt and not any(f in s for f in filt):
                        continue
                    CjescoreCli.cliprint(s)
            return returns
        except KeyboardInterrupt:
            CjescoreCli.vprint(f"Closing port {port_name}.")
            return

    def run(self, command, filt):
        if command:
            stat = self.uarttransceive(command, filt=filt)
            CjescoreCli.vprint(f"Received raw string {stat}")
        else:
            CjescoreCli.cliprint("Error: Command not specified.")


def main():
    parser = argparse.ArgumentParser(description="CLI for jescore serial communication.")
    parser.add_argument("command", type=str, nargs='?', help="Command to send to jescore")
    parser.add_argument("-p", "--port", type=str, help="Specify the port for connection")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose output")
    parser.add_argument("-b", "--baudrate", type=int, default=115200, help="Baud rate for communication (default: 115200)")
    parser.add_argument("-d", "--discover", action="store_true", help="Discover connected devices known to jescore")
    parser.add_argument("-l", "--listen", action="store_true", help="Listen to the given UART stream")
    parser.add_argument("--inline", action="store_true", help="Enable inline mode when listening with -l")
    parser.add_argument("--filter", type=str, help="Filter messages originating from certain jobs. Use brackets [,] for multiple job names.")

    args, unknown_args = parser.parse_known_args()
    config.config_verbose = args.verbose
    config.config_cli_usage = True

    if args.discover:
        descriptors = CjescoreCli.discoverports()
        for descriptor in descriptors:
            CjescoreCli.cliprint(descriptor)
        return

    if not args.port:
        port = CjescoreCli.portautodetect()
    else:
        port = args.port
    if not port and not args.port:
        CjescoreCli.cliprint("No jescore-enabled device detected!")
        exit()
    cli = CjescoreCli(baudrate=args.baudrate, port=port, verbose=args.verbose)

    if args.filter:
        filt = args.filter.strip('[]').split(',')
        filt.append("core")
    else:
        if args.command:
            filt = [args.command, "core"]
        else:
            filt = None

    if args.inline:
        config.config_iteration_print_end = '\r'

    command_to_send = ' '.join([args.command] + unknown_args) if args.command else ' '.join(unknown_args)
    cli.uarttransceive(command_to_send, filt=filt, keepopen=args.listen)


if __name__ == "__main__":
    main()
