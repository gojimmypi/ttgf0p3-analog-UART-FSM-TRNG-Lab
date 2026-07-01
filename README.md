![](../../workflows/gds/badge.svg) ![](../../workflows/docs/badge.svg) ![](../../workflows/test/badge.svg) ![](../../workflows/fpga/badge.svg)

# Tiny Tapeout Project: ttgf0p3-analog-UART-FSM-TRNG-Lab

Version 1.1.5 7/1/2026

Details of this project are located in [docs/info.md](./docs/info.md)

This project is part of the [EXPERIMENTAL Tiny Tapeout GF ttgf0p3 Analog](https://app.tinytapeout.com/shuttles/ttgf0p3) shuttle in [Project #5276](https://app.tinytapeout.com/projects/5276)

See the companion experimental (non-Analog) [Project #5271](https://app.tinytapeout.com/projects/5271) and the [Tiny Tapeout GF 26a](https://app.tinytapeout.com/shuttles/ttgf26a) shuttle in [Project #4337](https://app.tinytapeout.com/projects/4337)..

This branch turns the former GF 0p3 digital duplicate into a small analog experiment shell. It keeps the existing UART/SPI/TRNG control plane, enables `analog_pins: 6` in `info.yaml`, and adds a GF180 analog experiment hook for all six available `ua[5:0]` pins.

The FPGA builds remain useful for testing the UART/SPI register interface, scripts, binary stream framing, and deterministic TRNG surrogate. They cannot test real GF180 analog behavior such as DAC linearity, comparator offset, oscillator jitter, leakage, mismatch, or analog noise.

This project's top module is `tt_um_gojimmypi_ttgfa_UART_FSM_TRNG_Lab`, which keeps the GF analog `a` suffix (`ttgfa`) compared with the #4337 name `tt_um_gojimmypi_ttgf_UART_FSM_TRNG_Lab`.

See companion projects developed in parallel:

- This https://github.com/gojimmypi/ttgf0p3-UART-FSM-TRNG-Lab (Global Foundry 180 GFMCU180 Open Source PDK)
- Companion https://github.com/gojimmypi/ttgf-UART-FSM-TRNG-Lab (Global Foundry 180 GFMCU180 Open Source PDK)
- Companion https://github.com/gojimmypi/ttsky-UART-FSM-TRNG-Lab (Sky130, draft [4338](https://app.tinytapeout.com/projects/4338))

## Files and Directories

- `.devcontainer` - TT VS Code devcontainer configuration for easy setup and development. Edit with caution.
- `.github/workflows` - see the CI [workflows](.github/workflows)
- `docs` - documentation for the project, which is used to generate the project page on the Tiny Tapeout website. 
- `info.yaml` - metadata for the project, which is used to generate the project page on the Tiny Tapeout website.
- `ice40` - contains build scripts for testing this project on the TT Lattice iCE40 FPGA [Demoboard](https://store.tinytapeout.com/products/FPGA-Development-Kit-p813805747).
- `scripts` - scripts for building, testing, and flashing the project.
- `src` - the main source files for the project, including the Verilog code for the design and any necessary configuration files.
- `test` - testbenches and scripts for testing the project using simulation.  
- `test-hw` - test scripts and files for testing the project on hardware. Only the ULX3S FPGA board at this time.
- `ulx3s` - files for testing the project on the ULX3S FPGA board, including a wrapper module and scripts for building and flashing the board.
- `ulx3s/ESP32` - an app for the ULX3S on-board ESP32 to test the SPI communications with this TT project.

## What is Tiny Tapeout?

Tiny Tapeout is an educational project that aims to make it easier and cheaper than ever to get your digital designs manufactured on a real chip.

To learn more and get started, visit https://tinytapeout.com.

## Set up your Verilog project

1. Add your Verilog files to the `src` folder.
2. Edit the [info.yaml](info.yaml) and update information about your project, paying special attention to the `source_files` and `top_module` properties. If you are upgrading an existing Tiny Tapeout project, check out our [online info.yaml migration tool](https://tinytapeout.github.io/tt-yaml-upgrade-tool/).
3. Edit [docs/info.md](docs/info.md) and add a description of your project.
4. Adapt the testbench to your design. See [test/README.md](test/README.md) for more information.

The GitHub action will automatically build the ASIC files using [LibreLane](https://www.zerotoasiccourse.com/terminology/librelane/).


## Analog projects

For specifications and instructions, see the [analog specs page](https://tinytapeout.com/specs/analog/).

This repository contains the digital/FPGA-safe UART/SPI/TRNG shell plus a small analog pad exerciser in `src/ANALOG/analog_experiment_stub.v`. The analog block now drives a 1-bit sigma-delta DAC, monitor mux, oscillator/debug output, and charge/release/sample probe sequence on the six GF 0p3 analog pins. The sampled analog experiment state is readable at `R14`/`0xE`, and the latest `ua[5]` passive-structure threshold/decay timing sample is readable at `R15`/`0xF`, through the existing UART/SPI register interface. The analog GDS patch flow also adds a small real on-chip Metal4 passive structure on `ua[5]`: a pad-connected pickup plate and nearby grounded fringe finger, intended for charge/release/leakage/noise experiments. It is useful for FPGA/demoboard control-plane testing and post-silicon pad experiments, but it is still not a precision analog macro or a substitute for GF180 schematic/layout/SPICE/PEX work. The analog pin use is:

| Pin | Name | Purpose |
| --- | --- | --- |
| `ua[0]` | `ain_ext` | External analog stimulus/noise input |
| `ua[1]` | `dac_out` | 1-bit sigma-delta DAC output; RC-filter externally |
| `ua[2]` | `cmp_ref_ext` | External comparator/reference input |
| `ua[3]` | `amon_out` | Digital monitor mux output for DAC/comparator/probe/TRNG/status |
| `ua[4]` | `osc_out` | Divider or TRNG-bit monitor output |
| `ua[5]` | `puf_probe` | Charge/release/sample probe pad connected to a small on-chip Metal4 fringe/pickup structure |

Analog status readback is available at `R14`/`0xE` when `BIG16_SPI_REG` is enabled: bit 0 sampled `ua[0]`, bit 1 sampled `ua[2]`, bit 2 threshold compare, bit 3 live sampled `ua[5]`, bit 4 latched probe sample, bit 5 DAC bit, bit 6 oscillator/TRNG monitor bit, and bit 7 probe-driver enable. The new `R15`/`0xF` readback reports the latest `ua[5]` threshold/decay timing sample from the charge/release phase, so the on-chip passive structure is not just present in GDS; it is actively measured by RTL.


## Enable GitHub actions to build the results page

- [Enabling GitHub Pages](https://tinytapeout.com/faq/#my-github-action-is-failing-on-the-pages-part)

## Resources

- [FAQ](https://tinytapeout.com/faq/)
- [Digital design lessons](https://tinytapeout.com/digital_design/)
- [Learn how semiconductors work](https://tinytapeout.com/siliwiz/)
- [Join the community](https://tinytapeout.com/discord)
- [Build your design locally](https://www.tinytapeout.com/guides/local-hardening/)

## What next?

- [Submit your design to the next shuttle](https://app.tinytapeout.com/).
- Edit [this README](README.md) and explain your design, how it works, and how to test it.
- Share your project on your social network of choice:
  - LinkedIn [#tinytapeout](https://www.linkedin.com/search/results/content/?keywords=%23tinytapeout) [@TinyTapeout](https://www.linkedin.com/company/100708654/)
  - Mastodon [#tinytapeout](https://chaos.social/tags/tinytapeout) [@matthewvenn](https://chaos.social/@matthewvenn)
  - X (formerly Twitter) [#tinytapeout](https://twitter.com/hashtag/tinytapeout) [@tinytapeout](https://twitter.com/tinytapeout)
  - Bluesky [@tinytapeout.com](https://bsky.app/profile/tinytapeout.com)
