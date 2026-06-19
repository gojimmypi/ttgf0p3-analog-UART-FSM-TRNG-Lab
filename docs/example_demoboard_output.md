# Example Demoboard Output

<!--- # Do not move this file. Referenced by TT 4337 Documentation https://app.tinytapeout.com/projects/4337 --->

<!--- # Use only Fully Qualified URLs. This file is copied out of the GitHub repo for publication. --->

This is the example output for the [Tiny Tapeout FPGA Demoboard](https://tinytapeout.com/guides/get-started-demoboard-etr/) 
for the [Hardware Entropy Explorer: UART/SPI TRNG and PUF](https://app.tinytapeout.com/projects/4337) project.

The source code for this test is in [ice40](`https://github.com/gojimmypi/ttgf-UART-FSM-TRNG-Lab/tree/main/ice40`).

```text
gojimmypi:/mnt/c/workspace/ttgf-UART-FSM-TRNG-Lab/ice40
$ ./build_and_flash.sh

[ ..snip ..]

Info: Program finished normally.
2026-06-19 09:03:17,970 - tt_fpga    - INFO     - Bitstream created successfully: /mnt/c/workspace/ttgf-UART-FSM-TRNG-Lab/build/tt_um_gojimmypi_ttgf_UART_FSM_TRNG_Lab.bin
**************************************************************************
Build complete, proceeding to flash...
**************************************************************************
Uploading build/tt_um_gojimmypi_ttgf_UART_FSM_TRNG_Lab.bin
cp build/tt_um_gojimmypi_ttgf_UART_FSM_TRNG_Lab.bin :/bitstreams/tt_um_gojimmypi_ttgf_UART_FSM_TRNG_Lab.bin
cp :/config.ini /tmp/ttconf-wtjyr0p2.tmp
cp /tmp/ttconf-wtjyr0p2.tmp :/config.ini
Completed with TT_PORT: /dev/ttyS6
/mnt/c/workspace/ttgf-UART-FSM-TRNG-Lab/ice40
gojimmypi:/mnt/c/workspace/ttgf-UART-FSM-TRNG-Lab/ice40
$ ./run_tests.sh
**************************************************************************
**  Begin ./run_tests.sh from /mnt/c/workspace/ttgf-UART-FSM-TRNG-Lab/ice40
**************************************************************************
TT_UART_PORT: /dev/ttyS5
TT_PORT:      /dev/ttyS6
**************************************************************************
**  Setup environment
**************************************************************************
**************************************************************************
**  Begin ./env_ice40.sh from /mnt/c/workspace/ttgf-UART-FSM-TRNG-Lab/ice40
**************************************************************************
Setting up environment variables for Tiny Tapeout FPGA project...
TT_PORT:              /dev/ttyS6
WORKSPACE:            /mnt/c/workspace
TT_PROJECT_NAME:      ttgf-UART-FSM-TRNG-Lab
TT_PROJECT_NAME_ALT:  ttgf_UART_FSM_TRNG_Lab
TT_PROJECT_ROOT:      /mnt/c/workspace/ttgf-UART-FSM-TRNG-Lab
TT_TOP_NAME:          tt_um_gojimmypi_ttgf_UART_FSM_TRNG_Lab
TT_TOOLS:             /mnt/c/workspace/tt-support-tools-gojimmypi
**************************************************************************
**  Calling project reset script on port /dev/ttyS6
**************************************************************************
**************************************************************************
**  Begin ./project_reset.sh from /mnt/c/workspace/ttgf-UART-FSM-TRNG-Lab/ice40
**************************************************************************
TT_PORT:     /dev/ttyS6
TT_TOP_NAME: tt_um_gojimmypi_ttgf_UART_FSM_TRNG_Lab
>>> tt.shuttle.tt_um_gojimmypi_ttgf_UART_FSM_TRNG_Lab.enable()
tt.shuttle.tt_um_gojimmypi_ttgf_UART_FSM_TRNG_Lab.enable()
ttboard.fpga.fpga_mux: Enable design tt_um_gojimmypi_ttgf_UART_FSM_TRNG_Lab
Configuring PIO with frequency: 16000000 Hz
State machine activated
SS low, starting transmission

>>> tt.clock_project_PWM(25000000)
Transmission complete, total bytes: 104090
State machine deactivated, SS high
ttboard.demoboard: Resetting system clock to default 125000000.0Hz
ttboard.demoboard: In "manual inputs" mode but clock freq set--setting up for CLK/RST RP ctrl
ttboard.demoboard: Setting RP2040 system clock to 100000000Hz
ttboard.demoboard: Clocking at 25000000Hz
>>> tt.clock_project_PWM(25000000)
ttboard.demoboard: Clocking at 25000000Hz
<PWM slice=0 channel=0 invert=0>
>>>
>>> tt.reset_project(True)
tt.reset_project(True)
ttboard.demoboard: Changing reset to output mode
>>>
>>> tt.reset_project(False)
tt.reset_project(False)
>>>
**************************************************************************
**  Calling test scripts on port /dev/ttyS5
**************************************************************************
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
  sample 01: 0xCC94
PASS: Enable sampling
PASS: Freeze sampling
  sample 02: 0xE78E
PASS: Enable sampling
PASS: Freeze sampling
  sample 03: 0xB264
PASS: Enable sampling
PASS: Freeze sampling
  sample 04: 0x6390
PASS: Enable sampling
PASS: Freeze sampling
  sample 05: 0xE20B
PASS: Enable sampling
PASS: Freeze sampling
  sample 06: 0xD938
PASS: Enable sampling
PASS: Freeze sampling
  sample 07: 0x8F2C
PASS: Enable sampling
PASS: Freeze sampling
  sample 08: 0x3F7F

Evaluation: TRNG S0 LFSR frozen samples
  Samples:      8
  Unique:       8
  Zero samples: 0
  0xFFFF count: 0
  One bits:     66/128
  One ratio:    0.516
PASS: sample output changes
PASS: bit balance is reasonable for this small sample set

Running: TRNG S1 RO0/fallback path
PASS: Configure E0
PASS: Configure source
PASS: Configure oscillator mask
PASS: Configure divider
PASS: Enable sampling
PASS: Freeze sampling
  sample 01: 0x1E01
PASS: Enable sampling
PASS: Freeze sampling
  sample 02: 0xFC0F
PASS: Enable sampling
PASS: Freeze sampling
  sample 03: 0x199F
PASS: Enable sampling
PASS: Freeze sampling
  sample 04: 0x3C03
PASS: Enable sampling
PASS: Freeze sampling
  sample 05: 0xF303
PASS: Enable sampling
PASS: Freeze sampling
  sample 06: 0x033C
PASS: Enable sampling
PASS: Freeze sampling
  sample 07: 0x0CF0
PASS: Enable sampling
PASS: Freeze sampling
  sample 08: 0x0FCC

Evaluation: TRNG S1 RO0/fallback path
  Samples:      8
  Unique:       8
  Zero samples: 0
  0xFFFF count: 0
  One bits:     58/128
  One ratio:    0.453
PASS: sample output changes
PASS: bit balance is reasonable for this small sample set

Running: TRNG S2 ROX/fallback path
PASS: Configure E0
PASS: Configure source
PASS: Configure oscillator mask
PASS: Configure divider
PASS: Enable sampling
PASS: Freeze sampling
  sample 01: 0xC000
PASS: Enable sampling
PASS: Freeze sampling
  sample 02: 0x67E6
PASS: Enable sampling
PASS: Freeze sampling
  sample 03: 0x0798
PASS: Enable sampling
PASS: Freeze sampling
  sample 04: 0xF300
PASS: Enable sampling
PASS: Freeze sampling
  sample 05: 0xF0FF
PASS: Enable sampling
PASS: Freeze sampling
  sample 06: 0x9861
PASS: Enable sampling
PASS: Freeze sampling
  sample 07: 0x0000
PASS: Enable sampling
PASS: Freeze sampling
  sample 08: 0xF987

Evaluation: TRNG S2 ROX/fallback path
  Samples:      8
  Unique:       8
  Zero samples: 1
  0xFFFF count: 0
  One bits:     52/128
  One ratio:    0.406
PASS: sample output changes
PASS: bit balance is reasonable for this small sample set

Running: TRNG S3 MIX/fallback path
PASS: Configure E0
PASS: Configure source
PASS: Configure oscillator mask
PASS: Configure divider
PASS: Enable sampling
PASS: Freeze sampling
  sample 01: 0x9E00
PASS: Enable sampling
PASS: Freeze sampling
  sample 02: 0x8018
PASS: Enable sampling
PASS: Freeze sampling
  sample 03: 0xF0F0
PASS: Enable sampling
PASS: Freeze sampling
  sample 04: 0x0FF0
PASS: Enable sampling
PASS: Freeze sampling
  sample 05: 0xC3C3
PASS: Enable sampling
PASS: Freeze sampling
  sample 06: 0x81E1
PASS: Enable sampling
PASS: Freeze sampling
  sample 07: 0x33CC
PASS: Enable sampling
PASS: Freeze sampling
  sample 08: 0xF30F

Evaluation: TRNG S3 MIX/fallback path
  Samples:      8
  Unique:       8
  Zero samples: 0
  0xFFFF count: 0
  One bits:     56/128
  One ratio:    0.438
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
**************************************************************************
**  Done. Ports used:
**************************************************************************
TT_UART_PORT: /dev/ttyS5
TT_PORT:      /dev/ttyS6
gojimmypi:/mnt/c/workspace/ttgf-UART-FSM-TRNG-Lab/ice40
$
```