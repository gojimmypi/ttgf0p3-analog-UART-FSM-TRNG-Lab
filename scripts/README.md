# Scripts

Some bash scripts for cleaning and validating project source files.

- `check-nettype.sh` - ensure verilog files are wrapped in `` `default_nettype none `` .. `` `default_nettype wire ``
- `clean-files.sh` - ensure there are only simple ASCII chars & using UTF-8 encoding
- `env_tiny_tapeout.sh` - set environment variables (e.g. `source ./env_tiny_tapeout.sh`)
- `show_effective_defines.sh` - list the effective active macros in the `project_config.v` file, optionally generate C header.
- `verilator_lint.sh` - lint the Verilog project using Verilator.

## Generate C Header for ESP32

Example to create `tt_effective_defines.h` in the [ulx3s/ESP32/main/include](../ulx3s/ESP32/main/include) directory.

```bash
./show_effective_defines.sh  ../src/project_config.v  --header tt_effective_defines.h
```
