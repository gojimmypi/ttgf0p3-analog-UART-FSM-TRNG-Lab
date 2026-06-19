/*
 * Copyright (c) 2026 gojimmypi
 * SPDX-License-Identifier: Apache-2.0
 *
 * See ATTRIBUTION.md for third-party sources and credits.
 *
 * file: ./ulx3s/ESP32/main/ulx3s_spi_lib.c
 *
 * ESP32 ulx3s_spi_lib FPGA SPI library
 *
 */

#include "ulx3s_spi_lib.h"

#include <stdint.h>
#include <string.h>

#include "driver/spi_master.h"
#include "esp_log.h"

#ifndef ULX3S_SPI_HOST
#define ULX3S_SPI_HOST      SPI2_HOST
#endif

/* Prior testing SPI pins disabled: */
#if 0
    #define PIN_NUM_MISO        19
    #define PIN_NUM_MOSI        23
    #define PIN_NUM_CLK         18
    #define PIN_NUM_CS          5
#endif

#define PIN_NUM_MISO        2
#define PIN_NUM_MOSI        15
#define PIN_NUM_CLK         14
#define PIN_NUM_CS          13

#define SPI_CLOCK_HZ        1000000

#define TT_SPI_READ_FLAG    0x80U

/* Generated defined from src/project_config.v
 *   ./show_effective_defines.sh  ../src/project_config.v  --header tt_effective_defines.h
 */
#include "tt_effective_defines.h"

#ifdef TT_MACRO_BIG16_SPI_REG
    #define TT_SPI_ADDR_MASK    0x0FU
#else
    #define TT_SPI_ADDR_MASK    0x07U
#endif

static const char* const TAG = "ulx3s_spi";
static spi_device_handle_t ulx3s_spi;

/*
*  Initialize the SPI on the ULX3S ESP32
*/
esp_err_t ulx3s_spi_init(bool verbose)
{
    esp_err_t ret;

    spi_bus_config_t buscfg;
    spi_device_interface_config_t devcfg;

    if (verbose) {
        ESP_LOGI(TAG, "--------------------------------------------------------");
        ESP_LOGI(TAG, "SPI Config:");
        ESP_LOGI(TAG, "--------------------------------------------------------");
#ifdef ULX3S_SPI_HOST
        switch (ULX3S_SPI_HOST)
        {
        case SPI1_HOST:
            ESP_LOGI(TAG, "ULX3S_SPI_HOST: %s (%d)", "SPI1_HOST", SPI1_HOST);
            break;

        case SPI2_HOST:
            ESP_LOGI(TAG, "ULX3S_SPI_HOST: %s (%d)", "SPI2_HOST", SPI2_HOST);
            break;

        case SPI3_HOST:
            ESP_LOGI(TAG, "ULX3S_SPI_HOST: %s (%d)", "SPI3_HOST", SPI3_HOST);
            break;

        default:
            ESP_LOGW(TAG, "ULX3S_SPI_HOST: %s (%d)", "Unknown", ULX3S_SPI_HOST);
            break;
        }
#else 
        ESP_LOGE(TAG, "ULX3S_SPI_HOST not defined!");
#endif
        ESP_LOGI(TAG, "SPI_CLOCK_HZ:   %d", SPI_CLOCK_HZ);
        ESP_LOGI(TAG, "PIN_NUM_CS:     %d", PIN_NUM_CS);
        ESP_LOGI(TAG, "PIN_NUM_MISO:   %d", PIN_NUM_MISO);
        ESP_LOGI(TAG, "PIN_NUM_MOSI:   %d", PIN_NUM_MOSI);
        ESP_LOGI(TAG, "PIN_NUM_CLK:    %d", PIN_NUM_CLK);
        ESP_LOGI(TAG, "--------------------------------------------------------");
    } /* verbose */

    memset(&buscfg, 0, sizeof(buscfg));
    memset(&devcfg, 0, sizeof(devcfg));

    buscfg.miso_io_num = PIN_NUM_MISO;
    buscfg.mosi_io_num = PIN_NUM_MOSI;
    buscfg.sclk_io_num = PIN_NUM_CLK;
    buscfg.quadwp_io_num = -1;
    buscfg.quadhd_io_num = -1;
    buscfg.max_transfer_sz = 32;

    devcfg.clock_speed_hz = SPI_CLOCK_HZ;
    devcfg.mode = 0;
    devcfg.spics_io_num = PIN_NUM_CS;
    devcfg.queue_size = 1;

    ret = spi_bus_initialize(ULX3S_SPI_HOST, &buscfg, SPI_DMA_DISABLED);
    if (ret != ESP_OK) {
        ESP_LOGE(TAG, "spi_bus_initialize failed: %s", esp_err_to_name(ret));
        return ret;
    }

    ret = spi_bus_add_device(ULX3S_SPI_HOST, &devcfg, &ulx3s_spi);
    if (ret != ESP_OK) {
        ESP_LOGE(TAG, "spi_bus_add_device failed: %s", esp_err_to_name(ret));
        return ret;
    }

    return ESP_OK;
}

/*
*  Send data to the TT SPI from the ULX3S ESP32
*/
static esp_err_t ulx3s_spi_transfer(
    const uint8_t* tx_buf,
    uint8_t* rx_buf,
    size_t len)
{
    spi_transaction_t trans;
    esp_err_t ret;

    memset(&trans, 0, sizeof(trans));

    trans.length = len * 8U;
    trans.tx_buffer = tx_buf;
    trans.rx_buffer = rx_buf;

    ret = spi_device_transmit(ulx3s_spi, &trans);
    if (ret != ESP_OK) {
        ESP_LOGE(TAG, "spi_device_transmit failed: %s", esp_err_to_name(ret));
    }

    return ret;
}

#if 0
static void ulx3s_spi_test_once(void)
{
    esp_err_t ret;

    /*
     * Byte 0 is command.
     * Byte 1 is payload or dummy clocks for readback.
     *
     * With many simple SPI slaves, rx[0] is old/stale.
     * The useful response often appears in rx[1] or later.
     */
    uint8_t tx_buf[2];
    uint8_t rx_buf[2];

    tx_buf[0] = 0x52U;  /* Example command, ASCII 'R' */
    tx_buf[1] = 0x00U;  /* Dummy byte to clock response */

    rx_buf[0] = 0x00U;
    rx_buf[1] = 0x00U;

    ret = ulx3s_spi_transfer(tx_buf, rx_buf, sizeof(tx_buf));
    if (ret != ESP_OK) {
        return;
    }

    ESP_LOGI(TAG, "tx: %02X %02X  rx: %02X %02X",
             tx_buf[0], tx_buf[1],
             rx_buf[0], rx_buf[1]);
}
#endif /* conditional ulx3s_spi_test_once()  */

/*
*  Read data from the TT SPI on the ULX3S ESP32
*/
esp_err_t ulx3s_spi_read_reg(
    uint8_t addr,
    uint8_t* value)
{
    esp_err_t ret;
    uint8_t tx_buf[2];
    uint8_t rx_buf[2];

    if (value == NULL) {
        ESP_LOGE(TAG, "ulx3s_spi_read_reg: invalid argument");
        return ESP_ERR_INVALID_ARG;
    }

    tx_buf[0] = TT_SPI_READ_FLAG | (addr & TT_SPI_ADDR_MASK);
    tx_buf[1] = 0x00U;

    rx_buf[0] = 0x00U;
    rx_buf[1] = 0x00U;

    ret = ulx3s_spi_transfer(tx_buf, rx_buf, sizeof(tx_buf));
    if (ret != ESP_OK) {
        ESP_LOGE(TAG, "ulx3s_spi_transfer failed: %s", esp_err_to_name(ret));
        return ret;
    }

    /*
     * The first response byte is not the requested register value.
     * The slave loads the selected register after the command byte,
     * then clocks it out during the second byte.
     */
    *value = rx_buf[1];

    return ESP_OK;
}

/*
*  Send register data to the TT SPI on the ULX3S ESP32
*/
esp_err_t ulx3s_spi_write_reg(
    uint8_t addr,
    uint8_t value)
{
#if (ULX3S_SPI_WRITE_MODE != ULX3S_SPI_WRITE_MODE_MONITOR_ONLY)
    uint8_t tx_buf[2];
    uint8_t rx_buf[2];

    tx_buf[0] = addr & TT_SPI_ADDR_MASK;
    tx_buf[1] = value;

    rx_buf[0] = 0x00U;
    rx_buf[1] = 0x00U;

    return ulx3s_spi_transfer(tx_buf, rx_buf, sizeof(tx_buf));
#else
    ESP_LOGW(TAG, "ulx3s_spi_write_reg: write disabled by compile-time flag");
    return ESP_ERR_INVALID_STATE;
#endif /* conditional ULX3S_SPI_WRITE_MODE != ULX3S_SPI_WRITE_MODE_MONITOR_ONLY */
}

/*
*  Read register data from the TT SPI on the ULX3S ESP32
*/
esp_err_t ulx3s_spi_read_regs(uint8_t regs[ULX3S_SPI_REG_COUNT])
{
    esp_err_t ret;
    uint8_t addr;

    if (regs == NULL) {
        ESP_LOGE(TAG, "ulx3s_spi_read_regs: invalid argument");
        return ESP_ERR_INVALID_ARG;
    }

    for (addr = 0U; addr < ULX3S_SPI_REG_COUNT; addr++) {
        ret = ulx3s_spi_read_reg(addr, &regs[addr]);
        if (ret != ESP_OK) {
            ESP_LOGE(TAG, "ulx3s_spi_read_reg failed: %s", esp_err_to_name(ret));
            return ret;
        }
    }

    return ESP_OK;
}

/*
*  View TT SPI registers from the SPI on the ULX3S ESP32
*/
void ulx3s_spi_log_regs(const uint8_t regs[ULX3S_SPI_REG_COUNT])
{
    uint16_t raw;

    raw = ((uint16_t)regs[TT_REG_RAWHI] << 8) | regs[TT_REG_RAWLO];

    ESP_LOGI(TAG,
             "SPI regs: R0=%02X R1=%02X R2=%02X R3=%02X R4=%02X R5=%02X R6=%02X R7=%02X",
             regs[0],
             regs[1],
             regs[2],
             regs[3],
             regs[4],
             regs[5],
             regs[6],
             regs[7]);

#ifdef FPGA_TRNG_BIG16_SPI_REG
    ESP_LOGI(TAG,
        "SPI regs: R8=%02X R9=%02X RA=%02X RB=%02X RC=%02X RD=%02X RE=%02X RF=%02X",
        regs[8],
        regs[9],
        regs[10],
        regs[11],
        regs[12],
        regs[13],
        regs[14],
        regs[15]);

    ESP_LOGI(TAG,
        "raw=0x%04X status=0x%02X src=%u div=0x%02X mode=0x%02X oscen=0x%02X ui=0x%02X uo=0x%02X uio_in=0x%02X uio_out=0x%02X uio_oe=0x%02X",
        raw,
        regs[TT_REG_STATUS],
        regs[TT_REG_SRC],
        regs[TT_REG_DIV],
        regs[TT_REG_MODE],
        regs[TT_REG_OSCEN],
        regs[TT_REG_UI_IN],
        regs[TT_REG_UO_OUT],
        regs[TT_REG_UIO_IN],
        regs[TT_REG_UIO_OUT],
        regs[TT_REG_UIO_OE]);
#else
    ESP_LOGI(TAG,
        "raw=0x%04X status=0x%02X src=%u div=0x%02X mode=0x%02X oscen=0x%02X",
        raw,
        regs[TT_REG_STATUS],
        regs[TT_REG_SRC],
        regs[TT_REG_DIV],
        regs[TT_REG_MODE],
        regs[TT_REG_OSCEN]);
#endif
}


/*
*  Reset TT SPI Registers
*/
esp_err_t ulx3s_spi_reset_config_registers(void)
{
    esp_err_t ret;

    ret = ulx3s_spi_write_reg(TT_REG_CTRL, ULX3S_REG_CTRL_DEFAULT);
    if (ret != ESP_OK) {
        ESP_LOGE(TAG, "failed to reset R0: %s", esp_err_to_name(ret));
        return ret;
    }

    ret = ulx3s_spi_write_reg(TT_REG_SRC, ULX3S_REG_SRC_DEFAULT);
    if (ret != ESP_OK) {
        ESP_LOGE(TAG, "failed to reset R1: %s", esp_err_to_name(ret));
        return ret;
    }

    ret = ulx3s_spi_write_reg(TT_REG_DIV, ULX3S_REG_DIV_DEFAULT);
    if (ret != ESP_OK) {
        ESP_LOGE(TAG, "failed to reset R2: %s", esp_err_to_name(ret));
        return ret;
    }

    ret = ulx3s_spi_write_reg(TT_REG_MODE, ULX3S_REG_MODE_DEFAULT);
    if (ret != ESP_OK) {
        ESP_LOGE(TAG, "failed to reset R3: %s", esp_err_to_name(ret));
        return ret;
    }

    ret = ulx3s_spi_write_reg(TT_REG_OSCEN, ULX3S_REG_OSCEN_DEFAULT);
    if (ret != ESP_OK) {
        ESP_LOGE(TAG, "failed to reset R4: %s", esp_err_to_name(ret));
        return ret;
    }

    return ESP_OK;
}

/*
*  Self check diagnostics
*/
#define ULX3S_SPI_SELF_CHECK_RAW_SAMPLES        8U
#define ULX3S_SPI_SELF_CHECK_RAW_DELAY_MS       10U

#ifndef ULX3S_REG_STATUS_EXPECTED
#define ULX3S_REG_STATUS_EXPECTED           0x3CU
#endif

typedef enum {
    ULX3S_SPI_CHECK_EQUAL = 0,
    ULX3S_SPI_CHECK_MASK,
    ULX3S_SPI_CHECK_LOG_ONLY
} ulx3s_spi_check_type_t;

typedef struct {
    uint8_t addr;
    const char* name;
    uint8_t expected;
    uint8_t mask;
    ulx3s_spi_check_type_t type;
} ulx3s_spi_reg_check_t;

static unsigned int ulx3s_spi_check_reg_value(
    const uint8_t regs[ULX3S_SPI_REG_COUNT],
    const ulx3s_spi_reg_check_t* check)
{
    uint8_t actual;
    uint8_t actual_masked;
    uint8_t expected_masked;

    actual = regs[check->addr];

    if (check->type == ULX3S_SPI_CHECK_LOG_ONLY) {
        ESP_LOGI(TAG, "SPI self-check INFO %s: %02X", check->name, actual);
        return 0U;
    }

    if (check->type == ULX3S_SPI_CHECK_MASK) {
        actual_masked = actual & check->mask;
        expected_masked = check->expected & check->mask;

        if (actual_masked != expected_masked) {
            ESP_LOGE(TAG,
                "SPI self-check FAIL %s: expected mask %02X value %02X, actual %02X",
                check->name,
                check->mask,
                expected_masked,
                actual);
            return 1U;
        }

        ESP_LOGI(TAG,
            "SPI self-check PASS %s: actual %02X mask %02X value %02X",
            check->name,
            actual,
            check->mask,
            expected_masked);
        return 0U;
    }

    if (actual != check->expected) {
        ESP_LOGE(TAG,
            "SPI self-check FAIL %s: expected %02X, actual %02X",
            check->name,
            check->expected,
            actual);
        return 1U;
    }

    ESP_LOGI(TAG, "SPI self-check PASS %s: %02X", check->name, actual);

    return 0U;
}

static esp_err_t ulx3s_spi_check_raw_changes(
    unsigned int* pass_count,
    unsigned int* fail_count)
{
    esp_err_t ret;
    uint8_t regs[ULX3S_SPI_REG_COUNT];
    uint16_t first_raw;
    uint16_t last_raw;
    uint16_t raw;
    uint8_t sample;
    uint8_t changed;

    ret = ulx3s_spi_read_regs(regs);
    if (ret != ESP_OK) {
        ESP_LOGE(TAG, "SPI self-check raw read failed: %s", esp_err_to_name(ret));
        return ret;
    }

    first_raw = ((uint16_t)regs[TT_REG_RAWHI] << 8) | regs[TT_REG_RAWLO];
    last_raw = first_raw;
    changed = 0U;

    for (sample = 1U; sample < ULX3S_SPI_SELF_CHECK_RAW_SAMPLES; sample++) {
        vTaskDelay(pdMS_TO_TICKS(ULX3S_SPI_SELF_CHECK_RAW_DELAY_MS));

        ret = ulx3s_spi_read_regs(regs);
        if (ret != ESP_OK) {
            ESP_LOGE(TAG, "SPI self-check raw read failed: %s", esp_err_to_name(ret));
            return ret;
        }

        raw = ((uint16_t)regs[TT_REG_RAWHI] << 8) | regs[TT_REG_RAWLO];
        last_raw = raw;

        if (raw != first_raw) {
            changed = 1U;
        }
    }

    if (changed == 0U) {
        ESP_LOGE(TAG,
            "SPI self-check FAIL R6/R7 raw: fixed at 0x%04X across %u samples",
            first_raw,
            ULX3S_SPI_SELF_CHECK_RAW_SAMPLES);
        (*fail_count)++;
        return ESP_FAIL;
    }

    ESP_LOGI(TAG,
        "SPI self-check PASS R6/R7 raw: first=0x%04X last=0x%04X samples=%u",
        first_raw,
        last_raw,
        ULX3S_SPI_SELF_CHECK_RAW_SAMPLES);

    (*pass_count)++;

    return ESP_OK;
}

esp_err_t ulx3s_spi_self_check_regs_once(void)
{
    esp_err_t ret;
    uint8_t regs[ULX3S_SPI_REG_COUNT];
    unsigned int pass_count;
    unsigned int fail_count;
    size_t index;

    static const ulx3s_spi_reg_check_t reg_checks[] = {
        { TT_REG_CTRL,   "R0 CTRL",     ULX3S_REG_CTRL_DEFAULT,   0xFFU, ULX3S_SPI_CHECK_EQUAL },
        { TT_REG_SRC,    "R1 SRC",      ULX3S_REG_SRC_DEFAULT,    0xFFU, ULX3S_SPI_CHECK_EQUAL },
        { TT_REG_DIV,    "R2 DIV",      ULX3S_REG_DIV_DEFAULT,    0xFFU, ULX3S_SPI_CHECK_EQUAL },
        { TT_REG_MODE,   "R3 MODE",     ULX3S_REG_MODE_DEFAULT,   0xFFU, ULX3S_SPI_CHECK_EQUAL },
        { TT_REG_OSCEN,  "R4 OSCEN",    ULX3S_REG_OSCEN_DEFAULT,  0xFFU, ULX3S_SPI_CHECK_EQUAL },
        { TT_REG_STATUS, "R5 STATUS",   ULX3S_REG_STATUS_EXPECTED, 0xFFU, ULX3S_SPI_CHECK_EQUAL },

        /*
         * R6/R7 are checked separately as a combined non-fixed raw value.
         */

#ifdef FPGA_TRNG_BIG16_SPI_REG
         /*
          * R8 depends on board inputs. Require UART RX idle high on ui_in[3].
          * Do not require exact R8 because other input pins can vary.
          */
         { TT_REG_UI_IN,    "R8 UI_IN UART_RX_IDLE", 0x08U, 0x08U, ULX3S_SPI_CHECK_MASK },

         /*
          * R9, RA, and RB are readable pin snapshots, but may include dynamic
          * output/debug/entropy-visible bits. Log them without exact matching.
          */
         { TT_REG_UO_OUT,   "R9 UO_OUT",             0x00U, 0x00U, ULX3S_SPI_CHECK_LOG_ONLY },
         { TT_REG_UIO_IN,   "RA UIO_IN",             0x00U, 0x00U, ULX3S_SPI_CHECK_LOG_ONLY },
         { TT_REG_UIO_OUT,  "RB UIO_OUT",            0x00U, 0x00U, ULX3S_SPI_CHECK_LOG_ONLY },

         /*
          * With SPI enabled, uio_oe should normally be F4:
          * uio[2] plus uio[7:4] outputs, uio[3:0] otherwise inputs.
          */
         { TT_REG_UIO_OE,   "RC UIO_OE",             0xF4U, 0xFFU, ULX3S_SPI_CHECK_EQUAL },

         /*
          * Unused readable addresses should return 00.
          */
         { TT_REG_UNUSED_D, "RD UNUSED",             0x00U, 0xFFU, ULX3S_SPI_CHECK_EQUAL },
         { TT_REG_UNUSED_E, "RE UNUSED",             0x00U, 0xFFU, ULX3S_SPI_CHECK_EQUAL },
         { TT_REG_UNUSED_F, "RF UNUSED",             0x00U, 0xFFU, ULX3S_SPI_CHECK_EQUAL },
 #endif
    };

    pass_count = 0U;
    fail_count = 0U;

    ESP_LOGI(TAG, "SPI self-check: reading all known registers");

    ret = ulx3s_spi_read_regs(regs);
    if (ret != ESP_OK) {
        ESP_LOGE(TAG, "SPI self-check failed to read registers: %s", esp_err_to_name(ret));
        return ret;
    }

    ulx3s_spi_log_regs(regs);

    for (index = 0U; index < (sizeof(reg_checks) / sizeof(reg_checks[0])); index++) {
        if (reg_checks[index].addr >= ULX3S_SPI_REG_COUNT) {
            ESP_LOGE(TAG,
                "SPI self-check FAIL %s: addr %u outside register count %u",
                reg_checks[index].name,
                reg_checks[index].addr,
                ULX3S_SPI_REG_COUNT);
            fail_count++;
            continue;
        }

        if (ulx3s_spi_check_reg_value(regs, &reg_checks[index]) == 0U) {
            if (reg_checks[index].type != ULX3S_SPI_CHECK_LOG_ONLY) {
                pass_count++;
            }
        }
        else {
            fail_count++;
        }
    }

    ret = ulx3s_spi_check_raw_changes(&pass_count, &fail_count);
    if ((ret != ESP_OK) && (ret != ESP_FAIL)) {
        return ret;
    }

#ifdef FPGA_TRNG_BIG16_SPI_REG
    ESP_LOGI(TAG,
        "SPI self-check pins: ui=0x%02X uo=0x%02X uio_in=0x%02X uio_out=0x%02X uio_oe=0x%02X",
        regs[TT_REG_UI_IN],
        regs[TT_REG_UO_OUT],
        regs[TT_REG_UIO_IN],
        regs[TT_REG_UIO_OUT],
        regs[TT_REG_UIO_OE]);
#endif

    if (fail_count != 0U) {
        ESP_LOGE(TAG,
            "SPI self-check result: FAIL, pass=%u fail=%u",
            pass_count,
            fail_count);
        return ESP_FAIL;
    }

    ESP_LOGI(TAG,
        "SPI self-check result: PASS, pass=%u fail=%u",
        pass_count,
        fail_count);

    return ESP_OK;
}

/*
*  Show TT SPI Registers
*/
esp_err_t ulx3s_spi_dump_regs(void)
{
    esp_err_t ret;
    uint8_t regs[ULX3S_SPI_REG_COUNT];

    ret = ulx3s_spi_read_regs(regs);
    if (ret != ESP_OK) {
        return ret;
    }

    ulx3s_spi_log_regs(regs);

    return ESP_OK;
}

/*
*  Peek TT SPI Registers
*/
esp_err_t ulx3s_spi_monitor_once(void)
{
    esp_err_t ret;
    uint8_t regs[ULX3S_SPI_REG_COUNT];
    static uint8_t previous_regs[ULX3S_SPI_REG_COUNT];
    static uint8_t have_previous;

    ret = ulx3s_spi_read_regs(regs);
    if (ret != ESP_OK) {
        return ret;
    }

#if ULX3S_SPI_MONITOR_LOG_CHANGES_ONLY
    if ((have_previous == 0U) || (memcmp(previous_regs, regs, sizeof(regs)) != 0)) {
        ulx3s_spi_log_regs(regs);
        memcpy(previous_regs, regs, sizeof(previous_regs));
        have_previous = 1U;
    }
#else
    ulx3s_spi_log_regs(regs);
#endif

    return ESP_OK;
}

#if (ULX3S_SPI_WRITE_MODE == ULX3S_SPI_WRITE_MODE_BOOT_CONFIG_ONCE)
void ulx3s_spi_apply_default_config_once(void)
{
    esp_err_t ret;

    /*
     * Optional startup writes:
     * - R2 reg_div   : default/sample divider value
     * - R3 reg_mode  : start from mode 0
     * - R4 reg_oscen : enable oscillator/source bit 0
     *
     * R5..R7 are read-only status/raw outputs.
     */
    ret = ulx3s_spi_write_reg(TT_REG_DIV, 0x10U);
    if (ret != ESP_OK) {
        ESP_LOGE(TAG, "ulx3s_spi_write_reg failed: %s", esp_err_to_name(ret));
        return;
    }

    ret = ulx3s_spi_write_reg(TT_REG_MODE, 0x00U);
    if (ret != ESP_OK) {
        ESP_LOGE(TAG, "ulx3s_spi_write_reg failed: %s", esp_err_to_name(ret));
        return;
    }

    ret = ulx3s_spi_write_reg(TT_REG_OSCEN, 0x01U);
    if (ret != ESP_OK) {
        ESP_LOGE(TAG, "ulx3s_spi_write_reg failed: %s", esp_err_to_name(ret));
        return;
    }

    ret = ulx3s_spi_dump_regs();
    if (ret != ESP_OK) {
        ESP_LOGE(TAG, "ulx3s_spi_dump_regs failed: %s", esp_err_to_name(ret));
        return;
    }
}
#endif /* conditional ULX3S_SPI_WRITE_MODE == ULX3S_SPI_WRITE_MODE_BOOT_CONFIG_ONCE */

#if (ULX3S_SPI_WRITE_MODE == ULX3S_SPI_WRITE_MODE_SELF_TEST_ONCE)
static esp_err_t ulx3s_spi_expect_reg(
    uint8_t addr,
    uint8_t expected,
    const char* name)
{
    esp_err_t ret;
    uint8_t actual;

    ret = ulx3s_spi_read_reg(addr, &actual);
    if (ret != ESP_OK) {
        ESP_LOGE(TAG, "SPI self-test read failed for %s: %s",
                 name,
                 esp_err_to_name(ret));
        return ret;
    }

    if (actual != expected) {
        ESP_LOGE(TAG, "SPI self-test FAIL %s: expected %02X, actual %02X",
                 name,
                 expected,
                 actual);
        return ESP_FAIL;
    }

    ESP_LOGI(TAG, "SPI self-test PASS %s: %02X", name, actual);

    return ESP_OK;
}

void ulx3s_spi_self_test_once(void)
{
    esp_err_t ret;
    uint8_t saved_div;
    uint8_t saved_mode;
    uint8_t saved_oscen;
    unsigned int write_pass_count;
    unsigned int restore_pass_count;

    write_pass_count = 0U;
    restore_pass_count = 0U;

    ESP_LOGI(TAG, "SPI self-test: saving current writable registers");

    ret = ulx3s_spi_read_reg(TT_REG_DIV, &saved_div);
    if (ret != ESP_OK) {
        ESP_LOGE(TAG, "SPI self-test failed to save R2: %s", esp_err_to_name(ret));
        return;
    }

    ret = ulx3s_spi_read_reg(TT_REG_MODE, &saved_mode);
    if (ret != ESP_OK) {
        ESP_LOGE(TAG, "SPI self-test failed to save R3: %s", esp_err_to_name(ret));
        return;
    }

    ret = ulx3s_spi_read_reg(TT_REG_OSCEN, &saved_oscen);
    if (ret != ESP_OK) {
        ESP_LOGE(TAG, "SPI self-test failed to save R4: %s", esp_err_to_name(ret));
        return;
    }

    ESP_LOGI(TAG, "SPI self-test saved: R2=%02X R3=%02X R4=%02X",
             saved_div,
             saved_mode,
             saved_oscen);

    ret = ulx3s_spi_write_reg(TT_REG_DIV, 0xA5U);
    if (ret != ESP_OK) {
        ESP_LOGE(TAG, "SPI self-test failed to write R2: %s", esp_err_to_name(ret));
        return;
    }

    ret = ulx3s_spi_write_reg(TT_REG_MODE, 0x5AU);
    if (ret != ESP_OK) {
        ESP_LOGE(TAG, "SPI self-test failed to write R3: %s", esp_err_to_name(ret));
        return;
    }

    ret = ulx3s_spi_write_reg(TT_REG_OSCEN, 0x03U);
    if (ret != ESP_OK) {
        ESP_LOGE(TAG, "SPI self-test failed to write R4: %s", esp_err_to_name(ret));
        return;
    }

    ret = ulx3s_spi_expect_reg(TT_REG_DIV, 0xA5U, "R2");
    if (ret != ESP_OK) {
        return;
    }
    write_pass_count++;

    ret = ulx3s_spi_expect_reg(TT_REG_MODE, 0x5AU, "R3");
    if (ret != ESP_OK) {
        return;
    }
    write_pass_count++;

    ret = ulx3s_spi_expect_reg(TT_REG_OSCEN, 0x03U, "R4");
    if (ret != ESP_OK) {
        return;
    }
    write_pass_count++;

    ESP_LOGI(TAG, "SPI self-test: restoring saved writable registers");

    ret = ulx3s_spi_write_reg(TT_REG_DIV, saved_div);
    if (ret != ESP_OK) {
        ESP_LOGE(TAG, "SPI self-test failed to restore R2: %s", esp_err_to_name(ret));
        return;
    }

    ret = ulx3s_spi_write_reg(TT_REG_MODE, saved_mode);
    if (ret != ESP_OK) {
        ESP_LOGE(TAG, "SPI self-test failed to restore R3: %s", esp_err_to_name(ret));
        return;
    }

    ret = ulx3s_spi_write_reg(TT_REG_OSCEN, saved_oscen);
    if (ret != ESP_OK) {
        ESP_LOGE(TAG, "SPI self-test failed to restore R4: %s", esp_err_to_name(ret));
        return;
    }

    ret = ulx3s_spi_expect_reg(TT_REG_DIV, saved_div, "R2 restore");
    if (ret != ESP_OK) {
        return;
    }
    restore_pass_count++;

    ret = ulx3s_spi_expect_reg(TT_REG_MODE, saved_mode, "R3 restore");
    if (ret != ESP_OK) {
        return;
    }
    restore_pass_count++;

    ret = ulx3s_spi_expect_reg(TT_REG_OSCEN, saved_oscen, "R4 restore");
    if (ret != ESP_OK) {
        return;
    }
    restore_pass_count++;

    ESP_LOGI(TAG, "SPI self-test result: PASS, writes=%u, restores=%u",
             write_pass_count,
             restore_pass_count);
}
#endif /* conditional ULX3S_SPI_WRITE_MODE == ULX3S_SPI_WRITE_MODE_SELF_TEST_ONCE */
