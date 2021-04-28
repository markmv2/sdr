# Electrosense converter

This project contains the firmware for the downconverter part of the electrosense.org spectrum sensor. It extends the range of a standard RTL-SDR to >6GHz.

Directory structure:

 * bootloader: A slightly modified stm32duino-bootloader. There is no reason to recompile this, just use the esense_boot.bin binary.
 * FreeRTOS: This is the FreeRTOS operating system. If you want to compile the firmware you must run make here first.
 * ChibiOS: Some components from ChibiOS HAL.
 * firmware: This is the actual firmware. Run make here to build the image.

firmware/changelog.txt contains the diff output that compares this commit and [3b2e7c6b33](https://github.com/electrosense/hardware/tree/3b2e7c6b335081feabfaab9ab29f9687f472fbd4).