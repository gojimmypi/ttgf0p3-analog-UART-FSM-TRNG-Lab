# Example ESP32 SPI Failure

When using the wrong SPI pis or the in the case of the FPGA board not being programmed:

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
I (107) esp_image: segment 2: paddr=0001d4b0 vaddr=3ffb0000 size=023dch (  9180) load
I (114) esp_image: segment 3: paddr=0001f894 vaddr=40080000 size=00784h (  1924) load
I (119) esp_image: segment 4: paddr=00020020 vaddr=400d0020 size=14c84h ( 85124) map
I (154) esp_image: segment 5: paddr=00034cac vaddr=40080784 size=0e1f4h ( 57844) load
I (184) boot: Loaded app from partition at offset 0x10000
I (184) boot: Disabling RNG early entropy source...
I (195) cpu_start: Multicore app
I (203) cpu_start: Pro cpu start user code
I (203) cpu_start: cpu freq: 160000000 Hz
I (203) app_init: Application information:
I (206) app_init: Project name:     ulx3s_esp32
I (211) app_init: App version:      1.0.3-62-gea62011-dirty
I (218) app_init: Compile time:     Jun 20 2026 09:48:02
I (224) app_init: ELF file SHA256:  507cfaf4c...
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
W (295) spi_flash: Detected size(4096k) larger than the size in the binary image header(2048k). Using the size in the binary imag                     e header.
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
I (519) ulx3s_spi: PIN_NUM_CS:     13
I (519) ulx3s_spi: PIN_NUM_MISO:   2
I (529) ulx3s_spi: PIN_NUM_MOSI:   15
I (529) ulx3s_spi: PIN_NUM_CLK:    14
I (529) ulx3s_spi: --------------------------------------------------------
I (539) main: --------------------------------------------------------
I (549) main: Run SPI register self-check
I (549) main: --------------------------------------------------------
I (559) main: Main step: validate R0-RF register map, pin snapshot registers, and active R6/R7 raw-change behavior
I (569) ulx3s_spi: --------------------------------------------------------
I (579) ulx3s_spi: SPI self-check: begin
I (579) ulx3s_spi: --------------------------------------------------------
I (589) ulx3s_spi: SPI self-check purpose: verify R0-RF SPI register map, expected defaults, pin snapshots, and active raw moveme                     nt
I (599) ulx3s_spi: SPI self-check expected defaults after reset: R0=0x00 R1=0x00 R2=0x10 R3=0x00 R4=0x01
I (609) ulx3s_spi: SPI self-check expected R5 status: cold/reset 0x04 is allowed before TRNG warm-up; warmed/default is 0x3C
I (629) ulx3s_spi: SPI self-check expected BIG16 registers: R8 has UART RX idle bit set, RC=0xF4, RD=ASIC GF180 or ULX3S build ta                     rget, RE/RF=0x00
I (639) ulx3s_spi: --------------------------------------------------------
I (649) ulx3s_spi: SPI self-check: reset config registers to known defaults
I (659) ulx3s_spi: --------------------------------------------------------
I (659) ulx3s_spi: SPI self-check reset reason: ESP32 reset may not reset the FPGA register state
I (689) ulx3s_spi: --------------------------------------------------------
I (689) ulx3s_spi: SPI self-check: read R0-RF and compare register-map expectations
I (689) ulx3s_spi: --------------------------------------------------------
I (699) ulx3s_spi: SPI regs: R0=00 R1=00 R2=00 R3=00 R4=00 R5=00 R6=00 R7=00
I (709) ulx3s_spi: SPI regs: R8=00 R9=00 RA=00 RB=00 RC=00 RD=00 RE=00 RF=00
I (709) ulx3s_spi: raw=0x0000 status=0x00 src=0 div=0x00 mode=0x00 oscen=0x00 build=0x00(UNKNOWN) ui=0x00 uo=0x00 uio_in=0x00 uio                     _out=0x00 uio_oe=0x00
I (729) ulx3s_spi: SPI self-check step 1/3: compare stable registers and log dynamic pin snapshot registers
I (739) ulx3s_spi: SPI self-check PASS R0 CTRL: 00
I (739) ulx3s_spi: SPI self-check PASS R1 SRC: 00
E (749) ulx3s_spi: SPI self-check FAIL R2 DIV: expected 10, actual 00
I (759) ulx3s_spi: SPI self-check PASS R3 MODE: 00
E (759) ulx3s_spi: SPI self-check FAIL R4 OSCEN: expected 01, actual 00
E (769) ulx3s_spi: SPI self-check FAIL R8 UI_IN UART_RX_IDLE: expected mask 08 value 08, actual 00
I (779) ulx3s_spi: SPI self-check INFO R9 UO_OUT: 00
I (779) ulx3s_spi: SPI self-check INFO RA UIO_IN: 00
I (789) ulx3s_spi: SPI self-check INFO RB UIO_OUT: 00
E (799) ulx3s_spi: SPI self-check FAIL RC UIO_OE: expected F4, actual 00
E (799) ulx3s_spi: SPI self-check FAIL RD BUILD_TARGET ASIC_GF180_OR_ULX3S: expected ASIC GF180 42 or ULX3S FPGA 85/86/87/82/83,                      actual 00 (UNKNOWN)
I (819) ulx3s_spi: SPI self-check PASS RE UNUSED: 00
I (819) ulx3s_spi: SPI self-check PASS RF UNUSED: 00
E (829) ulx3s_spi: SPI self-check FAIL R5 STATUS initial: expected cold 04 or warmed 3C, actual 00
I (839) ulx3s_spi: SPI self-check step 2/3: record passive R6/R7 snapshot before active TRNG check
I (849) ulx3s_spi: SPI self-check INFO R6/R7 raw initial snapshot: 0x0000
I (859) ulx3s_spi: SPI self-check step 3/3: temporarily enable TRNG and require R6/R7 to change
I (859) ulx3s_spi: --------------------------------------------------------
I (869) ulx3s_spi: SPI self-check: active R6/R7 raw-change test
I (879) ulx3s_spi: --------------------------------------------------------
I (889) ulx3s_spi: SPI self-check purpose: prove R6/R7 are not fixed when the TRNG is explicitly enabled
I (899) ulx3s_spi: SPI self-check active config: write R0=00, R1=0x03, R2=0x01, R3=0x00, R4=0xFF, then R0=0x01
I (909) ulx3s_spi: SPI self-check pass rule: at least two unique 16-bit raw values across 8 samples
I (919) ulx3s_spi: SPI self-check active config applied; settling for 20 ms before sampling...
I (949) ulx3s_spi: SPI self-check raw sample 0: raw=0x0000 ctrl=0x00 status=0x00 src=0 div=0x00 mode=0x00 oscen=0x00
I (959) ulx3s_spi: SPI self-check raw sample 1: raw=0x0000 ctrl=0x00 status=0x00 src=0 div=0x00 mode=0x00 oscen=0x00
I (969) ulx3s_spi: SPI self-check raw sample 2: raw=0x0000 ctrl=0x00 status=0x00 src=0 div=0x00 mode=0x00 oscen=0x00
I (979) ulx3s_spi: SPI self-check raw sample 3: raw=0x0000 ctrl=0x00 status=0x00 src=0 div=0x00 mode=0x00 oscen=0x00
I (989) ulx3s_spi: SPI self-check raw sample 4: raw=0x0000 ctrl=0x00 status=0x00 src=0 div=0x00 mode=0x00 oscen=0x00
I (999) ulx3s_spi: SPI self-check raw sample 5: raw=0x0000 ctrl=0x00 status=0x00 src=0 div=0x00 mode=0x00 oscen=0x00
I (1009) ulx3s_spi: SPI self-check raw sample 6: raw=0x0000 ctrl=0x00 status=0x00 src=0 div=0x00 mode=0x00 oscen=0x00
I (1019) ulx3s_spi: SPI self-check raw sample 7: raw=0x0000 ctrl=0x00 status=0x00 src=0 div=0x00 mode=0x00 oscen=0x00
I (1029) ulx3s_spi: SPI self-check: restoring saved config after active raw-change test
E (1029) ulx3s_spi: SPI self-check FAIL R6/R7 raw: fixed at 0x0000 across 8 active TRNG samples
I (1039) ulx3s_spi: SPI self-check step 3/3: re-read R0-RF after active warm-up and restore
I (1049) ulx3s_spi: SPI regs: R0=00 R1=00 R2=00 R3=00 R4=00 R5=00 R6=00 R7=00
I (1059) ulx3s_spi: SPI regs: R8=00 R9=00 RA=00 RB=00 RC=00 RD=00 RE=00 RF=00
I (1069) ulx3s_spi: raw=0x0000 status=0x00 src=0 div=0x00 mode=0x00 oscen=0x00 build=0x00(UNKNOWN) ui=0x00 uo=0x00 uio_in=0x00 ui                     o_out=0x00 uio_oe=0x00
W (1079) ulx3s_spi: SPI self-check WARN R5 STATUS after active warm-up/restore: expected 3C, actual 00
I (1089) ulx3s_spi: SPI self-check final pin snapshot after warm-up/restore: ui=0x00 uo=0x00 uio_in=0x00 uio_out=0x00 uio_oe=0x00
E (1099) ulx3s_spi: SPI self-check result: FAIL, pass=5 fail=7
E (1109) main: ulx3s_spi_self_check_regs_once failed: ESP_FAIL
I (1119) main_task: Returned from app_main()
```