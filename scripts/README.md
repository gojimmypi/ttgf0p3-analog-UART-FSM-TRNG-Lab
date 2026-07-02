# Scripts

Some bash scripts for cleaning and validating project source files.

- `check-forbidden-files.sh` - CI guard for generated/local-only files that must not be committed, including caches, logs, `mag/`, generated TT configs, and hardening output.
- `check-nettype.sh` - ensure tracked Verilog files are wrapped in `` `default_nettype none `` .. `` `default_nettype wire ``.
- `clean-files.sh` - convert project source files to simple ASCII where needed.
- `env_tiny_tapeout.sh` - set local Tiny Tapeout environment variables (e.g. `source ./env_tiny_tapeout.sh`).
- `get_expected_version.sh` - extract `VERSION_STRING` from `project_config.v` for tests.
- `is_effective_define_enabled.sh` - query one effective Verilog define after preprocessing.
- `show_effective_defines.sh` - list effective active macros in `project_config.v`, optionally generate a C header.
- `verilator_lint.sh` - lint the Verilog project using Verilator.

## Generate C Header for ESP32

Example to create `tt_effective_defines.h` in the [ulx3s/ESP32/main/include](../ulx3s/ESP32/main/include) directory.

```bash
./show_effective_defines.sh  ../src/project_config.v  --header tt_effective_defines.h
```
