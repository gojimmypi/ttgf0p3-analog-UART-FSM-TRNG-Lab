/*
 * Copyright (c) 2026 gojimmypi
 * SPDX-License-Identifier: Apache-2.0
 *
 * See ATTRIBUTION.md for third-party sources and credits.
 *
 * file: analog_experiment_stub.v
 *
 * Digital/FPGA-safe placeholder for the GF180 analog experiment block.
 *
 * This module intentionally does not model the real analog behavior. It exists
 * so the mixed-signal top-level has a stable place to connect all ua[5:0]
 * pins while the real GF180 analog layout/SPICE block is developed.
 *
 * Planned analog pin roles:
 * - ua[0]: external analog stimulus/noise input
 * - ua[1]: DAC monitor output
 * - ua[2]: external comparator/reference input
 * - ua[3]: analog monitor mux output
 * - ua[4]: oscillator monitor output
 * - ua[5]: PUF/noise probe pad
 *
 * FPGA builds and ordinary RTL simulation cannot reproduce GF180 analog
 * resistor mismatch, comparator offset, pad capacitance, oscillator jitter,
 * leakage, or analog noise. They only validate the digital control shell.
 */
`default_nettype none

module analog_experiment_stub
(
    input  wire       clk,
    input  wire       rst_n,
    input  wire [7:0] reg_ctrl,
    input  wire [7:0] reg_src,
    input  wire [7:0] reg_div,
    input  wire [7:0] reg_mode,
    input  wire [7:0] reg_oscen,
    input  wire [7:0] reg_status,
    input  wire [7:0] reg_rawlo,
    input  wire [7:0] reg_rawhi,
    input  wire       trng_bit,
    inout  wire [7:0] ua
);

    /* Leave the analog pins high-Z in the digital stub. The custom analog
     * layout is expected to connect the real circuits to ua[5:0]. */
    assign ua[5:0] = 6'bzzzzzz;
    assign ua[7:6] = 2'bzz;

    /* Keep the intended control/status hooks visible without adding logic. */
    wire _unused_ok;
    assign _unused_ok = &{
        clk,
        rst_n,
        reg_ctrl,
        reg_src,
        reg_div,
        reg_mode,
        reg_oscen,
        reg_status,
        reg_rawlo,
        reg_rawhi,
        trng_bit,
        ua[5:0]
    };

endmodule

`default_nettype wire
