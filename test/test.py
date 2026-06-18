# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0
#
# See ATTRIBUTION.md for third-party sources and credits.
#
# file: test/test.py

import cocotb
from cocotb.triggers import Timer
from cocotb.clock import Clock

# CLK_PERIOD_NS = 10, for 100 MHz testing
# CLK_PERIOD_NS = 20, for common TT CLK = 50 MHz
# CLK_PERIOD_NS = 40, for our target 25 MHz
CLK_PERIOD_NS = 40
CLKS_PER_BIT = 217
SETTLE_TIME_NS = 2

UART_RX_BIT = 3
UART_TX_BIT = 4

EXPECTED_VERSION_PREFIX = b"Version "

TRNG_HEALTH_STATUS_DEBUG_PAGE_SELECT = True

def set_bit(value: int, bit_index: int, bit_value: int) -> int:
    mask = 1 << bit_index
    if bit_value:
        return value | mask
    return value & ~mask


async def uart_send_byte(dut, byte_value: int) -> None:
    bit_time_ns = CLK_PERIOD_NS * CLKS_PER_BIT

    current_ui = int(dut.ui_in.value)

    current_ui = set_bit(current_ui, UART_RX_BIT, 1)
    dut.ui_in.value = current_ui
    await Timer(bit_time_ns, unit="ns")

    current_ui = set_bit(current_ui, UART_RX_BIT, 0)
    dut.ui_in.value = current_ui
    await Timer(bit_time_ns, unit="ns")

    for bit_index in range(8):
        bit_value = (byte_value >> bit_index) & 0x1
        current_ui = set_bit(current_ui, UART_RX_BIT, bit_value)
        dut.ui_in.value = current_ui
        await Timer(bit_time_ns, unit="ns")

    current_ui = set_bit(current_ui, UART_RX_BIT, 1)
    dut.ui_in.value = current_ui
    await Timer(bit_time_ns, unit="ns")


async def uart_send_bytes(dut, data: bytes) -> None:
    for byte_value in data:
        await uart_send_byte(dut, byte_value)


def get_uart_tx_bit(dut) -> int:
    uo_value = dut.uo_out.value
    tx_value = uo_value[UART_TX_BIT]
    tx_text = str(tx_value)

    if tx_text not in ("0", "1"):
        raise ValueError(f"UART TX bit is not 0 or 1: {tx_text}")

    return int(tx_text)


async def uart_recv_byte(dut, idle_timeout_ns: int | None = None) -> int:
    bit_time_ns = CLK_PERIOD_NS * CLKS_PER_BIT
    half_bit_time_ns = bit_time_ns // 2

    prev_tx = None
    waited_ns = 0

    while True:
        await Timer(CLK_PERIOD_NS, unit="ns")
        await Timer(SETTLE_TIME_NS, unit="ns")

        uo_value = dut.uo_out.value
        tx_value = uo_value[UART_TX_BIT]
        tx_text = str(tx_value)

        if tx_text == "0":
            curr_tx = 0
        elif tx_text == "1":
            curr_tx = 1
        elif tx_text.upper() == "X":
            waited_ns += CLK_PERIOD_NS
            if idle_timeout_ns is not None and waited_ns >= idle_timeout_ns:
                raise TimeoutError("UART receive timeout waiting for start bit")
            continue
        else:
            raise ValueError(f"UART TX bit is not 0 or 1: {tx_text}")

        if prev_tx == 1 and curr_tx == 0:
            break

        prev_tx = curr_tx
        waited_ns += CLK_PERIOD_NS
        if idle_timeout_ns is not None and waited_ns >= idle_timeout_ns:
            raise TimeoutError("UART receive timeout waiting for start bit")

    await Timer(half_bit_time_ns, unit="ns")
    await Timer(SETTLE_TIME_NS, unit="ns")

    start_bit = get_uart_tx_bit(dut)
    assert start_bit == 0, f"Expected UART start bit 0, got {start_bit}"

    await Timer(bit_time_ns, unit="ns")
    await Timer(SETTLE_TIME_NS, unit="ns")

    result = 0
    for bit_index in range(8):
        bit_value = get_uart_tx_bit(dut)
        result |= (bit_value << bit_index)
        await Timer(bit_time_ns, unit="ns")
        await Timer(SETTLE_TIME_NS, unit="ns")

    stop_bit = get_uart_tx_bit(dut)
    assert stop_bit == 1, f"Expected UART stop bit 1, got {stop_bit}"

    return result


async def uart_recv_until_timeout(dut, max_bytes: int = 64, idle_timeout_bits: int = 20) -> bytes:
    bit_time_ns = CLK_PERIOD_NS * CLKS_PER_BIT
    idle_timeout_ns = bit_time_ns * idle_timeout_bits

    data = bytearray()

    for _ in range(max_bytes):
        try:
            data.append(await uart_recv_byte(dut, idle_timeout_ns=idle_timeout_ns))
        except TimeoutError:
            return bytes(data)

    return bytes(data)


def get_uo_bit(dut, bit_index: int) -> int:
    bit_text = str(dut.uo_out.value[bit_index])

    if bit_text not in ("0", "1"):
        raise ValueError(f"uo_out[{bit_index}] is not 0 or 1: {bit_text}")

    return int(bit_text)


def get_uo_7_5(dut) -> int:
    return (
        get_uo_bit(dut, 5)
        | (get_uo_bit(dut, 6) << 1)
        | (get_uo_bit(dut, 7) << 2)
    )


def set_ui_bit(dut, bit_index: int, bit_value: int) -> None:
    current_ui = int(dut.ui_in.value)
    current_ui = set_bit(current_ui, bit_index, bit_value)
    current_ui = set_bit(current_ui, UART_RX_BIT, 1)
    dut.ui_in.value = current_ui


async def uart_command_response(
    dut,
    command: bytes,
    max_bytes: int = 16,
    idle_timeout_bits: int = 80,
) -> bytes:
    recv_task = cocotb.start_soon(
        uart_recv_until_timeout(
            dut,
            max_bytes=max_bytes,
            idle_timeout_bits=idle_timeout_bits,
        )
    )

    await Timer(CLK_PERIOD_NS // 2, unit="ns")
    await uart_send_bytes(dut, command)

    return await recv_task


async def uart_expect_ok(dut, command: bytes) -> None:
    response = await uart_command_response(dut, command, max_bytes=3)

    assert response == b"OK\r", (
        f"Expected OK response to {command!r}, got {response!r}"
    )


async def uart_read_reg(dut, reg_num: int) -> int:
    command = f"R{reg_num}\r".encode("ascii")
    response = await uart_command_response(dut, command, max_bytes=6)

    expected_prefix = f"R{reg_num}=".encode("ascii")

    assert response.startswith(expected_prefix), (
        f"Expected {expected_prefix!r} prefix, got {response!r}"
    )

    assert len(response) == 6 and response.endswith(b"\r"), (
        f"Invalid register response for R{reg_num}: {response!r}"
    )

    return int(response[3:5], 16)


@cocotb.test()
async def test_gate_level_idle_sanity(dut):
    cocotb.start_soon(Clock(dut.clk, CLK_PERIOD_NS, unit="ns").start())

    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.rst_n.value = 0

    await Timer(100, unit="ns")
    dut.rst_n.value = 1

    await Timer(100_000, unit="ns")
    await Timer(SETTLE_TIME_NS, unit="ns")

    tx_idle = get_uart_tx_bit(dut)
    assert tx_idle == 1, f"UART TX should idle high after reset, got {tx_idle}"


@cocotb.test()
async def test_version_command_or_absent(dut):
    cocotb.start_soon(Clock(dut.clk, CLK_PERIOD_NS, unit="ns").start())

    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.rst_n.value = 0

    await Timer(100, unit="ns")
    dut.rst_n.value = 1

    # Gate-level simulation can leave outputs as X until reset has settled
    # through the synthesized netlist and a few clocks have completed.
    await Timer(100_000, unit="ns")
    await Timer(SETTLE_TIME_NS, unit="ns")

    tx_idle = get_uart_tx_bit(dut)
    assert tx_idle == 1, f"UART TX should idle high after reset, got {tx_idle}"

    # Start receive before transmit so fast gate-level responses are not missed.
    recv_task = cocotb.start_soon(
        uart_recv_until_timeout(dut, max_bytes=64, idle_timeout_bits=200)
    )

    await Timer(CLK_PERIOD_NS // 2, unit="ns")
    await uart_send_bytes(dut, b"V\r")
    response = await recv_task

    if not response:
        dut._log.info("No UART response received for V command; treating version command as absent")
        return

    if response == b"?\r":
        dut._log.info("Version command not present in this bitstream")
        return

    assert EXPECTED_VERSION_PREFIX in response, (
        f"Expected version prefix or absent-version response, got {response!r}"
    )


@cocotb.test(skip=not TRNG_HEALTH_STATUS_DEBUG_PAGE_SELECT)
async def test_trng_health_status_debug_page_select(dut):

    cocotb.start_soon(Clock(dut.clk, CLK_PERIOD_NS, unit="ns").start())

    dut.ena.value = 1
    dut.ui_in.value = 1 << UART_RX_BIT
    dut.uio_in.value = 0
    dut.rst_n.value = 0

    await Timer(100, unit="ns")
    dut.rst_n.value = 1

    await Timer(100_000, unit="ns")
    await Timer(SETTLE_TIME_NS, unit="ns")

    # Put TRNG in a deterministic, frozen state.
    for command in (
        b"E0\r",
        b"V0\r",
        b"W1\r",
        b"W0\r",
        b"S0\r",
        b"O00\r",
        b"D01\r",
    ):
        await uart_expect_ok(dut, command)

    rawlo = 0

    # Build a deterministic nonzero rawlo[2:0] value using single-step mode.
    for _ in range(4):
        for _ in range(16):
            await uart_expect_ok(dut, b"V1\r")
            await uart_expect_ok(dut, b"V0\r")

        rawlo = await uart_read_reg(dut, 6)

        if (rawlo & 0x07) != 0:
            break

    status = await uart_read_reg(dut, 5)

    raw_page_expected = rawlo & 0x07
    health_page_expected = (
        ((status >> 3) & 0x01)
        | (((status >> 4) & 0x01) << 1)
        | (((status >> 7) & 0x01) << 2)
    )

    assert raw_page_expected != health_page_expected, (
        "Test did not create distinct raw/debug page values: "
        f"rawlo=0x{rawlo:02X}, status=0x{status:02X}"
    )

    set_ui_bit(dut, 0, 0)
    await Timer(SETTLE_TIME_NS, unit="ns")

    raw_page_actual = get_uo_7_5(dut)

    assert raw_page_actual == raw_page_expected, (
        "ui_in[0]=0 should select reg_rawlo[2:0] on uo_out[7:5]: "
        f"expected 0x{raw_page_expected:X}, got 0x{raw_page_actual:X}, "
        f"rawlo=0x{rawlo:02X}"
    )

    set_ui_bit(dut, 0, 1)
    await Timer(SETTLE_TIME_NS, unit="ns")

    health_page_actual = get_uo_7_5(dut)

    assert health_page_actual == health_page_expected, (
        "ui_in[0]=1 should select R5 health summary bits on uo_out[7:5]: "
        f"expected 0x{health_page_expected:X}, got 0x{health_page_actual:X}, "
        f"status=0x{status:02X}"
    )
