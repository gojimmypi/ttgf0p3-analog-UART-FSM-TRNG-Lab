# Example Test Results

<!--- # Do not move this file. Referenced by TT 4337 Documentation https://app.tinytapeout.com/projects/4337 --->

<!--- # Use only Fully Qualified URLs. This file is copied out of the GitHub repo for publication. --->

This is the example output for the [Radiona ULX3S FPGA](https://radiona.org/ulx3s/) 
for the [Hardware Entropy Explorer: UART/SPI TRNG and PUF](https://app.tinytapeout.com/projects/4337) project.

The source code for this test is in [`ulx3s`](https://github.com/gojimmypi/ttgf0p3-UART-FSM-TRNG-Lab/tree/main/ulx3s)

```text
Info: Program finished normally.
ecppack ulx3s_out.config ulx3s.bit

Scanning build log...
IGNORE_COMBINATIONAL_WARNING=1
NOTE: Ignoring ABC combinational network warning as requested
Build PASSED
Flash...
Flashing file: ulx3s.bit
-rw-r--r-- 1 gojimmypi gojimmypi 299495 Jun 20 20:29 /mnt/c/workspace/ttgf0p3-UART-FSM-TRNG-Lab/ulx3s/ulx3s.bit
WSL Calling ./fujprog-v48-win64.exe (should auto-detect ULX3S port) ...
ULX2S / ULX3S JTAG programmer v4.8 (git 96ebb45 built Oct  7 2020 22:42:00)
Copyright (C) Marko Zec, EMARD, gojimmypi, kost and contributors
Using USB cable: ULX3S FPGA 12K v3.0.3
Programming: 100%
Completed in 13.05 seconds.
/mnt/c/workspace/ttgf0p3-UART-FSM-TRNG-Lab/test-hw
Ready to test external ULX3S UART () on port /dev/ttyS7 - Press Enter to continue ...
Configuration in: /mnt/c/workspace/ttgf0p3-UART-FSM-TRNG-Lab/src/project_config.v
ADJUSTABLE_BAUD_ENABLED= (defined)
BIG16_SPI_REG= (defined)
JTAG_ADDR_MSB=3
JTAG_ADDR_WIDTH=(3 + 1)
JTAG_ENABLED= (defined)
PROJECT_CLOCK_HZ=32'd25_000_000
PROJECT_CONFIG_V= (defined)
PROJECT_UART_BAUD=32'd115_200
SPI_ADDR_MSB=3
SPI_ADDR_WIDTH=(3 + 1)
SPI_ENABLED= (defined)
SPI_REG_ACCESS= (defined)
TRNG_BINARY_STREAM= (defined)
TRNG_CONDITIONED_STREAM= (defined)
TRNG_CONDITIONED_STREAM_GALOIS= (defined)
TRNG_ENABLED= (defined)
TRNG_HEALTH_STATUS= (defined)
TRNG_RAW_CLEAN_MIX= (defined)
UART_ENABLED= (defined)
USE_LONG_STRINGS= (defined)
VERSION_STRING_LEN=23
VERSION_STRING="Version 1.0.5 6/27/2026"
Expected version: Version 1.0.5 6/27/2026

Skipping register reset. Use --reset-registers to start from configured defaults.

Running: version_if_present
Version probe response: b'Version 1.0.5 6/27/2026\r'
PASS: Version command exact match

Running: power_on_defaults
PASS: R0 default reg_ctrl
PASS: R1 default reg_src
PASS: R2 default reg_div
PASS: R3 default reg_mode
PASS: R4 default reg_oscen

Running: single_nibble_writes
PASS: E1 write enable
PASS: R0 after E1
PASS: E0 clear enable
PASS: R0 after E0
PASS: V1 set ctrl bit 1
PASS: R0 after V1
PASS: W1 set ctrl bit 2
PASS: R0 after W1
PASS: S3 set source
PASS: R1 after S3
PASS: S0 clear source
PASS: R1 after S0

Running: two_nibble_writes
PASS: D2A write divider
PASS: R2 after D2A
PASS: M5C write mode
PASS: R3 after M5C
PASS: O0F write oscillator enable
PASS: R4 after O0F

Running: read_only_registers_format
PASS: R5 status format
PASS: R6 rawlo format
PASS: R7 rawhi format

Running: crlf_handling
PASS: CRLF read accepted

Running: error_cases
PASS: Unknown command
PASS: Bad hex digit
SKIP: Bad read register; BIG16_SPI_REG makes R8..RF valid
PASS: Missing second digit
PASS: Unexpected extra byte

Running: repeated_reads
PASS: Repeated R2 read 1
PASS: Repeated R2 read 2
PASS: Repeated R2 read 3
PASS: Repeated R2 read 4
PASS: Repeated R2 read 5

Command test coverage:
PASS: all known commands have tests

Tests passed: 8
Tests skipped: 0
Tests failed: 0

PASS
Expected version: Version 1.0.5 6/27/2026

Running: reset_config_registers
PASS: Reset E0
PASS: Reset V0
PASS: Reset W0
PASS: Reset S0
PASS: Reset D10
PASS: Reset M00
PASS: Reset O01

Running: version_if_present
Version probe response: b'Version 1.0.5 6/27/2026\r'
PASS: Version command exact match

Running: power_on_defaults
PASS: R0 default reg_ctrl
PASS: R1 default reg_src
PASS: R2 default reg_div
PASS: R3 default reg_mode
PASS: R4 default reg_oscen

Running: single_nibble_writes
PASS: E1 write enable
PASS: R0 after E1
PASS: E0 clear enable
PASS: R0 after E0
PASS: V1 set ctrl bit 1
PASS: R0 after V1
PASS: W1 set ctrl bit 2
PASS: R0 after W1
PASS: S3 set source
PASS: R1 after S3
PASS: S0 clear source
PASS: R1 after S0

Running: two_nibble_writes
PASS: D2A write divider
PASS: R2 after D2A
PASS: M5C write mode
PASS: R3 after M5C
PASS: O0F write oscillator enable
PASS: R4 after O0F

Running: read_only_registers_format
PASS: R5 status format
PASS: R6 rawlo format
PASS: R7 rawhi format

Running: crlf_handling
PASS: CRLF read accepted

Running: error_cases
PASS: Unknown command
PASS: Bad hex digit
SKIP: Bad read register; BIG16_SPI_REG makes R8..RF valid
PASS: Missing second digit
PASS: Unexpected extra byte

Running: repeated_reads
PASS: Repeated R2 read 1
PASS: Repeated R2 read 2
PASS: Repeated R2 read 3
PASS: Repeated R2 read 4
PASS: Repeated R2 read 5

Command test coverage:
PASS: all known commands have tests

Running: final_reset_config_registers
PASS: Reset E0
PASS: Reset V0
PASS: Reset W0
PASS: Reset S0
PASS: Reset D10
PASS: Reset M00
PASS: Reset O01

Tests passed: 10
Tests skipped: 0
Tests failed: 0

PASS

Running: TRNG health status reset/clear
PASS: Reset E0
PASS: Reset V0
PASS: Reset W0
PASS: Reset S0
PASS: Reset D10
PASS: Reset M00
PASS: Reset O01
PASS: Health reset O00 oscillators
PASS: Health clear E0
PASS: Health clear W1
PASS: Health clear W0
PASS: R5 health bits clear after W reset: 0x00 (no flags set)

Running: TRNG health status active oscillator
PASS: Reset E0
PASS: Reset V0
PASS: Reset W0
PASS: Reset S0
PASS: Reset D10
PASS: Reset M00
PASS: Reset O01
PASS: Health clear E0
PASS: Health clear W1
PASS: Health clear W0
PASS: Configure E0
PASS: Configure source
PASS: Configure oscillator mask
PASS: Configure divider
PASS: Health E1 enable
PASS: R5 active oscillator health: 0x3F (trng_enable, sample_tick, any_osc_en, health_valid, activity_seen, repetition_fail)
PASS: R5 active oscillator failure bits: 0x3F (trng_enable, sample_tick, any_osc_en, health_valid, activity_seen, repetition_fail)
PASS: Health cleanup E0

Skipping UART baud transition smoke; use --baud-test to enable it

Running: TRNG binary stream exact length
PASS: Reset E0
PASS: Reset V0
PASS: Reset W0
PASS: Reset S0
PASS: Reset D10
PASS: Reset M00
PASS: Reset O01
PASS: Binary stream reset E0
PASS: Binary stream S3 mixed source
PASS: Binary stream OFF oscillators
PASS: Binary stream D0F divider
PASS: Binary stream E1 enable
PASS: C10 returns exactly 16 bytes
PASS: C10 has no extra byte
PASS: Binary stream cleanup E0
PASS: R0 after binary stream cleanup

Running: TRNG raw binary stream exact length
PASS: Reset E0
PASS: Reset V0
PASS: Reset W0
PASS: Reset S0
PASS: Reset D10
PASS: Reset M00
PASS: Reset O01
PASS: Raw stream reset E0
PASS: Raw stream S3 mixed source
PASS: Raw stream OFF oscillators
PASS: Raw stream D0F divider
PASS: Raw stream E1 enable
PASS: B10 returns exactly 16 bytes
PASS: B10 has no extra byte
PASS: Raw stream cleanup E0
PASS: R0 after raw stream cleanup

Running: TRNG S0 LFSR frozen samples
PASS: Configure E0
PASS: Configure source
PASS: Configure oscillator mask
PASS: Configure divider
PASS: Enable sampling
PASS: Freeze sampling
  sample 01: 0xE936
PASS: Enable sampling
PASS: Freeze sampling
  sample 02: 0x3B09
PASS: Enable sampling
PASS: Freeze sampling
  sample 03: 0xFC55
PASS: Enable sampling
PASS: Freeze sampling
  sample 04: 0xB1DF
PASS: Enable sampling
PASS: Freeze sampling
  sample 05: 0xD287
PASS: Enable sampling
PASS: Freeze sampling
  sample 06: 0x99C4
PASS: Enable sampling
PASS: Freeze sampling
  sample 07: 0x63AC
PASS: Enable sampling
PASS: Freeze sampling
  sample 08: 0x76D1

Evaluation: TRNG S0 LFSR frozen samples
  Samples:      8
  Unique:       8
  Zero samples: 0
  0xFFFF count: 0
  One bits:     69/128
  One ratio:    0.539
PASS: sample output changes
PASS: bit balance is reasonable for this small sample set

Running: TRNG S1 RO0/fallback path
PASS: Configure E0
PASS: Configure source
PASS: Configure oscillator mask
PASS: Configure divider
PASS: Enable sampling
PASS: Freeze sampling
  sample 01: 0x019E
PASS: Enable sampling
PASS: Freeze sampling
  sample 02: 0x30FF
PASS: Enable sampling
PASS: Freeze sampling
  sample 03: 0x3000
PASS: Enable sampling
PASS: Freeze sampling
  sample 04: 0x3030
PASS: Enable sampling
PASS: Freeze sampling
  sample 05: 0xFF3F
PASS: Enable sampling
PASS: Freeze sampling
  sample 06: 0xCFF3
PASS: Enable sampling
PASS: Freeze sampling
  sample 07: 0xCCFC
PASS: Enable sampling
PASS: Freeze sampling
  sample 08: 0x1F99

Evaluation: TRNG S1 RO0/fallback path
  Samples:      8
  Unique:       8
  Zero samples: 0
  0xFFFF count: 0
  One bits:     67/128
  One ratio:    0.523
PASS: sample output changes
PASS: bit balance is reasonable for this small sample set

Running: TRNG S2 ROX/fallback path
PASS: Configure E0
PASS: Configure source
PASS: Configure oscillator mask
PASS: Configure divider
PASS: Enable sampling
PASS: Freeze sampling
  sample 01: 0x3F0F
PASS: Enable sampling
PASS: Freeze sampling
  sample 02: 0x0000
PASS: Enable sampling
PASS: Freeze sampling
  sample 03: 0x679E
PASS: Enable sampling
PASS: Freeze sampling
  sample 04: 0xC003
PASS: Enable sampling
PASS: Freeze sampling
  sample 05: 0xCF00
PASS: Enable sampling
PASS: Freeze sampling
  sample 06: 0x861F
PASS: Enable sampling
PASS: Freeze sampling
  sample 07: 0x8606
PASS: Enable sampling
PASS: Freeze sampling
  sample 08: 0xCCFC

Evaluation: TRNG S2 ROX/fallback path
  Samples:      8
  Unique:       8
  Zero samples: 1
  0xFFFF count: 0
  One bits:     53/128
  One ratio:    0.414
PASS: sample output changes
PASS: bit balance is reasonable for this small sample set

Running: TRNG S3 MIX/fallback path
PASS: Configure E0
PASS: Configure source
PASS: Configure oscillator mask
PASS: Configure divider
PASS: Enable sampling
PASS: Freeze sampling
  sample 01: 0x0333
PASS: Enable sampling
PASS: Freeze sampling
  sample 02: 0x9E00
PASS: Enable sampling
PASS: Freeze sampling
  sample 03: 0x7FFE
PASS: Enable sampling
PASS: Freeze sampling
  sample 04: 0xF00F
PASS: Enable sampling
PASS: Freeze sampling
  sample 05: 0x0CC0
PASS: Enable sampling
PASS: Freeze sampling
  sample 06: 0xFC0F
PASS: Enable sampling
PASS: Freeze sampling
  sample 07: 0x0F30
PASS: Enable sampling
PASS: Freeze sampling
  sample 08: 0xF3CC

Evaluation: TRNG S3 MIX/fallback path
  Samples:      8
  Unique:       8
  Zero samples: 0
  0xFFFF count: 0
  One bits:     63/128
  One ratio:    0.492
PASS: sample output changes
PASS: bit balance is reasonable for this small sample set

PASS

First LFSR sequence
  sample 01: 0x7F2E
  sample 02: 0x9F33
  sample 03: 0xFC1C
  sample 04: 0x6F03
  sample 05: 0x4B7D
  sample 06: 0x52C8
  sample 07: 0xD6B7
  sample 08: 0xEF2A

Second LFSR sequence
  sample 01: 0x7F2E
  sample 02: 0x9F33
  sample 03: 0xFC1C
  sample 04: 0x6F03
  sample 05: 0x4B7D
  sample 06: 0x52C8
  sample 07: 0xD6B7
  sample 08: 0xEF2A

Reproducibility evaluation:
PASS: LFSR sequence is reproducible

Sequence quality check:
  Samples:      8
  Unique:       8
  Zero samples: 0
  0xFFFF count: 0
  One bits:     75/128
  One ratio:    0.586
PASS: deterministic sequence is not stuck

PASS
Port used: /dev/ttyS7
gojimmypi:/mnt/c/workspace/ttgf0p3-UART-FSM-TRNG-Lab/test-hw
$
```
