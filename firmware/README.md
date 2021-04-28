# Firmware

Electrosense firmware can be found at: https://github.com/electrosense/hardware

The binaries folder contains binaries compiled using [gcc for Arm](https://developer.arm.com/tools-and-software/open-source-software/developer-tools/gnu-toolchain/gnu-rm/downloads/product-release), ready to be flashed to the STM32 CPU. The bootloader (esense_bootloader.bin) is first loaded using the ST-LINK V2 and [accompanying software](https://www.st.com/en/development-tools/stsw-link004.html). The firmware (esense.bin) is then loaded over USB using [dfu-util](http://dfu-util.sourceforge.net/).

At the time of this project, the firmware had not been updated for this version of the board.
The base commit is [3b2e7c6b33](https://github.com/electrosense/hardware/tree/3b2e7c6b335081feabfaab9ab29f9687f472fbd4).

The following changes were made (detailed changelog in source folder):
- Updated GPIO pin assignments for newest version of board
- Set MCO pin mode to "input" when not in use
