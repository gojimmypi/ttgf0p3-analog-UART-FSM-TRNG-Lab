# Tools

Maintenance scripts used to build, harden, patch, and validate the GF180 analog custom-GDS submission.

There's still a manual process:

1) commit TRL changes
2) harden-gds-lef workflow runs, download hardened-gds-lef artifact
3) manual copy into gds/ and lef/
4) commit gds and lef files
5) rerun gds workflow -> tt_submission artifact / precheck / GL test

## Release-critical scripts

- `build_custom_gds_verilog.py` - expands the split RTL under `src/` into the single Verilog file passed to `custom_gds`.
- `check_gds_content.py` - verifies that the submitted GDS contains real non-frame layout geometry and, when requested, the DRC-safe ua[5] passive probe structure.
- `full_harden_artifact.sh` - CI hardening path used by `.github/workflows/harden-gds-lef.yaml` to regenerate and stage hardened GDS/LEF artifacts.
- `full_harden_local.sh` - local hardening path used by `generate_analog_gds.sh`.
- `generate_analog_gds.sh` - preferred local command for regenerating final analog GDS/LEF from the latest RTL.
- `patch_analog_outputs.py` - final GDS/LEF post-processing for corrected analog pin/passive geometry.
- `patch_full_harden_config.py` - adjusts TT hardening config for the GF180 analog 1x2 template.
- `patch_full_harden_source.py` - temporary harden-only patch that removes top-level power pins from `src/project.v`; callers restore the file afterward.
- `refresh.sh` - compatibility wrapper for the supported local regeneration command.
- `strip_unused_analog_pins.py` - removes disabled ua[6]/ua[7] GDS text labels while preserving LEF pins required by TT checks.
