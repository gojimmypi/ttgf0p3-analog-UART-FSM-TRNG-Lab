# Example ESP32 Output

<!--- # Do not move this file. Referenced by TT 4337 Documentation https://app.tinytapeout.com/projects/4337 --->


```text
gojimmypi:/mnt/c/workspace/ttgf-UART-FSM-TRNG-Lab/ulx3s/ESP32
$ idf.py -p /dev/ttyS3 -b 115200 monitor
Executing action: monitor
Running idf_monitor in directory /mnt/c/workspace/ttgf-UART-FSM-TRNG-Lab/ulx3s/ESP32
Executing "/home/gojimmypi/.espressif/python_env/idf5.5_py3.10_env/bin/python /mnt/c/SysGCC/esp32-master/esp-idf/v5.5/tools/idf_monitor.py -p /dev/ttyS3 -b 115200 --toolchain-prefix xtensa-esp32-elf- --target esp32 --revision 0 /mnt/c/workspace/ttgf-UART-FSM-TRNG-Lab/ulx3s/ESP32/build/ulx3s_esp32.elf /mnt/c/workspace/ttgf-UART-FSM-TRNG-Lab/ulx3s/ESP32/build/bootloader/bootloader.elf -m '/home/gojimmypi/.espressif/python_env/idf5.5_py3.10_env/bin/python' '/mnt/c/SysGCC/esp32-master/esp-idf/v5.5/tools/idf.py' '-p' '/dev/ttyS3' '-b' '115200'"...
--- esp-idf-monitor 1.6.2 on /dev/ttyS3 115200
--- Quit: Ctrl+] | Menu: Ctrl+T | Help: Ctrl+T followed by Ctrl+H
I (13) boot: ESP-IDF v5.5 2nd stage bootloader
I (13) boot: compile time Jun 18 2026 18:48:34
I (13) boot: Multicore bootloader
I (13) boot: chip revision: v1.0
I (16) boot.esp32: SPI Speed      : 40MHz
I (20) boot.esp32: SPI Mode       : DIO
I (23) boot.esp32: SPI Flash Size : 2MB
I (27) boot: Enabling RNG early entropy source...
I (31) boot: Partition Table:
I (34) boot: ## Label            Usage          Type ST Offset   Length
I (40) boot:  0 nvs              WiFi data        01 02 00009000 00006000
I (47) boot:  1 phy_init         RF data          01 01 0000f000 00001000
I (53) boot:  2 factory          factory app      00 00 00010000 00100000
I (60) boot: End of partition table
I (63) esp_image: segment 0: paddr=00010020 vaddr=3f400020 size=0a680h ( 42624) map
I (85) esp_image: segment 1: paddr=0001a6a8 vaddr=3ff80000 size=00020h (    32) load
I (85) esp_image: segment 2: paddr=0001a6d0 vaddr=3ffb0000 size=023dch (  9180) load
I (92) esp_image: segment 3: paddr=0001cab4 vaddr=40080000 size=03564h ( 13668) load
I (102) esp_image: segment 4: paddr=00020020 vaddr=400d0020 size=1353ch ( 79164) map
I (131) esp_image: segment 5: paddr=00033564 vaddr=40083564 size=0b414h ( 46100) load
I (156) boot: Loaded app from partition at offset 0x10000
I (156) boot: Disabling RNG early entropy source...
I (167) cpu_start: Multicore app
I (175) cpu_start: Pro cpu start user code
I (175) cpu_start: cpu freq: 160000000 Hz
I (175) app_init: Application information:
I (178) app_init: Project name:     ulx3s_esp32
I (183) app_init: App version:      1.0.3-43-gb4a00dd-dirty
I (190) app_init: Compile time:     Jun 18 2026 21:51:26
I (196) app_init: ELF file SHA256:  e10a9e36c...
I (201) app_init: ESP-IDF:          v5.5
I (205) efuse_init: Min chip rev:     v0.0
I (210) efuse_init: Max chip rev:     v3.99
I (215) efuse_init: Chip rev:         v1.0
I (220) heap_init: Initializing. RAM available for dynamic allocation:
I (227) heap_init: At 3FFAE6E0 len 00001920 (6 KiB): DRAM
I (233) heap_init: At 3FFB2C98 len 0002D368 (180 KiB): DRAM
I (239) heap_init: At 3FFE0440 len 00003AE0 (14 KiB): D/IRAM
I (246) heap_init: At 3FFE4350 len 0001BCB0 (111 KiB): D/IRAM
I (252) heap_init: At 4008E978 len 00011688 (69 KiB): IRAM
I (259) spi_flash: detected chip: generic
I (263) spi_flash: flash io: dio
W (267) spi_flash: Detected size(4096k) larger than the size in the binary image header(2048k). Using the size in the binary image header.
I (281) main_task: Started on CPU0
I (291) main_task: Calling app_main()
I (291) main: ------------------- ULX3S ESP32 Example ----------------
I (291) main: --------------------------------------------------------
I (301) main: --------------------------------------------------------
I (301) main: ---------------------- BEGIN MAIN ----------------------
I (311) main: --------------------------------------------------------
I (321) main: --------------------------------------------------------
I (331) main: Stack Start: 0x0
I (331) main: Stack HWM: 2408

Hello world 3!
This is esp32 chip with 2 CPU core(s), WiFi/BTBLE, silicon revision v1.0, 2MB external flash
Minimum free heap size: 305488 bytes
I (351) main: SPI write mode: boot config once
I (351) ulx3s_spi: SPI regs: R0=00 R1=00 R2=10 R3=00 R4=01 R5=04 R6=00 R7=00 raw=0x0000 status=0x04 src=0 div=0x10 mode=0x00 oscen=0x01
I (461) main: TRNG deterministic LFSR test
I (461) main: lfsr test sample 00: raw=0x7F2E status=0x00
I (461) main: lfsr test sample 01: raw=0x9F33 status=0x00
I (461) main: lfsr test sample 02: raw=0xFC1C status=0x00
I (471) main: lfsr test sample 03: raw=0x6F03 status=0x00
I (481) main: lfsr test sample 04: raw=0x4B7D status=0x00
I (481) main: lfsr test sample 05: raw=0x52C8 status=0x00
I (491) main: lfsr test sample 06: raw=0xD6B7 status=0x00
I (491) main: lfsr test sample 07: raw=0xEF2A status=0x00
I (501) main: TRNG live source test: S1 RO0/fallback
I (511) main: S1 RO0/fallback sample 00: raw=0x0C3C status=0x3C
I (521) main: S1 RO0/fallback sample 01: raw=0x1E79 status=0x3C
I (531) main: S1 RO0/fallback sample 02: raw=0x7F81 status=0x3C
I (541) main: S1 RO0/fallback sample 03: raw=0xCFCF status=0x3C
I (551) main: S1 RO0/fallback sample 04: raw=0xCFCC status=0x3C
I (561) main: S1 RO0/fallback sample 05: raw=0x3C00 status=0x3C
I (571) main: S1 RO0/fallback sample 06: raw=0xF333 status=0x3C
I (581) main: S1 RO0/fallback sample 07: raw=0x3CF0 status=0x3C
I (581) main: TRNG live source test: S2 ROX/fallback
I (591) main: S2 ROX/fallback sample 00: raw=0x67F9 status=0x3C
I (601) main: S2 ROX/fallback sample 01: raw=0xCF3C status=0x3C
I (611) main: S2 ROX/fallback sample 02: raw=0x19F8 status=0x3C
I (621) main: S2 ROX/fallback sample 03: raw=0x0000 status=0x3C
I (631) main: S2 ROX/fallback sample 04: raw=0x0FF3 status=0x3C
I (641) main: S2 ROX/fallback sample 05: raw=0x9FFE status=0x3C
I (651) main: S2 ROX/fallback sample 06: raw=0x07FE status=0x3C
I (661) main: S2 ROX/fallback sample 07: raw=0xFF33 status=0x3C
I (661) main: TRNG live source test: S3 MIX/fallback
I (671) main: S3 MIX/fallback sample 00: raw=0x6799 status=0x3C
I (681) main: S3 MIX/fallback sample 01: raw=0xC0FF status=0x3C
I (691) main: S3 MIX/fallback sample 02: raw=0x0C33 status=0x3C
I (701) main: S3 MIX/fallback sample 03: raw=0x3CC0 status=0x3C
I (711) main: S3 MIX/fallback sample 04: raw=0x0C0F status=0x3C
I (721) main: S3 MIX/fallback sample 05: raw=0xC33F status=0x3C
I (731) main: S3 MIX/fallback sample 06: raw=0x7E60 status=0x3C
I (741) main: S3 MIX/fallback sample 07: raw=0x7FFE status=0x3C
I (741) main: TRNG SPI pin register test
I (741) main: pin regs: R8 UI_IN=0x18 R9 UO_OUT=0xD8 R10 UIO_IN=0x00 R11 UIO_OUT=0x70 R12 UIO_OE=0xF4
I (751) main: uio view: observed=0x00 drive_value=0x70 drive_enable=0xF4
I (751) ulx3s_spi: SPI regs: R0=00 R1=00 R2=10 R3=00 R4=01 R5=3C R6=FE R7=7F raw=0x7FFE status=0x3C src=0 div=0x10 mode=0x00 oscen=0x01
I (771) ulx3s_spi: SPI regs: R0=00 R1=00 R2=10 R3=00 R4=01 R5=3C R6=FE R7=7F raw=0x7FFE status=0x3C src=0 div=0x10 mode=0x00 oscen=0x01
I (276781) ulx3s_spi: SPI regs: R0=06 R1=00 R2=2A R3=00 R4=01 R5=00 R6=00 R7=00 raw=0x0000 status=0x00 src=0 div=0x2A mode=0x00 oscen=0x01
I (277781) ulx3s_spi: SPI regs: R0=06 R1=00 R2=2A R3=5C R4=0F R5=00 R6=00 R7=00 raw=0x0000 status=0x00 src=0 div=0x2A mode=0x5C oscen=0x0F
I (278781) ulx3s_spi: SPI regs: R0=00 R1=00 R2=10 R3=00 R4=01 R5=04 R6=00 R7=00 raw=0x0000 status=0x04 src=0 div=0x10 mode=0x00 oscen=0x01
I (279781) ulx3s_spi: SPI regs: R0=06 R1=00 R2=2A R3=5C R4=0F R5=00 R6=00 R7=00 raw=0x0000 status=0x00 src=0 div=0x2A mode=0x5C oscen=0x0F
I (280781) ulx3s_spi: SPI regs: R0=00 R1=00 R2=10 R3=5C R4=0F R5=04 R6=00 R7=00 raw=0x0000 status=0x04 src=0 div=0x10 mode=0x5C oscen=0x0F
I (281781) ulx3s_spi: SPI regs: R0=00 R1=00 R2=10 R3=00 R4=00 R5=00 R6=00 R7=00 raw=0x0000 status=0x00 src=0 div=0x10 mode=0x00 oscen=0x00
I (282781) ulx3s_spi: SPI regs: R0=00 R1=01 R2=01 R3=00 R4=01 R5=3C R6=CC R7=F3 raw=0xF3CC status=0x3C src=1 div=0x01 mode=0x00 oscen=0x01
I (283781) ulx3s_spi: SPI regs: R0=00 R1=03 R2=0F R3=00 R4=FF R5=3C R6=CF R7=CF raw=0xCFCF status=0x3C src=3 div=0x0F mode=0x00 oscen=0xFF
I (284781) ulx3s_spi: SPI regs: R0=00 R1=03 R2=0F R3=00 R4=FF R5=3C R6=0C R7=30 raw=0x300C status=0x3C src=3 div=0x0F mode=0x00 oscen=0xFF
I (285781) ulx3s_spi: SPI regs: R0=01 R1=00 R2=01 R3=00 R4=00 R5=3B R6=D9 R7=4B raw=0x4BD9 status=0x3B src=0 div=0x01 mode=0x00 oscen=0x00
I (286781) ulx3s_spi: SPI regs: R0=00 R1=00 R2=01 R3=00 R4=00 R5=38 R6=52 R7=97 raw=0x9752 status=0x38 src=0 div=0x01 mode=0x00 oscen=0x00
I (287781) ulx3s_spi: SPI regs: R0=00 R1=01 R2=01 R3=00 R4=01 R5=3C R6=00 R7=03 raw=0x0300 status=0x3C src=1 div=0x01 mode=0x00 oscen=0x01
I (288781) ulx3s_spi: SPI regs: R0=00 R1=01 R2=01 R3=00 R4=01 R5=3C R6=99 R7=19 raw=0x1999 status=0x3C src=1 div=0x01 mode=0x00 oscen=0x01
I (289781) ulx3s_spi: SPI regs: R0=00 R1=02 R2=01 R3=00 R4=FF R5=3C R6=3F R7=3F raw=0x3F3F status=0x3C src=2 div=0x01 mode=0x00 oscen=0xFF
I (290781) ulx3s_spi: SPI regs: R0=01 R1=02 R2=01 R3=00 R4=FF R5=3D R6=E0 R7=C3 raw=0xC3E0 status=0x3D src=2 div=0x01 mode=0x00 oscen=0xFF
I (291781) ulx3s_spi: SPI regs: R0=00 R1=03 R2=01 R3=00 R4=FF R5=3C R6=CF R7=F3 raw=0xF3CF status=0x3C src=3 div=0x01 mode=0x00 oscen=0xFF
I (292781) ulx3s_spi: SPI regs: R0=01 R1=03 R2=01 R3=00 R4=FF R5=3F R6=CC R7=06 raw=0x06CC status=0x3F src=3 div=0x01 mode=0x00 oscen=0xFF
I (293781) ulx3s_spi: SPI regs: R0=02 R1=00 R2=01 R3=00 R4=00 R5=00 R6=01 R7=00 raw=0x0001 status=0x00 src=0 div=0x01 mode=0x00 oscen=0x00
I (294781) ulx3s_spi: SPI regs: R0=02 R1=00 R2=01 R3=00 R4=00 R5=00 R6=F9 R7=03 raw=0x03F9 status=0x00 src=0 div=0x01 mode=0x00 oscen=0x00
I (295781) ulx3s_spi: SPI regs: R0=00 R1=00 R2=01 R3=00 R4=00 R5=00 R6=BA R7=FC raw=0xFCBA status=0x00 src=0 div=0x01 mode=0x00 oscen=0x00
I (296781) ulx3s_spi: SPI regs: R0=00 R1=00 R2=01 R3=00 R4=00 R5=00 R6=F9 R7=74 raw=0x74F9 status=0x00 src=0 div=0x01 mode=0x00 oscen=0x00
I (297781) ulx3s_spi: SPI regs: R0=02 R1=00 R2=01 R3=00 R4=00 R5=00 R6=9F R7=F9 raw=0xF99F status=0x00 src=0 div=0x01 mode=0x00 oscen=0x00
I (298781) ulx3s_spi: SPI regs: R0=02 R1=00 R2=01 R3=00 R4=00 R5=00 R6=C1 R7=3F raw=0x3FC1 status=0x00 src=0 div=0x01 mode=0x00 oscen=0x00
I (299781) ulx3s_spi: SPI regs: R0=00 R1=00 R2=01 R3=00 R4=00 R5=00 R6=E3 R7=E0 raw=0xE0E3 status=0x00 src=0 div=0x01 mode=0x00 oscen=0x00
I (300781) ulx3s_spi: SPI regs: R0=00 R1=00 R2=01 R3=00 R4=00 R5=00 R6=F0 R7=C6 raw=0xC6F0 status=0x00 src=0 div=0x01 mode=0x00 oscen=0x00
I (301781) ulx3s_spi: SPI regs: R0=02 R1=00 R2=01 R3=00 R4=00 R5=00 R6=34 R7=F0 raw=0xF034 status=0x00 src=0 div=0x01 mode=0x00 oscen=0x00
I (302781) ulx3s_spi: SPI regs: R0=02 R1=00 R2=01 R3=00 R4=00 R5=00 R6=6F R7=69 raw=0x696F status=0x00 src=0 div=0x01 mode=0x00 oscen=0x00
I (303781) ulx3s_spi: SPI regs: R0=02 R1=00 R2=01 R3=00 R4=00 R5=00 R6=D5 R7=B7 raw=0xB7D5 status=0x00 src=0 div=0x01 mode=0x00 oscen=0x00
I (304781) ulx3s_spi: SPI regs: R0=02 R1=00 R2=01 R3=00 R4=00 R5=00 R6=59 R7=AA raw=0xAA59 status=0x00 src=0 div=0x01 mode=0x00 oscen=0x00
I (305781) ulx3s_spi: SPI regs: R0=00 R1=00 R2=01 R3=00 R4=00 R5=00 R6=8D R7=2C raw=0x2C8D status=0x00 src=0 div=0x01 mode=0x00 oscen=0x00
I (306781) ulx3s_spi: SPI regs: R0=00 R1=00 R2=01 R3=00 R4=00 R5=00 R6=D6 R7=1A raw=0x1AD6 status=0x00 src=0 div=0x01 mode=0x00 oscen=0x00
I (307781) ulx3s_spi: SPI regs: R0=02 R1=00 R2=01 R3=00 R4=00 R5=00 R6=FD R7=D6 raw=0xD6FD status=0x00 src=0 div=0x01 mode=0x00 oscen=0x00
I (308781) ulx3s_spi: SPI regs: R0=02 R1=00 R2=01 R3=00 R4=00 R5=00 R6=CA R7=FB raw=0xFBCA status=0x00 src=0 div=0x01 mode=0x00 oscen=0x00
I (309781) ulx3s_spi: SPI regs: R0=02 R1=00 R2=01 R3=00 R4=00 R5=00 R6=01 R7=00 raw=0x0001 status=0x00 src=0 div=0x01 mode=0x00 oscen=0x00
I (310781) ulx3s_spi: SPI regs: R0=02 R1=00 R2=01 R3=00 R4=00 R5=00 R6=F9 R7=03 raw=0x03F9 status=0x00 src=0 div=0x01 mode=0x00 oscen=0x00
I (311781) ulx3s_spi: SPI regs: R0=00 R1=00 R2=01 R3=00 R4=00 R5=00 R6=BA R7=FC raw=0xFCBA status=0x00 src=0 div=0x01 mode=0x00 oscen=0x00
I (312781) ulx3s_spi: SPI regs: R0=00 R1=00 R2=01 R3=00 R4=00 R5=00 R6=F9 R7=74 raw=0x74F9 status=0x00 src=0 div=0x01 mode=0x00 oscen=0x00
I (313781) ulx3s_spi: SPI regs: R0=02 R1=00 R2=01 R3=00 R4=00 R5=00 R6=9F R7=F9 raw=0xF99F status=0x00 src=0 div=0x01 mode=0x00 oscen=0x00
I (314781) ulx3s_spi: SPI regs: R0=02 R1=00 R2=01 R3=00 R4=00 R5=00 R6=C1 R7=3F raw=0x3FC1 status=0x00 src=0 div=0x01 mode=0x00 oscen=0x00
I (315781) ulx3s_spi: SPI regs: R0=00 R1=00 R2=01 R3=00 R4=00 R5=00 R6=E3 R7=E0 raw=0xE0E3 status=0x00 src=0 div=0x01 mode=0x00 oscen=0x00
I (316781) ulx3s_spi: SPI regs: R0=00 R1=00 R2=01 R3=00 R4=00 R5=00 R6=F0 R7=C6 raw=0xC6F0 status=0x00 src=0 div=0x01 mode=0x00 oscen=0x00
I (317781) ulx3s_spi: SPI regs: R0=00 R1=00 R2=01 R3=00 R4=00 R5=00 R6=34 R7=F0 raw=0xF034 status=0x00 src=0 div=0x01 mode=0x00 oscen=0x00
I (318781) ulx3s_spi: SPI regs: R0=00 R1=00 R2=01 R3=00 R4=00 R5=00 R6=6F R7=69 raw=0x696F status=0x00 src=0 div=0x01 mode=0x00 oscen=0x00
I (319781) ulx3s_spi: SPI regs: R0=02 R1=00 R2=01 R3=00 R4=00 R5=00 R6=AA R7=6F raw=0x6FAA status=0x00 src=0 div=0x01 mode=0x00 oscen=0x00
I (320781) ulx3s_spi: SPI regs: R0=02 R1=00 R2=01 R3=00 R4=00 R5=00 R6=B2 R7=54 raw=0x54B2 status=0x00 src=0 div=0x01 mode=0x00 oscen=0x00
I (321781) ulx3s_spi: SPI regs: R0=00 R1=00 R2=01 R3=00 R4=00 R5=00 R6=1A R7=59 raw=0x591A status=0x00 src=0 div=0x01 mode=0x00 oscen=0x00
I (322781) ulx3s_spi: SPI regs: R0=00 R1=00 R2=01 R3=00 R4=00 R5=00 R6=AD R7=35 raw=0x35AD status=0x00 src=0 div=0x01 mode=0x00 oscen=0x00
I (323781) ulx3s_spi: SPI regs: R0=02 R1=00 R2=01 R3=00 R4=00 R5=00 R6=FB R7=AD raw=0xADFB status=0x00 src=0 div=0x01 mode=0x00 oscen=0x00
I (324781) ulx3s_spi: SPI regs: R0=00 R1=00 R2=01 R3=00 R4=00 R5=00 R6=95 R7=F7 raw=0xF795 status=0x00 src=0 div=0x01 mode=0x00 oscen=0x00
I (325781) ulx3s_spi: SPI regs: R0=00 R1=00 R2=01 R3=00 R4=00 R5=00 R6=2A R7=EF raw=0xEF2A status=0x00 src=0 div=0x01 mode=0x00 oscen=0x00
```
