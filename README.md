![](../../workflows/gds/badge.svg) ![](../../workflows/docs/badge.svg) ![](../../workflows/test/badge.svg) ![](../../workflows/fpga/badge.svg)

# Tiny Tapeout Project: ttgfa-UART-FSM-TRNG-Lab

Version 1.1.0 6/27/2026

Details of this project are located in [docs/info.md](./docs/info.md)

This project is part of the [EXPERIMENTAL Tiny Tapeout GF ttgf0p3 Analog](https://app.tinytapeout.com/shuttles/ttgf0p3) shuttle in [Project #5271](https://app.tinytapeout.com/projects/5271).

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

This repository currently contains the digital/FPGA-safe shell and a placeholder analog hook in `src/ANALOG/analog_experiment_stub.v`. The real analog implementation still needs GF180 schematic/layout/SPICE/PEX work before tapeout. The intended analog pin use is:

| Pin | Name | Purpose |
| --- | --- | --- |
| `ua[0]` | `ain_ext` | External analog stimulus/noise input |
| `ua[1]` | `dac_out` | DAC monitor output |
| `ua[2]` | `cmp_ref_ext` | External comparator/reference input |
| `ua[3]` | `amon_out` | Analog monitor mux output |
| `ua[4]` | `osc_out` | Oscillator monitor output |
| `ua[5]` | `puf_probe` | PUF/noise probe pad |


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
