/*
 * Copyright (c) 2026 gojimmypi
 * SPDX-License-Identifier: Apache-2.0
 *
 * See ATTRIBUTION.md for third-party sources and credits.
 *
 * file: analog_experiment_stub.v
 *
 * GF 0p3 analog experiment pad exerciser.
 *
 * This block replaces the original high-Z placeholder with a small,
 * FPGA-safe mixed-signal experiment that uses all six GF 0p3 analog pins.
 * It is intentionally simple Verilog so it can still be built by the same
 * Tiny Tapeout/FPGA flows as the UART/SPI/TRNG control shell.
 *
 * Important limitation:
 * - This is not a precision analog macro and it is not a substitute for
 *   GF180 schematic/layout/SPICE/PEX work.
 * - The output pins are standard digital 0/1/Z drives that are useful when
 *   connected to external RC filters, scopes, counters, or Analog Discovery.
 * - The input pins are sampled through ordinary CMOS input thresholds, which
 *   is useful for threshold/noise experiments but not a real comparator model.
 * - The analog GDS patch flow adds one small real on-chip passive structure on ua[5]:
 *   a Metal4 pickup/fringe capacitor tied to the puf_probe pad and nearby
 *   grounded Metal4.  This RTL exercises that physical structure with the
 *   same charge/release/sample sequence used for external RC experiments.
 *
 * Analog pin roles:
 * - ua[0]: ain_ext       high-Z input, sampled by the CMOS threshold
 * - ua[1]: dac_out       1-bit sigma-delta DAC output; RC-filter externally
 * - ua[2]: cmp_ref_ext   high-Z input, sampled by the CMOS threshold
 * - ua[3]: amon_out      monitor mux output
 * - ua[4]: osc_out       clock-divider/TRNG monitor output
 * - ua[5]: puf_probe     charge/release/sample probe pad with GDS-level Metal4 passive
 *
 * Control through the existing UART/SPI registers:
 * - R0/reg_ctrl[0]       global analog enable, via E1/E0
 * - R0/reg_ctrl[1]       invert driven analog outputs, via V1/V0
 * - R0/reg_ctrl[2]       puf_probe discharge polarity, via W1/W0
 * - R1/reg_src[1:0]      DAC source select
 *                         0: reg_div[4:0]
 *                         1: reg_rawlo[4:0]
 *                         2: reg_rawhi[4:0]
 *                         3: entropy mix from raw bytes and trng_bit
 * - R2/reg_div           DAC code in [4:0] and osc divider reload value
 * - R3/reg_mode[2:0]     amon_out mux select
 *                         0: dac_out bit
 *                         1: ain_ext sampled threshold
 *                         2: cmp_ref_ext sampled threshold
 *                         3: ain_ext & ~cmp_ref_ext threshold compare
 *                         4: puf_probe sampled threshold
 *                         5: trng_bit
 *                         6: osc_out bit
 *                         7: reg_status[0]
 * - R3/reg_mode[4:3]     puf_probe charge/release/sample timing scale
 * - R3/reg_mode[5]       osc_out source: 0 = local divider, 1 = trng_bit
 * - R4/reg_oscen[0]      enable ua[1] dac_out driver
 * - R4/reg_oscen[1]      enable ua[3] amon_out driver
 * - R4/reg_oscen[2]      enable ua[4] osc_out driver
 * - R4/reg_oscen[3]      enable ua[5] puf_probe charge/release driver
 * - R14/0xE             read analog status through UART/SPI
 * - R15/0xF             read latest puf_probe threshold/decay timing sample
 *                         bit 0: sampled ua[0]
 *                         bit 1: sampled ua[2]
 *                         bit 2: ua[0] & ~ua[2] threshold compare
 *                         bit 3: live sampled ua[5]
 *                         bit 4: latched ua[5] probe sample
 *                         bit 5: current sigma-delta bit
 *                         bit 6: current osc/TRNG monitor bit
 *                         bit 7: puf_probe driver enabled
 * - R15/0xF             puf_probe threshold/decay timing
 *                         00: no threshold crossing observed yet
 *                         01..FE: cycles from release to CMOS threshold crossing
 *                         FF: saturated/no crossing before timeout
 *
 * Example bring-up commands:
 * - E1, D10, O01          enable half-scale sigma-delta DAC on ua[1]
 * - E1, D08, M00, O03     enable DAC and monitor DAC bit on ua[3]
 * - E1, M03, O02          monitor sampled ain_ext & ~cmp_ref_ext on ua[3]
 * - E1, D20, M00, O05     enable DAC plus divided-clock output on ua[4]
 * - E1, M18, O08          run puf_probe charge/release/sample sequence
 * - RF                     read latest ua[5] passive-structure decay timing sample
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
    output wire [7:0] analog_status,
    output wire [7:0] analog_measure,
    inout  wire [7:0] ua
);

    wire       analog_enable;
    wire       analog_invert;
    wire       probe_discharge;
    wire [1:0] dac_src_sel;
    wire [2:0] amon_sel;
    wire [1:0] probe_rate_sel;
    wire       osc_src_trng;
    wire       dac_pin_oe;
    wire       amon_pin_oe;
    wire       osc_pin_oe;
    wire       probe_pin_enable;
    wire [4:0] dac_code;
    wire [5:0] dac_sum;
    wire [7:0] osc_reload;
    wire       cmp_threshold;
    wire       amon_mux;
    wire       dac_pin_out;
    wire       amon_pin_out;
    wire       osc_pin_out;

    reg        ain_meta;
    reg        ain_sync;
    reg        ref_meta;
    reg        ref_sync;
    reg        probe_meta;
    reg        probe_sync;

    reg  [4:0] dac_accum;
    reg        dac_out_q;

    reg  [7:0] osc_ctr;
    reg        osc_out_q;

    reg  [7:0] probe_ctr;
    reg  [7:0] probe_decay_ctr_q;
    reg  [7:0] probe_decay_q;
    reg        probe_decay_active_q;
    reg        probe_drive_oe_q;
    reg        probe_drive_q;
    reg        probe_sample_q;
    reg  [1:0] probe_phase;
    reg  [1:0] probe_phase_q;

    assign analog_enable    = reg_ctrl[0];
    assign analog_invert    = reg_ctrl[1];
    assign probe_discharge  = reg_ctrl[2];
    assign dac_src_sel      = reg_src[1:0];
    assign amon_sel         = reg_mode[2:0];
    assign probe_rate_sel   = reg_mode[4:3];
    assign osc_src_trng     = reg_mode[5];

    assign dac_pin_oe       = analog_enable & reg_oscen[0];
    assign amon_pin_oe      = analog_enable & reg_oscen[1];
    assign osc_pin_oe       = analog_enable & reg_oscen[2];
    assign probe_pin_enable = analog_enable & reg_oscen[3];

    assign dac_code = (dac_src_sel == 2'd1) ? reg_rawlo[4:0] :
                      (dac_src_sel == 2'd2) ? reg_rawhi[4:0] :
                      (dac_src_sel == 2'd3) ? ({reg_rawhi[1:0], reg_rawlo[2:0]} ^ {4'b0000, trng_bit}) :
                                             reg_div[4:0];

    assign dac_sum = {1'b0, dac_accum} + {1'b0, dac_code};

    assign osc_reload = (reg_div == 8'h00) ? 8'h01 : reg_div;

    assign cmp_threshold = ain_sync & ~ref_sync;

    assign amon_mux = (amon_sel == 3'd1) ? ain_sync :
                      (amon_sel == 3'd2) ? ref_sync :
                      (amon_sel == 3'd3) ? cmp_threshold :
                      (amon_sel == 3'd4) ? probe_sample_q :
                      (amon_sel == 3'd5) ? trng_bit :
                      (amon_sel == 3'd6) ? (osc_src_trng ? trng_bit : osc_out_q) :
                      (amon_sel == 3'd7) ? reg_status[0] :
                                           dac_out_q;

    assign dac_pin_out  = dac_out_q ^ analog_invert;
    assign amon_pin_out = amon_mux ^ analog_invert;
    assign osc_pin_out  = (osc_src_trng ? trng_bit : osc_out_q) ^ analog_invert;

    assign analog_status = {
        probe_drive_oe_q,
        (osc_src_trng ? trng_bit : osc_out_q),
        dac_out_q,
        probe_sample_q,
        probe_sync,
        cmp_threshold,
        ref_sync,
        ain_sync
    };

    assign analog_measure = probe_decay_q;

    assign ua[0] = 1'bz;
    assign ua[1] = dac_pin_oe ? dac_pin_out : 1'bz;
    assign ua[2] = 1'bz;
    assign ua[3] = amon_pin_oe ? amon_pin_out : 1'bz;
    assign ua[4] = osc_pin_oe ? osc_pin_out : 1'bz;
    assign ua[5] = (probe_pin_enable & probe_drive_oe_q) ? probe_drive_q : 1'bz;

    wire [1:0] unused_ua;
    assign unused_ua = ua[7:6];

    always @(*) begin
        case (probe_rate_sel)
            2'd0: probe_phase = probe_ctr[3:2];
            2'd1: probe_phase = probe_ctr[5:4];
            2'd2: probe_phase = probe_ctr[7:6];
            default: probe_phase = {probe_ctr[7], probe_ctr[5]};
        endcase
    end

    always @(posedge clk) begin
        if (!rst_n) begin
            ain_meta         <= 1'b0;
            ain_sync         <= 1'b0;
            ref_meta         <= 1'b0;
            ref_sync         <= 1'b0;
            probe_meta       <= 1'b0;
            probe_sync       <= 1'b0;
            dac_accum        <= 5'd0;
            dac_out_q        <= 1'b0;
            osc_ctr          <= 8'h00;
            osc_out_q        <= 1'b0;
            probe_ctr            <= 8'h00;
            probe_decay_ctr_q    <= 8'h00;
            probe_decay_q        <= 8'h00;
            probe_decay_active_q <= 1'b0;
            probe_drive_oe_q     <= 1'b0;
            probe_drive_q        <= 1'b0;
            probe_sample_q       <= 1'b0;
            probe_phase_q        <= 2'd0;
        end else begin
            ain_meta   <= ua[0];
            ain_sync   <= ain_meta;
            ref_meta   <= ua[2];
            ref_sync   <= ref_meta;
            probe_meta <= ua[5];
            probe_sync <= probe_meta;

            if (dac_pin_oe) begin
                dac_accum <= dac_sum[4:0];
                dac_out_q <= dac_sum[5];
            end else begin
                dac_accum <= 5'd0;
                dac_out_q <= 1'b0;
            end

            if (osc_pin_oe && !osc_src_trng) begin
                if (osc_ctr >= osc_reload) begin
                    osc_ctr   <= 8'h00;
                    osc_out_q <= ~osc_out_q;
                end else begin
                    osc_ctr <= osc_ctr + 8'h01;
                end
            end else begin
                osc_ctr   <= 8'h00;
                osc_out_q <= 1'b0;
            end

            if (probe_pin_enable) begin
                probe_ctr     <= probe_ctr + 8'h01;
                probe_phase_q <= probe_phase;

                case (probe_phase)
                    2'd0: begin
                        probe_drive_oe_q     <= 1'b1;
                        probe_drive_q        <= ~probe_discharge;
                        probe_decay_ctr_q    <= 8'h00;
                        probe_decay_active_q <= 1'b0;
                    end
                    2'd1: begin
                        probe_drive_oe_q <= 1'b0;
                        probe_drive_q    <= ~probe_discharge;

                        if (probe_phase_q != 2'd1) begin
                            probe_decay_ctr_q    <= 8'h00;
                            probe_decay_active_q <= 1'b1;
                        end else if (probe_decay_active_q) begin
                            if (probe_sync != ~probe_discharge) begin
                                probe_decay_q        <= probe_decay_ctr_q;
                                probe_decay_active_q <= 1'b0;
                            end else if (probe_decay_ctr_q != 8'hff) begin
                                probe_decay_ctr_q <= probe_decay_ctr_q + 8'h01;
                            end else begin
                                probe_decay_q        <= 8'hff;
                                probe_decay_active_q <= 1'b0;
                            end
                        end
                    end
                    2'd2: begin
                        probe_drive_oe_q <= 1'b0;
                        probe_drive_q    <= ~probe_discharge;
                        probe_sample_q   <= probe_sync;

                        if (probe_decay_active_q) begin
                            probe_decay_q        <= probe_decay_ctr_q;
                            probe_decay_active_q <= 1'b0;
                        end
                    end
                    default: begin
                        probe_drive_oe_q     <= 1'b1;
                        probe_drive_q        <= probe_discharge;
                        probe_decay_active_q <= 1'b0;
                    end
                endcase
            end else begin
                probe_ctr            <= 8'h00;
                probe_decay_ctr_q    <= 8'h00;
                probe_decay_active_q <= 1'b0;
                probe_drive_oe_q     <= 1'b0;
                probe_drive_q        <= 1'b0;
                probe_sample_q       <= probe_sync;
                probe_phase_q        <= 2'd0;
            end
        end
    end

    wire _unused_ok;
    assign _unused_ok = &{
        unused_ua,
        reg_ctrl[7:3],
        reg_src[7:2],
        reg_mode[7:6],
        reg_oscen[7:4],
        reg_status[7:1],
        reg_rawlo[7:5],
        reg_rawhi[7:5]
    };

endmodule

`default_nettype wire
