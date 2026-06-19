# Example Test Results

<!--- # Do not move this file. Referenced by TT 4337 Documentation https://app.tinytapeout.com/projects/4337 --->


```text
Info: Program finished normally.
ecppack ulx3s_out.config ulx3s.bit

Scanning build log...
IGNORE_COMBINATIONAL_WARNING=1
NOTE: Ignoring ABC combinational network warning as requested
Build PASSED
Flash...
Flashing file:
-rw-r--r-- 1 gojimmypi gojimmypi 299336 Jun 19 09:01 /mnt/c/workspace/ttgf-UART-FSM-TRNG-Lab/ulx3s/ulx3s.bit
ULX2S / ULX3S JTAG programmer v4.8 (git 96ebb45 built Oct  7 2020 22:42:00)
Copyright (C) Marko Zec, EMARD, gojimmypi, kost and contributors
Using USB cable: ULX3S FPGA 12K v3.0.3
Programming: 100%
Completed in 13.86 seconds.
/mnt/c/workspace/ttgf-UART-FSM-TRNG-Lab/test-hw
Press Enter to continue...
Configuration in: /mnt/c/workspace/ttgf-UART-FSM-TRNG-Lab/src/project_config.v
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
VERSION_STRING="Version 1.0.4 6/18/2026"
Expected version: Version 1.0.4 6/18/2026

Skipping register reset. Use --reset-registers to start from configured defaults.

Running: version_if_present
Version probe response: b'Version 1.0.4 6/18/2026\r'
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
Expected version: Version 1.0.4 6/18/2026

Running: reset_config_registers
PASS: Reset E0
PASS: Reset V0
PASS: Reset W0
PASS: Reset S0
PASS: Reset D10
PASS: Reset M00
PASS: Reset O01

Running: version_if_present
Version probe response: b'Version 1.0.4 6/18/2026\r'
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
PASS: R5 active oscillator health: 0x3D (trng_enable, any_osc_en, health_valid, activity_seen, repetition_fail)
PASS: R5 active oscillator failure bits: 0x3D (trng_enable, any_osc_en, health_valid, activity_seen, repetition_fail)
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
  sample 01: 0xD1BF
PASS: Enable sampling
PASS: Freeze sampling
  sample 02: 0x00B5
PASS: Enable sampling
PASS: Freeze sampling
  sample 03: 0xEC88
PASS: Enable sampling
PASS: Freeze sampling
  sample 04: 0x257C
PASS: Enable sampling
PASS: Freeze sampling
  sample 05: 0xC317
PASS: Enable sampling
PASS: Freeze sampling
  sample 06: 0x5338
PASS: Enable sampling
PASS: Freeze sampling
  sample 07: 0xA957
PASS: Enable sampling
PASS: Freeze sampling
  sample 08: 0x9752

Evaluation: TRNG S0 LFSR frozen samples
  Samples:      8
  Unique:       8
  Zero samples: 0
  0xFFFF count: 0
  One bits:     63/128
  One ratio:    0.492
PASS: sample output changes
PASS: bit balance is reasonable for this small sample set

Running: TRNG S1 RO0/fallback path
PASS: Configure E0
PASS: Configure source
PASS: Configure oscillator mask
PASS: Configure divider
PASS: Enable sampling
PASS: Freeze sampling
  sample 01: 0x067F
PASS: Enable sampling
PASS: Freeze sampling
  sample 02: 0xF33F
PASS: Enable sampling
PASS: Freeze sampling
  sample 03: 0x0300
PASS: Enable sampling
PASS: Freeze sampling
  sample 04: 0xFCC0
PASS: Enable sampling
PASS: Freeze sampling
  sample 05: 0x30CC
PASS: Enable sampling
PASS: Freeze sampling
  sample 06: 0x0C0F
PASS: Enable sampling
PASS: Freeze sampling
  sample 07: 0xF0FC
PASS: Enable sampling
PASS: Freeze sampling
  sample 08: 0x1999

Evaluation: TRNG S1 RO0/fallback path
  Samples:      8
  Unique:       8
  Zero samples: 0
  0xFFFF count: 0
  One bits:     60/128
  One ratio:    0.469
PASS: sample output changes
PASS: bit balance is reasonable for this small sample set

Running: TRNG S2 ROX/fallback path
PASS: Configure E0
PASS: Configure source
PASS: Configure oscillator mask
PASS: Configure divider
PASS: Enable sampling
PASS: Freeze sampling
  sample 01: 0x3003
PASS: Enable sampling
PASS: Freeze sampling
  sample 02: 0x19F9
PASS: Enable sampling
PASS: Freeze sampling
  sample 03: 0x3F3F
PASS: Enable sampling
PASS: Freeze sampling
  sample 04: 0xE7F9
PASS: Enable sampling
PASS: Freeze sampling
  sample 05: 0x8180
PASS: Enable sampling
PASS: Freeze sampling
  sample 06: 0x33C0
PASS: Enable sampling
PASS: Freeze sampling
  sample 07: 0x3FCC
PASS: Enable sampling
PASS: Freeze sampling
  sample 08: 0xCF0C

Evaluation: TRNG S2 ROX/fallback path
  Samples:      8
  Unique:       8
  Zero samples: 0
  0xFFFF count: 0
  One bits:     64/128
  One ratio:    0.500
PASS: sample output changes
PASS: bit balance is reasonable for this small sample set

Running: TRNG S3 MIX/fallback path
PASS: Configure E0
PASS: Configure source
PASS: Configure oscillator mask
PASS: Configure divider
PASS: Enable sampling
PASS: Freeze sampling
  sample 01: 0x303F
PASS: Enable sampling
PASS: Freeze sampling
  sample 02: 0xFFFF
PASS: Enable sampling
PASS: Freeze sampling
  sample 03: 0xF3CF
PASS: Enable sampling
PASS: Freeze sampling
  sample 04: 0xF3C3
PASS: Enable sampling
PASS: Freeze sampling
  sample 05: 0x3FFF
PASS: Enable sampling
PASS: Freeze sampling
  sample 06: 0xC30C
PASS: Enable sampling
PASS: Freeze sampling
  sample 07: 0xCC33
PASS: Enable sampling
PASS: Freeze sampling
  sample 08: 0x6678

Evaluation: TRNG S3 MIX/fallback path
  Samples:      8
  Unique:       8
  Zero samples: 0
  0xFFFF count: 1
  One bits:     82/128
  One ratio:    0.641
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
Port used: /dev/ttyS12
gojimmypi:/mnt/c/workspace/ttgf-UART-FSM-TRNG-Lab/test-hw
```
