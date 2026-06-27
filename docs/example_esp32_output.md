# Example ESP32 Output

<!--- # Do not move this file. Referenced by TT 4337 Documentation https://app.tinytapeout.com/projects/4337 --->

<!--- # Use only Fully Qualified URLs. This file is copied out of the GitHub repo for publication. --->

This is the example output for the [ESP32 example app](https://github.com/gojimmypi/ttgf0p3-UART-FSM-TRNG-Lab/tree/main/ulx3s/ESP32) 
on the [Radiona ULX3S FPGA](https://radiona.org/ulx3s/) 
for the [Hardware Entropy Explorer: UART/SPI TRNG and PUF](https://app.tinytapeout.com/projects/4337) project.

The source code for this test is in [`ulx3s/ESP32`](https://github.com/gojimmypi/ttgf0p3-UART-FSM-TRNG-Lab/tree/main/ulx3s/ESP32).

Users of the [VisualGDB](https://visualgdb.com/) Extension for Visual Studio can 
find a project file in [ulx3s/ESP32/VisualGDB](https://github.com/gojimmypi/ttgf0p3-UART-FSM-TRNG-Lab/tree/main/ulx3s/ESP32/VisualGDB)

```text
ets Jun  8 2016 00:22:57

rst:0x1 (POWERON_RESET),boot:0x13 (SPI_FAST_FLASH_BOOT)
configsip: 0, SPIWP:0xee
clk_drv:0x00,q_drv:0x00,d_drv:0x00,cs0_drv:0x00,hd_drv:0x00,wp_drv:0x00
mode:DIO, clock div:2
load:0x3fff0030,len:6380
ho 0 tail 12 room 4
load:0x40078000,len:15916
load:0x40080400,len:3860
entry 0x40080638
I (29) boot: ESP-IDF v5.5 2nd stage bootloader
I (29) boot: compile time Jun 18 2026 18:48:34
I (29) boot: Multicore bootloader
I (30) boot: chip revision: v1.0
I (33) boot.esp32: SPI Speed      : 40MHz
I (37) boot.esp32: SPI Mode       : DIO
I (40) boot.esp32: SPI Flash Size : 2MB
I (44) boot: Enabling RNG early entropy source...
I (48) boot: Partition Table:
I (51) boot: ## Label            Usage          Type ST Offset   Length
I (57) boot:  0 nvs              WiFi data        01 02 00009000 00006000
I (64) boot:  1 phy_init         RF data          01 01 0000f000 00001000
I (70) boot:  2 factory          factory app      00 00 00010000 00100000
I (77) boot: End of partition table
I (80) esp_image: segment 0: paddr=00010020 vaddr=3f400020 size=0d460h ( 54368) map
I (106) esp_image: segment 1: paddr=0001d488 vaddr=3ff80000 size=00020h (    32) load
I (106) esp_image: segment 2: paddr=0001d4b0 vaddr=3ffb0000 size=023dch (  9180) load
I (113) esp_image: segment 3: paddr=0001f894 vaddr=40080000 size=00784h (  1924) load
I (118) esp_image: segment 4: paddr=00020020 vaddr=400d0020 size=14c7ch ( 85116) map
I (154) esp_image: segment 5: paddr=00034ca4 vaddr=40080784 size=0e1f4h ( 57844) load
I (184) boot: Loaded app from partition at offset 0x10000
I (184) boot: Disabling RNG early entropy source...
I (195) cpu_start: Multicore app
I (203) cpu_start: Pro cpu start user code
I (203) cpu_start: cpu freq: 160000000 Hz
I (203) app_init: Application information:
I (206) app_init: Project name:     ulx3s_esp32
I (211) app_init: App version:      1.0.3-71-g3c6be2e-dirty
I (217) app_init: Compile time:     Jun 20 2026 11:46:31
I (223) app_init: ELF file SHA256:  72cfb981b...
I (229) app_init: ESP-IDF:          v5.5
I (233) efuse_init: Min chip rev:     v0.0
I (238) efuse_init: Max chip rev:     v3.99
I (243) efuse_init: Chip rev:         v1.0
I (248) heap_init: Initializing. RAM available for dynamic allocation:
I (255) heap_init: At 3FFAE6E0 len 00001920 (6 KiB): DRAM
I (261) heap_init: At 3FFB2C98 len 0002D368 (180 KiB): DRAM
I (267) heap_init: At 3FFE0440 len 00003AE0 (14 KiB): D/IRAM
I (274) heap_init: At 3FFE4350 len 0001BCB0 (111 KiB): D/IRAM
I (280) heap_init: At 4008E978 len 00011688 (69 KiB): IRAM
I (287) spi_flash: detected chip: generic
I (291) spi_flash: flash io: dio
W (295) spi_flash: Detected size(4096k) larger than the size in the binary image header(2048k). Using the size in the binary image header.
I (309) main_task: Started on CPU0
I (319) main_task: Calling app_main()
I (319) main: ------------------- ULX3S ESP32 Example ----------------
I (319) main: --------------------------------------------------------
I (329) main: --------------------------------------------------------
I (329) main: ---------------------- BEGIN MAIN ----------------------
I (339) main: --------------------------------------------------------
I (349) main: --------------------------------------------------------
I (359) main: Stack Start: 0x0
I (359) main: Stack HWM: 2440
I (359) main: Minimum free heap size: 305488 bytes

TT project_config.v effective settings (excludes project.v)
-----------------------------------------------------------
TT_MACRO_ADJUSTABLE_BAUD_ENABLED: 1
TT_MACRO_BIG16_SPI_REG: 1
TT_MACRO_JTAG_ADDR_MSB: 3
TT_MACRO_JTAG_ADDR_WIDTH: 4
TT_MACRO_JTAG_ENABLED: 1
TT_MACRO_PROJECT_CLOCK_HZ: 25000000
TT_MACRO_PROJECT_CONFIG_V: 1
TT_MACRO_PROJECT_UART_BAUD: 115200
TT_MACRO_SPI_ADDR_MSB: 3
TT_MACRO_SPI_ADDR_WIDTH: 4
TT_MACRO_SPI_ENABLED: 1
TT_MACRO_SPI_REG_ACCESS: 1
TT_MACRO_TRNG_BINARY_STREAM: 1
TT_MACRO_TRNG_CONDITIONED_STREAM: 1
TT_MACRO_TRNG_CONDITIONED_STREAM_GALOIS: 1
TT_MACRO_TRNG_ENABLED: 1
TT_MACRO_TRNG_HEALTH_STATUS: 1
TT_MACRO_TRNG_RAW_CLEAN_MIX: 1
TT_MACRO_UART_ENABLED: 1
TT_MACRO_USE_LONG_STRINGS: 1
TT_MACRO_VERSION_STRING_LEN: 23
TT_MACRO_VERSION_STRING: Version 1.0.5 6/27/2026
-----------------------------------------------------------
This is esp32 chip with 2 CPU core(s), WiFi/BTBLE, silicon revision v1.0, 2MB external flash
I (449) main: Tiny Tapeout SPI Test Version 1.0.5 6/27/2026
I (459) main: --------------------------------------------------------
I (469) main: Initialize ESP32 SPI bus
I (469) main: --------------------------------------------------------
I (479) main: Main step: configure ESP32 SPI peripheral and attach the ULX3S FPGA SPI device
I (489) ulx3s_spi: --------------------------------------------------------
I (499) ulx3s_spi: SPI Config:
I (499) ulx3s_spi: --------------------------------------------------------
I (509) ulx3s_spi: ULX3S_SPI_HOST: SPI2_HOST (1)
I (509) ulx3s_spi: SPI_CLOCK_HZ:   1000000
I (519) ulx3s_spi: PIN_NUM_CS:     21
I (519) ulx3s_spi: PIN_NUM_MISO:   19
I (529) ulx3s_spi: PIN_NUM_MOSI:   23
I (529) ulx3s_spi: PIN_NUM_CLK:    18
I (529) ulx3s_spi: --------------------------------------------------------
I (539) main: --------------------------------------------------------
I (549) main: Run SPI register self-check
I (549) main: --------------------------------------------------------
I (559) main: Main step: validate R0-RF register map, pin snapshot registers, and active R6/R7 raw-change behavior
I (569) ulx3s_spi: --------------------------------------------------------
I (579) ulx3s_spi: SPI self-check: begin
I (579) ulx3s_spi: --------------------------------------------------------
I (589) ulx3s_spi: SPI self-check purpose: verify R0-RF SPI register map, expected defaults, pin snapshots, and active raw movement
I (599) ulx3s_spi: SPI self-check expected defaults after reset: R0=0x00 R1=0x00 R2=0x10 R3=0x00 R4=0x01
I (609) ulx3s_spi: SPI self-check expected R5 status: cold/reset 0x04 is allowed before TRNG warm-up; warmed/default is 0x3C
I (629) ulx3s_spi: SPI self-check expected BIG16 registers: R8 has UART RX idle bit set, RC=0xF4, RD=ASIC GF180 or ULX3S build target, RE/RF=0x00
I (639) ulx3s_spi: --------------------------------------------------------
I (649) ulx3s_spi: SPI self-check: reset config registers to known defaults
I (659) ulx3s_spi: --------------------------------------------------------
I (659) ulx3s_spi: SPI self-check reset reason: ESP32 reset may not reset the FPGA register state
I (689) ulx3s_spi: --------------------------------------------------------
I (689) ulx3s_spi: SPI self-check: read R0-RF and compare register-map expectations
I (689) ulx3s_spi: --------------------------------------------------------
I (699) ulx3s_spi: SPI regs: R0=00 R1=00 R2=10 R3=00 R4=01 R5=04 R6=00 R7=00
I (709) ulx3s_spi: SPI regs: R8=08 R9=18 RA=00 RB=00 RC=F4 RD=8A RE=00 RF=00
I (709) ulx3s_spi: raw=0x0000 status=0x04 src=0 div=0x10 mode=0x00 oscen=0x01 build=0x8A(FPGA TT DEMOBOARD) ui=0x08 uo=0x18 uio_in=0x00 uio_out=0x00 uio_oe=0xF4
I (729) ulx3s_spi: SPI self-check step 1/3: compare stable registers and log dynamic pin snapshot registers
I (739) ulx3s_spi: SPI self-check PASS R0 CTRL: 00
I (739) ulx3s_spi: SPI self-check PASS R1 SRC: 00
I (749) ulx3s_spi: SPI self-check PASS R2 DIV: 10
I (759) ulx3s_spi: SPI self-check PASS R3 MODE: 00
I (759) ulx3s_spi: SPI self-check PASS R4 OSCEN: 01
I (769) ulx3s_spi: SPI self-check PASS R8 UI_IN UART_RX_IDLE: actual 08 mask 08 value 08
I (779) ulx3s_spi: SPI self-check INFO R9 UO_OUT: 18
I (779) ulx3s_spi: SPI self-check INFO RA UIO_IN: 00
I (789) ulx3s_spi: SPI self-check INFO RB UIO_OUT: 00
I (789) ulx3s_spi: SPI self-check PASS RC UIO_OE: F4
I (799) ulx3s_spi: SPI self-check PASS RD BUILD_TARGET ASIC_GF180_OR_ULX3S: actual 8A (FPGA TT DEMOBOARD)
I (809) ulx3s_spi: SPI self-check PASS RE UNUSED: 00
I (809) ulx3s_spi: SPI self-check PASS RF UNUSED: 00
I (819) ulx3s_spi: SPI self-check PASS R5 STATUS initial cold/reset state: 04
I (829) ulx3s_spi: SPI self-check note: R5=0x04 is allowed immediately after FPGA/project reset before TRNG warm-up
I (839) ulx3s_spi: SPI self-check step 2/3: record passive R6/R7 snapshot before active TRNG check
I (849) ulx3s_spi: SPI self-check INFO R6/R7 raw initial snapshot: 0x0000
I (859) ulx3s_spi: SPI self-check step 3/3: temporarily enable TRNG and require R6/R7 to change
I (869) ulx3s_spi: --------------------------------------------------------
I (869) ulx3s_spi: SPI self-check: active R6/R7 raw-change test
I (879) ulx3s_spi: --------------------------------------------------------
I (889) ulx3s_spi: SPI self-check purpose: prove R6/R7 are not fixed when the TRNG is explicitly enabled
I (899) ulx3s_spi: SPI self-check active config: write R0=00, R1=0x03, R2=0x01, R3=0x00, R4=0xFF, then R0=0x01
I (909) ulx3s_spi: SPI self-check pass rule: at least two unique 16-bit raw values across 8 samples
I (919) ulx3s_spi: SPI self-check active config applied; settling for 20 ms before sampling...
I (949) ulx3s_spi: SPI self-check raw sample 0: raw=0xFF00 ctrl=0x01 status=0x3F src=3 div=0x01 mode=0x00 oscen=0xFF
I (959) ulx3s_spi: SPI self-check raw sample 1: raw=0xF30C ctrl=0x01 status=0x3F src=3 div=0x01 mode=0x00 oscen=0xFF
I (969) ulx3s_spi: SPI self-check raw sample 2: raw=0xFCFF ctrl=0x01 status=0x3F src=3 div=0x01 mode=0x00 oscen=0xFF
I (979) ulx3s_spi: SPI self-check raw sample 3: raw=0xFFFC ctrl=0x01 status=0x3F src=3 div=0x01 mode=0x00 oscen=0xFF
I (989) ulx3s_spi: SPI self-check raw sample 4: raw=0xCC3C ctrl=0x01 status=0x3F src=3 div=0x01 mode=0x00 oscen=0xFF
I (999) ulx3s_spi: SPI self-check raw sample 5: raw=0x3FCC ctrl=0x01 status=0x3F src=3 div=0x01 mode=0x00 oscen=0xFF
I (1009) ulx3s_spi: SPI self-check raw sample 6: raw=0x0078 ctrl=0x01 status=0x3F src=3 div=0x01 mode=0x00 oscen=0xFF
I (1019) ulx3s_spi: SPI self-check raw sample 7: raw=0x00F9 ctrl=0x01 status=0x3D src=3 div=0x01 mode=0x00 oscen=0xFF
I (1029) ulx3s_spi: SPI self-check: restoring saved config after active raw-change test
I (1029) ulx3s_spi: SPI self-check PASS R6/R7 raw changed: unique=8/8 first=0xFF00 last=0x00F9
I (1039) ulx3s_spi: --------------------------------------------------------
I (1049) ulx3s_spi: SPI self-check step 3/3: re-read R0-RF after active warm-up and restore
I (1059) ulx3s_spi: SPI regs: R0=00 R1=00 R2=10 R3=00 R4=01 R5=3C R6=00 R7=FC
I (1069) ulx3s_spi: SPI regs: R8=08 R9=18 RA=F0 RB=F0 RC=F4 RD=8A RE=00 RF=00
I (1079) ulx3s_spi: raw=0xFC00 status=0x3C src=0 div=0x10 mode=0x00 oscen=0x01 build=0x8A(FPGA TT DEMOBOARD) ui=0x08 uo=0x18 uio_in=0xF0 uio_out=0xF0 uio_oe=0xF4
I (1089) ulx3s_spi: SPI self-check PASS R5 STATUS after active warm-up/restore: 3C
I (1099) ulx3s_spi: SPI self-check final pin snapshot after warm-up/restore: ui=0x08 uo=0x18 uio_in=0xF0 uio_out=0xF0 uio_oe=0xF4
I (1109) ulx3s_spi: SPI self-check result: PASS, pass=12 fail=0
I (1119) main: --------------------------------------------------------
I (1119) main: Run RO activity characterization
I (1129) main: --------------------------------------------------------
I (1139) main: Main step: sweep one-hot oscillator enables in S2 and S3 modes and summarize activity statistics
I (1149) ulx3s_spi: --------------------------------------------------------
I (1159) ulx3s_spi: RO characterize: begin
I (1159) ulx3s_spi: --------------------------------------------------------
I (1169) ulx3s_spi: RO characterize purpose: verify each one-hot oscillator-enable path produces non-fixed SPI-visible raw samples
I (1179) ulx3s_spi: RO characterize scope: S2 ROX/fallback RO0-RO7, S3 MIX/fallback RO0-RO7, then S3 ALL oscen=0xFF
I (1189) ulx3s_spi: RO characterize config: samples=256 div=0x01 mode=0x00 sample_delay_ms=1 settle_ms=10
I (1199) ulx3s_spi: RO characterize pass rules: unique_count > 1, change_count > 0, ones_count not all 0 or all 1
I (1209) ulx3s_spi: RO characterize note: this is an activity screen, not a per-RO frequency or entropy proof
I (1219) ulx3s_spi: --------------------------------------------------------
I (1229) ulx3s_spi: RO characterize phase 1/3: src=2 S2 ROX/fallback, one-hot RO0-RO7
I (1239) ulx3s_spi: --------------------------------------------------------
I (1249) ulx3s_spi: RO characterize test: src=2 S2 ROX/fallback RO0 oscen=0x01
I (1259) ulx3s_spi: RO characterize test purpose: one-hot activity screen using 256 samples; this is not a frequency measurement
I (1269) ulx3s_spi: RO characterize setup: source=2 oscen=0x01; disabling sampling before config writes
I (1279) ulx3s_spi: RO characterize setup writes: R0=00, R1=0x02, R2=0x01, R3=0x00, R4=0x01, R0=0x01
I (1289) ulx3s_spi: RO characterize setup applied; settling for 10 ms before collecting samples...
I (1589) ulx3s_spi: src=2 S2 ROX/fallback RO0 oscen=0x01 unique=222/256 changes=255/255 ones=2050/4096 (50.0%) first=0xE7FC last=0x0C1F min=0x0006 max=0xFFFC status_or=0x3F status_and=0x3D
I (1599) ulx3s_spi: RO characterize PASS
I (1609) ulx3s_spi: .....................
I (1609) ulx3s_spi: RO characterize test: src=2 S2 ROX/fallback RO1 oscen=0x02
I (1619) ulx3s_spi: RO characterize test purpose: one-hot activity screen using 256 samples; this is not a frequency measurement
I (1629) ulx3s_spi: RO characterize setup: source=2 oscen=0x02; disabling sampling before config writes
I (1639) ulx3s_spi: RO characterize setup writes: R0=00, R1=0x02, R2=0x01, R3=0x00, R4=0x02, R0=0x01
I (1649) ulx3s_spi: RO characterize setup applied; settling for 10 ms before collecting samples...
I (1949) ulx3s_spi: src=2 S2 ROX/fallback RO1 oscen=0x02 unique=214/256 changes=255/255 ones=1992/4096 (48.6%) first=0xC00C last=0x3330 min=0x0003 max=0xFFFF status_or=0x3F status_and=0x3D
I (1959) ulx3s_spi: RO characterize PASS
I (1969) ulx3s_spi: .....................
I (1969) ulx3s_spi: RO characterize test: src=2 S2 ROX/fallback RO2 oscen=0x04
I (1979) ulx3s_spi: RO characterize test purpose: one-hot activity screen using 256 samples; this is not a frequency measurement
I (1989) ulx3s_spi: RO characterize setup: source=2 oscen=0x04; disabling sampling before config writes
I (1999) ulx3s_spi: RO characterize setup writes: R0=00, R1=0x02, R2=0x01, R3=0x00, R4=0x04, R0=0x01
I (2009) ulx3s_spi: RO characterize setup applied; settling for 10 ms before collecting samples...
I (2309) ulx3s_spi: src=2 S2 ROX/fallback RO2 oscen=0x04 unique=211/256 changes=253/255 ones=2084/4096 (50.9%) first=0x3FCC last=0x3CCC min=0x0000 max=0xFFFE status_or=0x3F status_and=0x3D
I (2319) ulx3s_spi: RO characterize PASS
I (2329) ulx3s_spi: .....................
I (2329) ulx3s_spi: RO characterize test: src=2 S2 ROX/fallback RO3 oscen=0x08
I (2339) ulx3s_spi: RO characterize test purpose: one-hot activity screen using 256 samples; this is not a frequency measurement
I (2349) ulx3s_spi: RO characterize setup: source=2 oscen=0x08; disabling sampling before config writes
I (2359) ulx3s_spi: RO characterize setup writes: R0=00, R1=0x02, R2=0x01, R3=0x00, R4=0x08, R0=0x01
I (2369) ulx3s_spi: RO characterize setup applied; settling for 10 ms before collecting samples...
I (2669) ulx3s_spi: src=2 S2 ROX/fallback RO3 oscen=0x08 unique=224/256 changes=255/255 ones=2019/4096 (49.3%) first=0x3CE1 last=0xFFFF min=0x0003 max=0xFFFF status_or=0x3F status_and=0x3D
I (2679) ulx3s_spi: RO characterize PASS
I (2689) ulx3s_spi: .....................
I (2689) ulx3s_spi: RO characterize test: src=2 S2 ROX/fallback RO4 oscen=0x10
I (2699) ulx3s_spi: RO characterize test purpose: one-hot activity screen using 256 samples; this is not a frequency measurement
I (2709) ulx3s_spi: RO characterize setup: source=2 oscen=0x10; disabling sampling before config writes
I (2719) ulx3s_spi: RO characterize setup writes: R0=00, R1=0x02, R2=0x01, R3=0x00, R4=0x10, R0=0x01
I (2729) ulx3s_spi: RO characterize setup applied; settling for 10 ms before collecting samples...
I (3029) ulx3s_spi: src=2 S2 ROX/fallback RO4 oscen=0x10 unique=222/256 changes=255/255 ones=2011/4096 (49.1%) first=0x87FC last=0x67C3 min=0x0000 max=0xFFCF status_or=0x3F status_and=0x3D
I (3039) ulx3s_spi: RO characterize PASS
I (3049) ulx3s_spi: .....................
I (3049) ulx3s_spi: RO characterize test: src=2 S2 ROX/fallback RO5 oscen=0x20
I (3059) ulx3s_spi: RO characterize test purpose: one-hot activity screen using 256 samples; this is not a frequency measurement
I (3069) ulx3s_spi: RO characterize setup: source=2 oscen=0x20; disabling sampling before config writes
I (3079) ulx3s_spi: RO characterize setup writes: R0=00, R1=0x02, R2=0x01, R3=0x00, R4=0x20, R0=0x01
I (3089) ulx3s_spi: RO characterize setup applied; settling for 10 ms before collecting samples...
I (3389) ulx3s_spi: src=2 S2 ROX/fallback RO5 oscen=0x20 unique=226/256 changes=255/255 ones=1991/4096 (48.6%) first=0x00C3 last=0xC0C0 min=0x0003 max=0xFFFF status_or=0x3F status_and=0x3D
I (3399) ulx3s_spi: RO characterize PASS
I (3409) ulx3s_spi: .....................
I (3409) ulx3s_spi: RO characterize test: src=2 S2 ROX/fallback RO6 oscen=0x40
I (3419) ulx3s_spi: RO characterize test purpose: one-hot activity screen using 256 samples; this is not a frequency measurement
I (3429) ulx3s_spi: RO characterize setup: source=2 oscen=0x40; disabling sampling before config writes
I (3439) ulx3s_spi: RO characterize setup writes: R0=00, R1=0x02, R2=0x01, R3=0x00, R4=0x40, R0=0x01
I (3449) ulx3s_spi: RO characterize setup applied; settling for 10 ms before collecting samples...
I (3749) ulx3s_spi: src=2 S2 ROX/fallback RO6 oscen=0x40 unique=231/256 changes=255/255 ones=2006/4096 (49.0%) first=0xF03F last=0x0F78 min=0x0000 max=0xFFCF status_or=0x3F status_and=0x3D
I (3759) ulx3s_spi: RO characterize PASS
I (3769) ulx3s_spi: .....................
I (3769) ulx3s_spi: RO characterize test: src=2 S2 ROX/fallback RO7 oscen=0x80
I (3779) ulx3s_spi: RO characterize test purpose: one-hot activity screen using 256 samples; this is not a frequency measurement
I (3789) ulx3s_spi: RO characterize setup: source=2 oscen=0x80; disabling sampling before config writes
I (3799) ulx3s_spi: RO characterize setup writes: R0=00, R1=0x02, R2=0x01, R3=0x00, R4=0x80, R0=0x01
I (3809) ulx3s_spi: RO characterize setup applied; settling for 10 ms before collecting samples...
I (4109) ulx3s_spi: src=2 S2 ROX/fallback RO7 oscen=0x80 unique=211/256 changes=255/255 ones=2069/4096 (50.5%) first=0x013C last=0x3C3F min=0x0003 max=0xFFFF status_or=0x3F status_and=0x3D
I (4119) ulx3s_spi: RO characterize PASS
I (4129) ulx3s_spi: .....................
I (4129) ulx3s_spi: --------------------------------------------------------
I (4139) ulx3s_spi: RO characterize phase 2/3: src=3 S3 MIX/fallback, one-hot RO0-RO7
I (4149) ulx3s_spi: --------------------------------------------------------
I (4149) ulx3s_spi: RO characterize test: src=3 S3 MIX/fallback RO0 oscen=0x01
I (4159) ulx3s_spi: RO characterize test purpose: one-hot activity screen using 256 samples; this is not a frequency measurement
I (4169) ulx3s_spi: RO characterize setup: source=3 oscen=0x01; disabling sampling before config writes
I (4179) ulx3s_spi: RO characterize setup writes: R0=00, R1=0x03, R2=0x01, R3=0x00, R4=0x01, R0=0x01
I (4189) ulx3s_spi: RO characterize setup applied; settling for 10 ms before collecting samples...
I (4489) ulx3s_spi: src=3 S3 MIX/fallback RO0 oscen=0x01 unique=216/256 changes=254/255 ones=2103/4096 (51.3%) first=0x07FF last=0x3F30 min=0x0000 max=0xFFF0 status_or=0x3F status_and=0x3D
I (4499) ulx3s_spi: RO characterize PASS
I (4509) ulx3s_spi: .....................
I (4509) ulx3s_spi: RO characterize test: src=3 S3 MIX/fallback RO1 oscen=0x02
I (4519) ulx3s_spi: RO characterize test purpose: one-hot activity screen using 256 samples; this is not a frequency measurement
I (4529) ulx3s_spi: RO characterize setup: source=3 oscen=0x02; disabling sampling before config writes
I (4539) ulx3s_spi: RO characterize setup writes: R0=00, R1=0x03, R2=0x01, R3=0x00, R4=0x02, R0=0x01
I (4549) ulx3s_spi: RO characterize setup applied; settling for 10 ms before collecting samples...
I (4849) ulx3s_spi: src=3 S3 MIX/fallback RO1 oscen=0x02 unique=216/256 changes=255/255 ones=2011/4096 (49.1%) first=0xF9C3 last=0x180F min=0x0000 max=0xFFFF status_or=0x3F status_and=0x3D
I (4859) ulx3s_spi: RO characterize PASS
I (4869) ulx3s_spi: .....................
I (4869) ulx3s_spi: RO characterize test: src=3 S3 MIX/fallback RO2 oscen=0x04
I (4879) ulx3s_spi: RO characterize test purpose: one-hot activity screen using 256 samples; this is not a frequency measurement
I (4889) ulx3s_spi: RO characterize setup: source=3 oscen=0x04; disabling sampling before config writes
I (4899) ulx3s_spi: RO characterize setup writes: R0=00, R1=0x03, R2=0x01, R3=0x00, R4=0x04, R0=0x01
I (4909) ulx3s_spi: RO characterize setup applied; settling for 10 ms before collecting samples...
I (5209) ulx3s_spi: src=3 S3 MIX/fallback RO2 oscen=0x04 unique=217/256 changes=255/255 ones=2003/4096 (48.9%) first=0x3C0C last=0xC003 min=0x0003 max=0xFFFF status_or=0x3F status_and=0x3D
I (5219) ulx3s_spi: RO characterize PASS
I (5229) ulx3s_spi: .....................
I (5229) ulx3s_spi: RO characterize test: src=3 S3 MIX/fallback RO3 oscen=0x08
I (5239) ulx3s_spi: RO characterize test purpose: one-hot activity screen using 256 samples; this is not a frequency measurement
I (5249) ulx3s_spi: RO characterize setup: source=3 oscen=0x08; disabling sampling before config writes
I (5259) ulx3s_spi: RO characterize setup writes: R0=00, R1=0x03, R2=0x01, R3=0x00, R4=0x08, R0=0x01
I (5269) ulx3s_spi: RO characterize setup applied; settling for 10 ms before collecting samples...
I (5569) ulx3s_spi: src=3 S3 MIX/fallback RO3 oscen=0x08 unique=214/256 changes=255/255 ones=2177/4096 (53.1%) first=0x0CFC last=0xFCFC min=0x0000 max=0xFFFF status_or=0x3F status_and=0x3D
I (5579) ulx3s_spi: RO characterize PASS
I (5589) ulx3s_spi: .....................
I (5589) ulx3s_spi: RO characterize test: src=3 S3 MIX/fallback RO4 oscen=0x10
I (5599) ulx3s_spi: RO characterize test purpose: one-hot activity screen using 256 samples; this is not a frequency measurement
I (5609) ulx3s_spi: RO characterize setup: source=3 oscen=0x10; disabling sampling before config writes
I (5619) ulx3s_spi: RO characterize setup writes: R0=00, R1=0x03, R2=0x01, R3=0x00, R4=0x10, R0=0x01
I (5629) ulx3s_spi: RO characterize setup applied; settling for 10 ms before collecting samples...
I (5929) ulx3s_spi: src=3 S3 MIX/fallback RO4 oscen=0x10 unique=221/256 changes=255/255 ones=2031/4096 (49.6%) first=0xFF00 last=0x19CF min=0x0000 max=0xFFFF status_or=0x3F status_and=0x3D
I (5939) ulx3s_spi: RO characterize PASS
I (5949) ulx3s_spi: .....................
I (5949) ulx3s_spi: RO characterize test: src=3 S3 MIX/fallback RO5 oscen=0x20
I (5959) ulx3s_spi: RO characterize test purpose: one-hot activity screen using 256 samples; this is not a frequency measurement
I (5969) ulx3s_spi: RO characterize setup: source=3 oscen=0x20; disabling sampling before config writes
I (5979) ulx3s_spi: RO characterize setup writes: R0=00, R1=0x03, R2=0x01, R3=0x00, R4=0x20, R0=0x01
I (5989) ulx3s_spi: RO characterize setup applied; settling for 10 ms before collecting samples...
I (6289) ulx3s_spi: src=3 S3 MIX/fallback RO5 oscen=0x20 unique=222/256 changes=254/255 ones=2042/4096 (49.9%) first=0xFFF3 last=0x33F0 min=0x0000 max=0xFFFF status_or=0x3F status_and=0x3D
I (6299) ulx3s_spi: RO characterize PASS
I (6309) ulx3s_spi: .....................
I (6309) ulx3s_spi: RO characterize test: src=3 S3 MIX/fallback RO6 oscen=0x40
I (6319) ulx3s_spi: RO characterize test purpose: one-hot activity screen using 256 samples; this is not a frequency measurement
I (6329) ulx3s_spi: RO characterize setup: source=3 oscen=0x40; disabling sampling before config writes
I (6339) ulx3s_spi: RO characterize setup writes: R0=00, R1=0x03, R2=0x01, R3=0x00, R4=0x40, R0=0x01
I (6349) ulx3s_spi: RO characterize setup applied; settling for 10 ms before collecting samples...
I (6649) ulx3s_spi: src=3 S3 MIX/fallback RO6 oscen=0x40 unique=216/256 changes=254/255 ones=1988/4096 (48.5%) first=0x0C0C last=0x0F0F min=0x0000 max=0xFFF0 status_or=0x3F status_and=0x3D
I (6659) ulx3s_spi: RO characterize PASS
I (6669) ulx3s_spi: .....................
I (6669) ulx3s_spi: RO characterize test: src=3 S3 MIX/fallback RO7 oscen=0x80
I (6679) ulx3s_spi: RO characterize test purpose: one-hot activity screen using 256 samples; this is not a frequency measurement
I (6689) ulx3s_spi: RO characterize setup: source=3 oscen=0x80; disabling sampling before config writes
I (6699) ulx3s_spi: RO characterize setup writes: R0=00, R1=0x03, R2=0x01, R3=0x00, R4=0x80, R0=0x01
I (6709) ulx3s_spi: RO characterize setup applied; settling for 10 ms before collecting samples...
I (7009) ulx3s_spi: src=3 S3 MIX/fallback RO7 oscen=0x80 unique=213/256 changes=254/255 ones=2001/4096 (48.9%) first=0x00C3 last=0x0333 min=0x0003 max=0xFFFF status_or=0x3F status_and=0x3D
I (7019) ulx3s_spi: RO characterize PASS
I (7029) ulx3s_spi: .....................
I (7029) ulx3s_spi: --------------------------------------------------------
I (7039) ulx3s_spi: RO characterize phase 3/3: src=3 S3 MIX/fallback, all oscillator enables oscen=0xFF
I (7049) ulx3s_spi: --------------------------------------------------------
I (7059) ulx3s_spi: RO characterize test: src=3 S3 MIX/fallback ALL oscen=0xFF
I (7059) ulx3s_spi: RO characterize test purpose: one-hot activity screen using 256 samples; this is not a frequency measurement
I (7079) ulx3s_spi: RO characterize setup: source=3 oscen=0xFF; disabling sampling before config writes
I (7089) ulx3s_spi: RO characterize setup writes: R0=00, R1=0x03, R2=0x01, R3=0x00, R4=0xFF, R0=0x01
I (7099) ulx3s_spi: RO characterize setup applied; settling for 10 ms before collecting samples...
I (7399) ulx3s_spi: src=3 S3 MIX/fallback ALL oscen=0xFF unique=223/256 changes=255/255 ones=2051/4096 (50.1%) first=0x0FF0 last=0xF078 min=0x0003 max=0xFFFF status_or=0x3F status_and=0x3D
I (7409) ulx3s_spi: RO characterize PASS
I (7419) ulx3s_spi: .....................
I (7419) ulx3s_spi: RO characterize: restoring saved SPI config after characterization sweep
I (7429) ulx3s_spi: RO characterize: restore complete
I (7439) ulx3s_spi: RO characterize result: PASS, pass=17 fail=0
I (7439) main: --------------------------------------------------------
I (7449) main: Apply post-diagnostic SPI write policy
I (7459) main: --------------------------------------------------------
I (7459) main: SPI write mode: boot config once
I (7469) ulx3s_spi: --------------------------------------------------------
I (7479) ulx3s_spi: SPI boot config: apply safe defaults once
I (7479) ulx3s_spi: --------------------------------------------------------
I (7489) ulx3s_spi: SPI boot config purpose: leave firmware/demo in monitor-friendly defaults after diagnostics
I (7499) ulx3s_spi: SPI boot config writes: R0=0x00 R1=0x00 R2=0x10 R3=0x00 R4=0x01
I (7509) ulx3s_spi: SPI boot config: defaults written; dumping registers for confirmation
I (7519) ulx3s_spi: SPI regs: R0=00 R1=00 R2=10 R3=00 R4=01 R5=3C R6=33 R7=00
I (7529) ulx3s_spi: SPI regs: R8=08 R9=79 RA=00 RB=00 RC=F4 RD=8A RE=00 RF=00
I (7529) ulx3s_spi: raw=0x0033 status=0x3C src=0 div=0x10 mode=0x00 oscen=0x01 build=0x8A(FPGA TT DEMOBOARD) ui=0x08 uo=0x79 uio_in=0x00 uio_out=0x00 uio_oe=0xF4
I (7649) main: --------------------------------------------------------
I (7649) main: Run TRNG demo sequence
I (7649) main: --------------------------------------------------------
I (7649) main: Main step: run deterministic LFSR plus S1/S2/S3 live-source demonstrations
I (7659) main: --------------------------------------------------------
I (7669) main: TRNG deterministic LFSR test
I (7669) main: --------------------------------------------------------
I (7679) main: TRNG LFSR purpose: verify the deterministic test-mode sequence still responds through the normal read path
I (7689) main: TRNG LFSR expectation: samples should match the known firmware/RTL deterministic sequence
I (7709) main: lfsr test sample 00: raw=0x7F2E status=0x00
I (7709) main: lfsr test sample 01: raw=0x9F33 status=0x00
I (7719) main: lfsr test sample 02: raw=0xFC1C status=0x00
I (7719) main: lfsr test sample 03: raw=0x6F03 status=0x00
I (7729) main: lfsr test sample 04: raw=0x4B7D status=0x00
I (7739) main: lfsr test sample 05: raw=0x52C8 status=0x00
I (7739) main: lfsr test sample 06: raw=0xD6B7 status=0x00
I (7749) main: lfsr test sample 07: raw=0xEF2A status=0x00
I (7749) main: --------------------------------------------------------
I (7759) main: TRNG live source test
I (7759) main: --------------------------------------------------------
I (7769) main: TRNG live source: S1 RO0/fallback source=1 divider=0x01 oscen=0x01
I (7779) main: TRNG live purpose: confirm this source selection produces changing raw/status samples through the tt_trng API
I (7799) main: S1 RO0/fallback sample 00: raw=0x3C0F status=0x3C
I (7809) main: S1 RO0/fallback sample 01: raw=0x0006 status=0x3C
I (7819) main: S1 RO0/fallback sample 02: raw=0xE07F status=0x3C
I (7829) main: S1 RO0/fallback sample 03: raw=0x3300 status=0x3C
I (7839) main: S1 RO0/fallback sample 04: raw=0x0F0C status=0x3C
I (7849) main: S1 RO0/fallback sample 05: raw=0x6678 status=0x3C
I (7859) main: S1 RO0/fallback sample 06: raw=0x30CF status=0x3C
I (7869) main: S1 RO0/fallback sample 07: raw=0x33CF status=0x3C
I (7869) main: --------------------------------------------------------
I (7869) main: TRNG live source test
I (7869) main: --------------------------------------------------------
I (7879) main: TRNG live source: S2 ROX/fallback source=2 divider=0x01 oscen=0xFF
I (7889) main: TRNG live purpose: confirm this source selection produces changing raw/status samples through the tt_trng API
I (7909) main: S2 ROX/fallback sample 00: raw=0xF033 status=0x3C
I (7919) main: S2 ROX/fallback sample 01: raw=0xF3F0 status=0x3C
I (7929) main: S2 ROX/fallback sample 02: raw=0x30CC status=0x3C
I (7939) main: S2 ROX/fallback sample 03: raw=0x33FC status=0x3C
I (7949) main: S2 ROX/fallback sample 04: raw=0x03CC status=0x3C
I (7959) main: S2 ROX/fallback sample 05: raw=0x0C30 status=0x3C
I (7969) main: S2 ROX/fallback sample 06: raw=0x0187 status=0x3C
I (7979) main: S2 ROX/fallback sample 07: raw=0x667F status=0x3C
I (7979) main: --------------------------------------------------------
I (7979) main: TRNG live source test
I (7979) main: --------------------------------------------------------
I (7989) main: TRNG live source: S3 MIX/fallback source=3 divider=0x01 oscen=0xFF
I (7999) main: TRNG live purpose: confirm this source selection produces changing raw/status samples through the tt_trng API
I (8019) main: S3 MIX/fallback sample 00: raw=0x00CF status=0x3C
I (8029) main: S3 MIX/fallback sample 01: raw=0xCFFC status=0x3C
I (8039) main: S3 MIX/fallback sample 02: raw=0x30FC status=0x3C
I (8049) main: S3 MIX/fallback sample 03: raw=0x33F0 status=0x3C
I (8059) main: S3 MIX/fallback sample 04: raw=0x3FFF status=0x3C
I (8069) main: S3 MIX/fallback sample 05: raw=0xF0CF status=0x3C
I (8079) main: S3 MIX/fallback sample 06: raw=0x003C status=0x3C
I (8089) main: S3 MIX/fallback sample 07: raw=0xF0CF status=0x3C
I (8089) main: --------------------------------------------------------
I (8089) main: Run SPI pin snapshot demo
I (8089) main: --------------------------------------------------------
I (8099) main: Main step: read R8/R9/RA/RB/RC through tt_trng_read_pin_regs()
I (8109) main: --------------------------------------------------------
I (8119) main: TRNG SPI pin register test
I (8119) main: --------------------------------------------------------
I (8129) main: TRNG pin purpose: read SPI-visible snapshots R8/R9/RA/RB/RC and confirm the debug view of TT pins
I (8139) main: TRNG pin expectation: RC should normally be 0xF4 with SPI enabled; R8 should include UART RX idle high
I (8149) main: pin regs: R8 UI_IN=0x08 R9 UO_OUT=0xF9 RA UIO_IN=0xF0 RB UIO_OUT=0xF0 RC UIO_OE=0xF4
I (8159) main: uio view: observed=0xF0 drive_value=0xF0 drive_enable=0xF4
I (8169) main: --------------------------------------------------------
I (8169) main: Restore default SPI config before monitor loop
I (8179) main: --------------------------------------------------------
I (8189) main: Main step: reset R0-R4 to defaults and dump R0-RF before entering monitor loop
I (8199) ulx3s_spi: SPI regs: R0=00 R1=00 R2=10 R3=00 R4=01 R5=3C R6=CF R7=F0
I (8199) ulx3s_spi: SPI regs: R8=08 R9=F9 RA=F0 RB=F0 RC=F4 RD=8A RE=00 RF=00
I (8209) ulx3s_spi: raw=0xF0CF status=0x3C src=0 div=0x10 mode=0x00 oscen=0x01 build=0x8A(FPGA TT DEMOBOARD) ui=0x08 uo=0xF9 uio_in=0xF0 uio_out=0xF0 uio_oe=0xF4
I (8229) ulx3s_spi: SPI regs: R0=00 R1=00 R2=10 R3=00 R4=01 R5=3C R6=CF R7=F0
I (8239) ulx3s_spi: SPI regs: R8=08 R9=F9 RA=F0 RB=F0 RC=F4 RD=8A RE=00 RF=00
I (8239) ulx3s_spi: raw=0xF0CF status=0x3C src=0 div=0x10 mode=0x00 oscen=0x01 build=0x8A(FPGA TT DEMOBOARD) ui=0x08 uo=0xF9 uio_in=0xF0 uio_out=0xF0 uio_oe=0xF4
I (14259) ulx3s_spi: SPI regs: R0=00 R1=00 R2=00 R3=00 R4=00 R5=00 R6=00 R7=00
I (14259) ulx3s_spi: SPI regs: R8=00 R9=00 RA=00 RB=00 RC=00 RD=00 RE=00 RF=00
I (14259) ulx3s_spi: raw=0x0000 status=0x00 src=0 div=0x00 mode=0x00 oscen=0x00 build=0x00(UNKNOWN) ui=0x00 uo=0x00 uio_in=0x00 uio_out=0x00 uio_oe=0x00
I (17279) ulx3s_spi: SPI regs: R0=00 R1=00 R2=10 R3=00 R4=01 R5=04 R6=00 R7=00
I (17279) ulx3s_spi: SPI regs: R8=08 R9=18 RA=00 RB=00 RC=F4 RD=8A RE=00 RF=00
I (17279) ulx3s_spi: raw=0x0000 status=0x04 src=0 div=0x10 mode=0x00 oscen=0x01 build=0x8A(FPGA TT DEMOBOARD) ui=0x08 uo=0x18 uio_in=0x00 uio_out=0x00 uio_oe=0xF4
I (18299) ulx3s_spi: SPI regs: R0=FF R1=FF R2=FF R3=FF R4=FF R5=FF R6=FF R7=FF
I (18299) ulx3s_spi: SPI regs: R8=FF R9=FF RA=FF RB=FF RC=FF RD=FF RE=FF RF=FF
I (18299) ulx3s_spi: raw=0xFFFF status=0xFF src=255 div=0xFF mode=0xFF oscen=0xFF build=0xFF(UNRECOGNIZED) ui=0xFF uo=0xFF uio_in=0xFF uio_out=0xFF uio_oe=0xFF
I (20319) ulx3s_spi: SPI regs: R0=00 R1=00 R2=10 R3=00 R4=01 R5=04 R6=00 R7=00
I (20319) ulx3s_spi: SPI regs: R8=08 R9=18 RA=00 RB=00 RC=F4 RD=8A RE=00 RF=00
I (20319) ulx3s_spi: raw=0x0000 status=0x04 src=0 div=0x10 mode=0x00 oscen=0x01 build=0x8A(FPGA TT DEMOBOARD) ui=0x08 uo=0x18 uio_in=0x00 uio_out=0x00 uio_oe=0xF4
I (23339) ulx3s_spi: SPI regs: R0=06 R1=00 R2=10 R3=00 R4=01 R5=00 R6=00 R7=00
I (23339) ulx3s_spi: SPI regs: R8=08 R9=10 RA=00 RB=00 RC=F4 RD=8A RE=00 RF=00
I (23339) ulx3s_spi: raw=0x0000 status=0x00 src=0 div=0x10 mode=0x00 oscen=0x01 build=0x8A(FPGA TT DEMOBOARD) ui=0x08 uo=0x10 uio_in=0x00 uio_out=0x00 uio_oe=0xF4
I (24359) ulx3s_spi: SPI regs: R0=06 R1=00 R2=2A R3=5C R4=0F R5=00 R6=00 R7=00
I (24359) ulx3s_spi: SPI regs: R8=08 R9=10 RA=00 RB=00 RC=F4 RD=8A RE=00 RF=00
I (24359) ulx3s_spi: raw=0x0000 status=0x00 src=0 div=0x2A mode=0x5C oscen=0x0F build=0x8A(FPGA TT DEMOBOARD) ui=0x08 uo=0x10 uio_in=0x00 uio_out=0x00 uio_oe=0xF4
I (25379) ulx3s_spi: SPI regs: R0=00 R1=00 R2=10 R3=00 R4=01 R5=04 R6=00 R7=00
I (25379) ulx3s_spi: SPI regs: R8=08 R9=18 RA=00 RB=00 RC=F4 RD=8A RE=00 RF=00
I (25379) ulx3s_spi: raw=0x0000 status=0x04 src=0 div=0x10 mode=0x00 oscen=0x01 build=0x8A(FPGA TT DEMOBOARD) ui=0x08 uo=0x18 uio_in=0x00 uio_out=0x00 uio_oe=0xF4
I (26399) ulx3s_spi: SPI regs: R0=06 R1=00 R2=2A R3=00 R4=01 R5=00 R6=00 R7=00
I (26399) ulx3s_spi: SPI regs: R8=08 R9=10 RA=00 RB=00 RC=F4 RD=8A RE=00 RF=00
I (26399) ulx3s_spi: raw=0x0000 status=0x00 src=0 div=0x2A mode=0x00 oscen=0x01 build=0x8A(FPGA TT DEMOBOARD) ui=0x08 uo=0x10 uio_in=0x00 uio_out=0x00 uio_oe=0xF4
I (27419) ulx3s_spi: SPI regs: R0=06 R1=00 R2=2A R3=5C R4=0F R5=00 R6=00 R7=00
I (27419) ulx3s_spi: SPI regs: R8=08 R9=10 RA=00 RB=00 RC=F4 RD=8A RE=00 RF=00
I (27419) ulx3s_spi: raw=0x0000 status=0x00 src=0 div=0x2A mode=0x5C oscen=0x0F build=0x8A(FPGA TT DEMOBOARD) ui=0x08 uo=0x10 uio_in=0x00 uio_out=0x00 uio_oe=0xF4
I (28439) ulx3s_spi: SPI regs: R0=00 R1=00 R2=10 R3=00 R4=00 R5=00 R6=00 R7=00
I (28439) ulx3s_spi: SPI regs: R8=08 R9=10 RA=00 RB=00 RC=F4 RD=8A RE=00 RF=00
I (28439) ulx3s_spi: raw=0x0000 status=0x00 src=0 div=0x10 mode=0x00 oscen=0x00 build=0x8A(FPGA TT DEMOBOARD) ui=0x08 uo=0x10 uio_in=0x00 uio_out=0x00 uio_oe=0xF4
I (29459) ulx3s_spi: SPI regs: R0=00 R1=01 R2=01 R3=00 R4=01 R5=04 R6=00 R7=00
I (29459) ulx3s_spi: SPI regs: R8=08 R9=18 RA=00 RB=00 RC=F4 RD=8A RE=00 RF=00
I (29459) ulx3s_spi: raw=0x0000 status=0x04 src=1 div=0x01 mode=0x00 oscen=0x01 build=0x8A(FPGA TT DEMOBOARD) ui=0x08 uo=0x18 uio_in=0x00 uio_out=0x00 uio_oe=0xF4
I (30479) ulx3s_spi: SPI regs: R0=01 R1=03 R2=0F R3=00 R4=FF R5=3D R6=7E R7=33
I (30479) ulx3s_spi: SPI regs: R8=08 R9=7B RA=70 RB=C0 RC=F4 RD=8A RE=00 RF=00
I (30479) ulx3s_spi: raw=0x337E status=0x3D src=3 div=0x0F mode=0x00 oscen=0xFF build=0x8A(FPGA TT DEMOBOARD) ui=0x08 uo=0x7B uio_in=0x70 uio_out=0xC0 uio_oe=0xF4
I (31499) ulx3s_spi: SPI regs: R0=01 R1=03 R2=0F R3=00 R4=FF R5=3D R6=03 R7=C3
I (31499) ulx3s_spi: SPI regs: R8=08 R9=7B RA=F0 RB=00 RC=F4 RD=8A RE=00 RF=00
I (31499) ulx3s_spi: raw=0xC303 status=0x3D src=3 div=0x0F mode=0x00 oscen=0xFF build=0x8A(FPGA TT DEMOBOARD) ui=0x08 uo=0x7B uio_in=0xF0 uio_out=0x00 uio_oe=0xF4
I (32519) ulx3s_spi: SPI regs: R0=00 R1=00 R2=01 R3=00 R4=00 R5=38 R6=92 R7=BB
I (32519) ulx3s_spi: SPI regs: R8=08 R9=50 RA=B0 RB=B0 RC=F4 RD=8A RE=00 RF=00
I (32519) ulx3s_spi: raw=0xBB92 status=0x38 src=0 div=0x01 mode=0x00 oscen=0x00 build=0x8A(FPGA TT DEMOBOARD) ui=0x08 uo=0x50 uio_in=0xB0 uio_out=0xB0 uio_oe=0xF4
I (33539) ulx3s_spi: SPI regs: R0=01 R1=00 R2=01 R3=00 R4=00 R5=3B R6=7F R7=86
I (33539) ulx3s_spi: SPI regs: R8=08 R9=12 RA=10 RB=50 RC=F4 RD=8A RE=00 RF=00
I (33539) ulx3s_spi: raw=0x867F status=0x3B src=0 div=0x01 mode=0x00 oscen=0x00 build=0x8A(FPGA TT DEMOBOARD) ui=0x08 uo=0x12 uio_in=0x10 uio_out=0x50 uio_oe=0xF4
I (34559) ulx3s_spi: SPI regs: R0=00 R1=01 R2=01 R3=00 R4=01 R5=3C R6=F0 R7=00
I (34559) ulx3s_spi: SPI regs: R8=08 R9=18 RA=00 RB=00 RC=F4 RD=8A RE=00 RF=00
I (34559) ulx3s_spi: raw=0x00F0 status=0x3C src=1 div=0x01 mode=0x00 oscen=0x01 build=0x8A(FPGA TT DEMOBOARD) ui=0x08 uo=0x18 uio_in=0x00 uio_out=0x00 uio_oe=0xF4
I (35579) ulx3s_spi: SPI regs: R0=01 R1=01 R2=01 R3=00 R4=01 R5=3D R6=61 R7=F3
I (35579) ulx3s_spi: SPI regs: R8=08 R9=3F RA=00 RB=E0 RC=F4 RD=8A RE=00 RF=00
I (35579) ulx3s_spi: raw=0xF361 status=0x3D src=1 div=0x01 mode=0x00 oscen=0x01 build=0x8A(FPGA TT DEMOBOARD) ui=0x08 uo=0x3F uio_in=0x00 uio_out=0xE0 uio_oe=0xF4
I (36599) ulx3s_spi: SPI regs: R0=00 R1=02 R2=01 R3=00 R4=FF R5=3C R6=F0 R7=33
I (36599) ulx3s_spi: SPI regs: R8=00 R9=18 RA=30 RB=30 RC=F4 RD=8A RE=00 RF=00
I (36599) ulx3s_spi: raw=0x33F0 status=0x3C src=2 div=0x01 mode=0x00 oscen=0xFF build=0x8A(FPGA TT DEMOBOARD) ui=0x00 uo=0x18 uio_in=0x30 uio_out=0x30 uio_oe=0xF4
I (37619) ulx3s_spi: SPI regs: R0=00 R1=02 R2=01 R3=00 R4=FF R5=3C R6=3C R7=F0
I (37619) ulx3s_spi: SPI regs: R8=08 R9=98 RA=F0 RB=F0 RC=F4 RD=8A RE=00 RF=00
I (37619) ulx3s_spi: raw=0xF03C status=0x3C src=2 div=0x01 mode=0x00 oscen=0xFF build=0x8A(FPGA TT DEMOBOARD) ui=0x08 uo=0x98 uio_in=0xF0 uio_out=0xF0 uio_oe=0xF4
I (38639) ulx3s_spi: SPI regs: R0=00 R1=03 R2=01 R3=00 R4=FF R5=3C R6=7F R7=80
I (38639) ulx3s_spi: SPI regs: R8=08 R9=F9 RA=80 RB=80 RC=F4 RD=8A RE=00 RF=00
I (38639) ulx3s_spi: raw=0x807F status=0x3C src=3 div=0x01 mode=0x00 oscen=0xFF build=0x8A(FPGA TT DEMOBOARD) ui=0x08 uo=0xF9 uio_in=0x80 uio_out=0x80 uio_oe=0xF4
I (39659) ulx3s_spi: SPI regs: R0=00 R1=03 R2=01 R3=00 R4=FF R5=3C R6=99 R7=F9
I (39659) ulx3s_spi: SPI regs: R8=08 R9=39 RA=F0 RB=F0 RC=F4 RD=8A RE=00 RF=00
I (39659) ulx3s_spi: raw=0xF999 status=0x3C src=3 div=0x01 mode=0x00 oscen=0xFF build=0x8A(FPGA TT DEMOBOARD) ui=0x08 uo=0x39 uio_in=0xF0 uio_out=0xF0 uio_oe=0xF4
I (40679) ulx3s_spi: SPI regs: R0=02 R1=00 R2=01 R3=00 R4=00 R5=00 R6=03 R7=00
I (40679) ulx3s_spi: SPI regs: R8=08 R9=71 RA=00 RB=00 RC=F4 RD=8A RE=00 RF=00
I (40679) ulx3s_spi: raw=0x0003 status=0x00 src=0 div=0x01 mode=0x00 oscen=0x00 build=0x8A(FPGA TT DEMOBOARD) ui=0x08 uo=0x71 uio_in=0x00 uio_out=0x00 uio_oe=0xF4
I (41699) ulx3s_spi: SPI regs: R0=00 R1=00 R2=01 R3=00 R4=00 R5=00 R6=F2 R7=07
I (41699) ulx3s_spi: SPI regs: R8=08 R9=50 RA=00 RB=00 RC=F4 RD=8A RE=00 RF=00
I (41699) ulx3s_spi: raw=0x07F2 status=0x00 src=0 div=0x01 mode=0x00 oscen=0x00 build=0x8A(FPGA TT DEMOBOARD) ui=0x08 uo=0x50 uio_in=0x00 uio_out=0x00 uio_oe=0xF4
I (42719) ulx3s_spi: SPI regs: R0=02 R1=00 R2=01 R3=00 R4=00 R5=00 R6=E9 R7=F2
I (42719) ulx3s_spi: SPI regs: R8=08 R9=31 RA=F0 RB=F0 RC=F4 RD=8A RE=00 RF=00
I (42719) ulx3s_spi: raw=0xF2E9 status=0x00 src=0 div=0x01 mode=0x00 oscen=0x00 build=0x8A(FPGA TT DEMOBOARD) ui=0x08 uo=0x31 uio_in=0xF0 uio_out=0xF0 uio_oe=0xF4
I (43739) ulx3s_spi: SPI regs: R0=02 R1=00 R2=01 R3=00 R4=00 R5=00 R6=E6 R7=D3
I (43739) ulx3s_spi: SPI regs: R8=08 R9=C0 RA=D0 RB=D0 RC=F4 RD=8A RE=00 RF=00
I (43739) ulx3s_spi: raw=0xD3E6 status=0x00 src=0 div=0x01 mode=0x00 oscen=0x00 build=0x8A(FPGA TT DEMOBOARD) ui=0x08 uo=0xC0 uio_in=0xD0 uio_out=0xD0 uio_oe=0xF4
I (44759) ulx3s_spi: SPI regs: R0=02 R1=00 R2=01 R3=00 R4=00 R5=00 R6=7F R7=E6
I (44759) ulx3s_spi: SPI regs: R8=08 R9=F1 RA=E0 RB=E0 RC=F4 RD=8A RE=00 RF=00
I (44759) ulx3s_spi: raw=0xE67F status=0x00 src=0 div=0x01 mode=0x00 oscen=0x00 build=0x8A(FPGA TT DEMOBOARD) ui=0x08 uo=0xF1 uio_in=0xE0 uio_out=0xE0 uio_oe=0xF4
I (45779) ulx3s_spi: SPI regs: R0=02 R1=00 R2=01 R3=00 R4=00 R5=00 R6=07 R7=FF
I (45779) ulx3s_spi: SPI regs: R8=08 R9=F1 RA=F0 RB=F0 RC=F4 RD=8A RE=00 RF=00
I (45779) ulx3s_spi: raw=0xFF07 status=0x00 src=0 div=0x01 mode=0x00 oscen=0x00 build=0x8A(FPGA TT DEMOBOARD) ui=0x08 uo=0xF1 uio_in=0xF0 uio_out=0xF0 uio_oe=0xF4
I (46799) ulx3s_spi: SPI regs: R0=02 R1=00 R2=01 R3=00 R4=00 R5=00 R6=1B R7=07
I (46799) ulx3s_spi: SPI regs: R8=08 R9=71 RA=00 RB=00 RC=F4 RD=8A RE=00 RF=00
I (46799) ulx3s_spi: raw=0x071B status=0x00 src=0 div=0x01 mode=0x00 oscen=0x00 build=0x8A(FPGA TT DEMOBOARD) ui=0x08 uo=0x71 uio_in=0x00 uio_out=0x00 uio_oe=0xF4
I (47819) ulx3s_spi: SPI regs: R0=02 R1=00 R2=01 R3=00 R4=00 R5=00 R6=81 R7=37
I (47819) ulx3s_spi: SPI regs: R8=08 R9=31 RA=30 RB=30 RC=F4 RD=8A RE=00 RF=00
I (47819) ulx3s_spi: raw=0x3781 status=0x00 src=0 div=0x01 mode=0x00 oscen=0x00 build=0x8A(FPGA TT DEMOBOARD) ui=0x08 uo=0x31 uio_in=0x30 uio_out=0x30 uio_oe=0xF4
I (48839) ulx3s_spi: SPI regs: R0=02 R1=00 R2=01 R3=00 R4=00 R5=00 R6=A5 R7=81
I (48839) ulx3s_spi: SPI regs: R8=08 R9=B1 RA=80 RB=80 RC=F4 RD=8A RE=00 RF=00
I (48839) ulx3s_spi: raw=0x81A5 status=0x00 src=0 div=0x01 mode=0x00 oscen=0x00 build=0x8A(FPGA TT DEMOBOARD) ui=0x08 uo=0xB1 uio_in=0x80 uio_out=0x80 uio_oe=0xF4
I (49859) ulx3s_spi: SPI regs: R0=02 R1=00 R2=01 R3=00 R4=00 R5=00 R6=7D R7=4B
I (49859) ulx3s_spi: SPI regs: R8=08 R9=A1 RA=40 RB=40 RC=F4 RD=8A RE=00 RF=00
I (49859) ulx3s_spi: raw=0x4B7D status=0x00 src=0 div=0x01 mode=0x00 oscen=0x00 build=0x8A(FPGA TT DEMOBOARD) ui=0x08 uo=0xA1 uio_in=0x40 uio_out=0x40 uio_oe=0xF4
I (50879) ulx3s_spi: SPI regs: R0=02 R1=00 R2=01 R3=00 R4=00 R5=00 R6=52 R7=7D
I (50879) ulx3s_spi: SPI regs: R8=08 R9=50 RA=70 RB=70 RC=F4 RD=8A RE=00 RF=00
I (50879) ulx3s_spi: raw=0x7D52 status=0x00 src=0 div=0x01 mode=0x00 oscen=0x00 build=0x8A(FPGA TT DEMOBOARD) ui=0x08 uo=0x50 uio_in=0x70 uio_out=0x70 uio_oe=0xF4
I (51899) ulx3s_spi: SPI regs: R0=00 R1=00 R2=01 R3=00 R4=00 R5=00 R6=C8 R7=52
I (51899) ulx3s_spi: SPI regs: R8=08 R9=10 RA=50 RB=50 RC=F4 RD=8A RE=00 RF=00
I (51899) ulx3s_spi: raw=0x52C8 status=0x00 src=0 div=0x01 mode=0x00 oscen=0x00 build=0x8A(FPGA TT DEMOBOARD) ui=0x08 uo=0x10 uio_in=0x50 uio_out=0x50 uio_oe=0xF4
I (52919) ulx3s_spi: SPI regs: R0=02 R1=00 R2=01 R3=00 R4=00 R5=00 R6=AD R7=91
I (52919) ulx3s_spi: SPI regs: R8=08 R9=B1 RA=90 RB=90 RC=F4 RD=8A RE=00 RF=00
I (52919) ulx3s_spi: raw=0x91AD status=0x00 src=0 div=0x01 mode=0x00 oscen=0x00 build=0x8A(FPGA TT DEMOBOARD) ui=0x08 uo=0xB1 uio_in=0x90 uio_out=0x90 uio_oe=0xF4
I (53939) ulx3s_spi: SPI regs: R0=00 R1=00 R2=01 R3=00 R4=00 R5=00 R6=B7 R7=D6
I (53939) ulx3s_spi: SPI regs: R8=08 R9=F1 RA=D0 RB=D0 RC=F4 RD=8A RE=00 RF=00
I (53939) ulx3s_spi: raw=0xD6B7 status=0x00 src=0 div=0x01 mode=0x00 oscen=0x00 build=0x8A(FPGA TT DEMOBOARD) ui=0x08 uo=0xF1 uio_in=0xD0 uio_out=0xD0 uio_oe=0xF4
I (54959) ulx3s_spi: SPI regs: R0=02 R1=00 R2=01 R3=00 R4=00 R5=00 R6=BC R7=DF
I (54959) ulx3s_spi: SPI regs: R8=08 R9=90 RA=D0 RB=D0 RC=F4 RD=8A RE=00 RF=00
I (54959) ulx3s_spi: raw=0xDFBC status=0x00 src=0 div=0x01 mode=0x00 oscen=0x00 build=0x8A(FPGA TT DEMOBOARD) ui=0x08 uo=0x90 uio_in=0xD0 uio_out=0xD0 uio_oe=0xF4
I (55979) ulx3s_spi: SPI regs: R0=04 R1=00 R2=01 R3=00 R4=00 R5=00 R6=00 R7=00
I (55979) ulx3s_spi: SPI regs: R8=08 R9=10 RA=00 RB=00 RC=F4 RD=8A RE=00 RF=00
I (55979) ulx3s_spi: raw=0x0000 status=0x00 src=0 div=0x01 mode=0x00 oscen=0x00 build=0x8A(FPGA TT DEMOBOARD) ui=0x08 uo=0x10 uio_in=0x00 uio_out=0x00 uio_oe=0xF4
I (56999) ulx3s_spi: SPI regs: R0=00 R1=00 R2=01 R3=00 R4=00 R5=00 R6=3F R7=00
I (56999) ulx3s_spi: SPI regs: R8=08 R9=F1 RA=00 RB=00 RC=F4 RD=8A RE=00 RF=00
I (56999) ulx3s_spi: raw=0x003F status=0x00 src=0 div=0x01 mode=0x00 oscen=0x00 build=0x8A(FPGA TT DEMOBOARD) ui=0x08 uo=0xF1 uio_in=0x00 uio_out=0x00 uio_oe=0xF4
I (58019) ulx3s_spi: SPI regs: R0=00 R1=00 R2=01 R3=00 R4=00 R5=00 R6=2E R7=7F
I (58019) ulx3s_spi: SPI regs: R8=08 R9=D0 RA=70 RB=70 RC=F4 RD=8A RE=00 RF=00
I (58019) ulx3s_spi: raw=0x7F2E status=0x00 src=0 div=0x01 mode=0x00 oscen=0x00 build=0x8A(FPGA TT DEMOBOARD) ui=0x08 uo=0xD0 uio_in=0x70 uio_out=0x70 uio_oe=0xF4
I (59039) ulx3s_spi: SPI regs: R0=00 R1=00 R2=01 R3=00 R4=00 R5=00 R6=9F R7=2E
I (59039) ulx3s_spi: SPI regs: R8=08 R9=F1 RA=20 RB=20 RC=F4 RD=8A RE=00 RF=00
I (59039) ulx3s_spi: raw=0x2E9F status=0x00 src=0 div=0x01 mode=0x00 oscen=0x00 build=0x8A(FPGA TT DEMOBOARD) ui=0x08 uo=0xF1 uio_in=0x20 uio_out=0x20 uio_oe=0xF4
I (60059) ulx3s_spi: SPI regs: R0=00 R1=00 R2=01 R3=00 R4=00 R5=00 R6=33 R7=9F
I (60059) ulx3s_spi: SPI regs: R8=08 R9=71 RA=90 RB=90 RC=F4 RD=8A RE=00 RF=00
I (60059) ulx3s_spi: raw=0x9F33 status=0x00 src=0 div=0x01 mode=0x00 oscen=0x00 build=0x8A(FPGA TT DEMOBOARD) ui=0x08 uo=0x71 uio_in=0x90 uio_out=0x90 uio_oe=0xF4
I (61079) ulx3s_spi: SPI regs: R0=00 R1=00 R2=01 R3=00 R4=00 R5=00 R6=F8 R7=67
I (61079) ulx3s_spi: SPI regs: R8=08 R9=10 RA=60 RB=60 RC=F4 RD=8A RE=00 RF=00
I (61079) ulx3s_spi: raw=0x67F8 status=0x00 src=0 div=0x01 mode=0x00 oscen=0x00 build=0x8A(FPGA TT DEMOBOARD) ui=0x08 uo=0x10 uio_in=0x60 uio_out=0x60 uio_oe=0xF4
I (62099) ulx3s_spi: SPI regs: R0=00 R1=00 R2=01 R3=00 R4=00 R5=00 R6=38 R7=F8
I (62099) ulx3s_spi: SPI regs: R8=08 R9=10 RA=F0 RB=F0 RC=F4 RD=8A RE=00 RF=00
I (62099) ulx3s_spi: raw=0xF838 status=0x00 src=0 div=0x01 mode=0x00 oscen=0x00 build=0x8A(FPGA TT DEMOBOARD) ui=0x08 uo=0x10 uio_in=0xF0 uio_out=0xF0 uio_oe=0xF4
I (63119) ulx3s_spi: SPI regs: R0=00 R1=00 R2=01 R3=00 R4=00 R5=00 R6=BC R7=71
I (63119) ulx3s_spi: SPI regs: R8=08 R9=90 RA=70 RB=70 RC=F4 RD=8A RE=00 RF=00
I (63119) ulx3s_spi: raw=0x71BC status=0x00 src=0 div=0x01 mode=0x00 oscen=0x00 build=0x8A(FPGA TT DEMOBOARD) ui=0x08 uo=0x90 uio_in=0x70 uio_out=0x70 uio_oe=0xF4
I (64139) ulx3s_spi: SPI regs: R0=02 R1=00 R2=01 R3=00 R4=00 R5=00 R6=0D R7=BC
I (64139) ulx3s_spi: SPI regs: R8=08 R9=B1 RA=B0 RB=B0 RC=F4 RD=8A RE=00 RF=00
I (64139) ulx3s_spi: raw=0xBC0D status=0x00 src=0 div=0x01 mode=0x00 oscen=0x00 build=0x8A(FPGA TT DEMOBOARD) ui=0x08 uo=0xB1 uio_in=0xB0 uio_out=0xB0 uio_oe=0xF4
I (65159) ulx3s_spi: SPI regs: R0=00 R1=00 R2=01 R3=00 R4=00 R5=00 R6=5B R7=1A
I (65159) ulx3s_spi: SPI regs: R8=08 R9=71 RA=10 RB=10 RC=F4 RD=8A RE=00 RF=00
I (65159) ulx3s_spi: raw=0x1A5B status=0x00 src=0 div=0x01 mode=0x00 oscen=0x00 build=0x8A(FPGA TT DEMOBOARD) ui=0x08 uo=0x71 uio_in=0x10 uio_out=0x10 uio_oe=0xF4
I (66179) ulx3s_spi: SPI regs: R0=02 R1=00 R2=01 R3=00 R4=00 R5=00 R6=EA R7=5B
I (66179) ulx3s_spi: SPI regs: R8=08 R9=50 RA=50 RB=50 RC=F4 RD=8A RE=00 RF=00
I (66179) ulx3s_spi: raw=0x5BEA status=0x00 src=0 div=0x01 mode=0x00 oscen=0x00 build=0x8A(FPGA TT DEMOBOARD) ui=0x08 uo=0x50 uio_in=0x50 uio_out=0x50 uio_oe=0xF4
I (67199) ulx3s_spi: SPI regs: R0=00 R1=00 R2=01 R3=00 R4=00 R5=00 R6=2C R7=D5
I (67199) ulx3s_spi: SPI regs: R8=08 R9=90 RA=D0 RB=D0 RC=F4 RD=8A RE=00 RF=00
I (67199) ulx3s_spi: raw=0xD52C status=0x00 src=0 div=0x01 mode=0x00 oscen=0x00 build=0x8A(FPGA TT DEMOBOARD) ui=0x08 uo=0x90 uio_in=0xD0 uio_out=0xD0 uio_oe=0xF4
I (68219) ulx3s_spi: SPI regs: R0=02 R1=00 R2=01 R3=00 R4=00 R5=00 R6=8D R7=2C
I (68219) ulx3s_spi: SPI regs: R8=08 R9=B1 RA=20 RB=20 RC=F4 RD=8A RE=00 RF=00
I (68219) ulx3s_spi: raw=0x2C8D status=0x00 src=0 div=0x01 mode=0x00 oscen=0x00 build=0x8A(FPGA TT DEMOBOARD) ui=0x08 uo=0xB1 uio_in=0x20 uio_out=0x20 uio_oe=0xF4
I (69239) ulx3s_spi: SPI regs: R0=00 R1=00 R2=01 R3=00 R4=00 R5=00 R6=D6 R7=1A
I (69239) ulx3s_spi: SPI regs: R8=08 R9=D0 RA=10 RB=10 RC=F4 RD=8A RE=00 RF=00
I (69239) ulx3s_spi: raw=0x1AD6 status=0x00 src=0 div=0x01 mode=0x00 oscen=0x00 build=0x8A(FPGA TT DEMOBOARD) ui=0x08 uo=0xD0 uio_in=0x10 uio_out=0x10 uio_oe=0xF4
I (70259) ulx3s_spi: SPI regs: R0=02 R1=00 R2=01 R3=00 R4=00 R5=00 R6=FD R7=D6
I (70259) ulx3s_spi: SPI regs: R8=08 R9=B1 RA=D0 RB=D0 RC=F4 RD=8A RE=00 RF=00
I (70259) ulx3s_spi: raw=0xD6FD status=0x00 src=0 div=0x01 mode=0x00 oscen=0x00 build=0x8A(FPGA TT DEMOBOARD) ui=0x08 uo=0xB1 uio_in=0xD0 uio_out=0xD0 uio_oe=0xF4
I (71279) ulx3s_spi: SPI regs: R0=00 R1=00 R2=01 R3=00 R4=00 R5=00 R6=CA R7=FB
I (71279) ulx3s_spi: SPI regs: R8=08 R9=50 RA=F0 RB=F0 RC=F4 RD=8A RE=00 RF=00
I (71279) ulx3s_spi: raw=0xFBCA status=0x00 src=0 div=0x01 mode=0x00 oscen=0x00 build=0x8A(FPGA TT DEMOBOARD) ui=0x08 uo=0x50 uio_in=0xF0 uio_out=0xF0 uio_oe=0xF4
I (72299) ulx3s_spi: SPI regs: R0=00 R1=00 R2=10 R3=00 R4=01 R5=04 R6=2A R7=EF
I (72299) ulx3s_spi: SPI regs: R8=08 R9=58 RA=E0 RB=E0 RC=F4 RD=8A RE=00 RF=00
I (72299) ulx3s_spi: raw=0xEF2A status=0x04 src=0 div=0x10 mode=0x00 oscen=0x01 build=0x8A(FPGA TT DEMOBOARD) ui=0x08 uo=0x58 uio_in=0xE0 uio_out=0xE0 uio_oe=0xF4
I (73319) ulx3s_spi: SPI regs: R0=06 R1=00 R2=10 R3=00 R4=01 R5=00 R6=00 R7=00
I (73319) ulx3s_spi: SPI regs: R8=08 R9=10 RA=00 RB=00 RC=F4 RD=8A RE=00 RF=00
I (73319) ulx3s_spi: raw=0x0000 status=0x00 src=0 div=0x10 mode=0x00 oscen=0x01 build=0x8A(FPGA TT DEMOBOARD) ui=0x08 uo=0x10 uio_in=0x00 uio_out=0x00 uio_oe=0xF4
I (74339) ulx3s_spi: SPI regs: R0=06 R1=00 R2=2A R3=5C R4=0F R5=00 R6=00 R7=00
I (74339) ulx3s_spi: SPI regs: R8=08 R9=10 RA=00 RB=00 RC=F4 RD=8A RE=00 RF=00
I (74339) ulx3s_spi: raw=0x0000 status=0x00 src=0 div=0x2A mode=0x5C oscen=0x0F build=0x8A(FPGA TT DEMOBOARD) ui=0x08 uo=0x10 uio_in=0x00 uio_out=0x00 uio_oe=0xF4
I (75359) ulx3s_spi: SPI regs: R0=00 R1=00 R2=10 R3=00 R4=01 R5=04 R6=00 R7=00
I (75359) ulx3s_spi: SPI regs: R8=08 R9=18 RA=00 RB=00 RC=F4 RD=8A RE=00 RF=00
I (75359) ulx3s_spi: raw=0x0000 status=0x04 src=0 div=0x10 mode=0x00 oscen=0x01 build=0x8A(FPGA TT DEMOBOARD) ui=0x08 uo=0x18 uio_in=0x00 uio_out=0x00 uio_oe=0xF4


```
