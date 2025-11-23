<img width="1920" height="300" alt="jescore_cli_logo_banner" src="https://github.com/user-attachments/assets/65346ad1-1f6f-41f8-86b4-0e27a6e0d3b5" />

# jescorecli

|Main Repo 🔆|PyPi Package 📦️|Support 🙏|
|-|-|-|
|[<img src="https://github.com/user-attachments/assets/2fc4f696-0a6c-444b-a99b-053f9bee6d59" width="100"/>](https://github.com/jesdev-io/jescore)||[![Buy me a coffee](https://img.shields.io/badge/Ko--fi-Support%20Me-FF5E5B?style=for-the-badge&logo=ko-fi&logoColor=white)](https://ko-fi.com/jseshack)|

**Host-side serial CLI for MCUs running `jescore`.** This is a Python wrapper for serial communication with MCUs that have a version of `jescore` running on them and are connected by their USB-to-UART interface (default interface for most dev board MCUs). With this tool you can steer your MCU from your standard terminal by invoking `jescore <command>`. See [`jescore` CLI documentation](https://github.com/jesdev-io/jescore/wiki/CLI-Documentation).

## How to use
Install this package with its URL or with PyPi and `pip` in a virtual environment:
```bash
pip install git+https://github.com/jesdev-io/jescorecli.git # via URL
pip install jescorecli # via pypi
```

You can install it globally with `pipx` if you have multiple projects that use `jescore`:
```bash
pipx install git+https://github.com/jesdev-io/jescorecli.git
pipx install jescorecli
```

If you have a MCU with `jescore` running connected to your PC, you can now communicate with it.

```bash
jescore stats # list the stats of your MCU's firmware
jescore -p /dev/ttyACM0 help # list the available commands of your MCU connected to port ACM0
jescore -l # keep the serial terminal open to listen for your MCU's messages.
```

**See more commands [in the wiki](https://github.com/jesdev-io/jescore/wiki/CLI-Documentation#option-1-jescore-cli)**.


## Module structure
This module wraps `pyserial` and maps `jescore` specific string patterns to serial I/O. It enables to to use your terminal of choice to behave like a serial terminal emulator with extra QOL sugar. The module is structured as such:
- `common.py`: String literals that `jescore` expects on the MCU side.
- `config.py`: Session-specific configuration variables that handle verbosity and specific line endings.
- `jescorecli.py`: `pyserial` wrapper and driver code for the module.

## About Testing
This module's unit testing does not test the module itself, but rather the MCU's response to the built-in serial commands. It therefore does not make sense to run these tests without a `jescore`-enabled MCU attached. You can start testing by installing this module in the development version with `pip install jescorecli[dev]` and then running `pytest`.