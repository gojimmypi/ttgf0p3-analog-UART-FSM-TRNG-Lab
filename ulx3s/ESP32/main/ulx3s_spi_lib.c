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
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"

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

#ifdef TT_MACRO_BIG16_SPI_REG
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
        (unsigned int)regs[TT_REG_SRC],
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
        (unsigned int)regs[TT_REG_SRC],
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
#define ULX3S_SPI_SELF_CHECK_TRNG_ENABLE        0x01U
#define ULX3S_SPI_SELF_CHECK_TRNG_SRC           3U
#define ULX3S_SPI_SELF_CHECK_TRNG_DIV           0x01U
#define ULX3S_SPI_SELF_CHECK_TRNG_MODE          0x00U
#define ULX3S_SPI_SELF_CHECK_TRNG_OSCEN         0xFFU
#define ULX3S_SPI_SELF_CHECK_TRNG_SAMPLES       8U
#define ULX3S_SPI_SELF_CHECK_TRNG_DELAY_MS      10U
#define ULX3S_SPI_SELF_CHECK_TRNG_SETTLE_MS     20U

#define ULX3S_SPI_RO_CHARACTERIZE_SOURCE_ROX    2U
#define ULX3S_SPI_RO_CHARACTERIZE_SOURCE_MIX    3U
#define ULX3S_SPI_RO_CHARACTERIZE_DIV           0x01U
#define ULX3S_SPI_RO_CHARACTERIZE_MODE          0x00U
#define ULX3S_SPI_RO_CHARACTERIZE_ENABLE        0x01U
#define ULX3S_SPI_RO_CHARACTERIZE_SAMPLES       256U
#define ULX3S_SPI_RO_CHARACTERIZE_DELAY_MS      1U
#define ULX3S_SPI_RO_CHARACTERIZE_SETTLE_MS     10U
#define ULX3S_SPI_RO_CHARACTERIZE_RO_COUNT      8U

#ifndef ULX3S_REG_STATUS_EXPECTED
#define ULX3S_REG_STATUS_EXPECTED               0x3CU
#endif

#ifndef ULX3S_REG_STATUS_COLD_EXPECTED
#define ULX3S_REG_STATUS_COLD_EXPECTED          0x04U
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

static uint16_t ulx3s_spi_raw_from_regs(const uint8_t regs[ULX3S_SPI_REG_COUNT])
{
    return ((uint16_t)regs[TT_REG_RAWHI] << 8) | regs[TT_REG_RAWLO];
}

static unsigned int ulx3s_spi_popcount16(uint16_t value)
{
    unsigned int count;

    count = 0U;

    while (value != 0U) {
        count += (unsigned int)(value & 1U);
        value >>= 1U;
    }

    return count;
}

static void ulx3s_spi_log_section(const char* title)
{
    ESP_LOGI(TAG, "--------------------------------------------------------");
    ESP_LOGI(TAG, "%s", title);
    ESP_LOGI(TAG, "--------------------------------------------------------");
}

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

static unsigned int ulx3s_spi_check_status_initial(uint8_t status)
{
    if (status == ULX3S_REG_STATUS_COLD_EXPECTED) {
        ESP_LOGI(TAG,
            "SPI self-check PASS R5 STATUS initial cold/reset state: %02X",
            status);
        ESP_LOGI(TAG,
            "SPI self-check note: R5=0x%02X is allowed immediately after FPGA/project reset before TRNG warm-up",
            (unsigned int)ULX3S_REG_STATUS_COLD_EXPECTED);
        return 0U;
    }

    if (status == ULX3S_REG_STATUS_EXPECTED) {
        ESP_LOGI(TAG,
            "SPI self-check PASS R5 STATUS initial warmed/default state: %02X",
            status);
        return 0U;
    }

    ESP_LOGE(TAG,
        "SPI self-check FAIL R5 STATUS initial: expected cold %02X or warmed %02X, actual %02X",
        (unsigned int)ULX3S_REG_STATUS_COLD_EXPECTED,
        (unsigned int)ULX3S_REG_STATUS_EXPECTED,
        status);
    return 1U;
}

static void ulx3s_spi_log_status_after_warmup(uint8_t status)
{
    if (status == ULX3S_REG_STATUS_EXPECTED) {
        ESP_LOGI(TAG,
            "SPI self-check PASS R5 STATUS after active warm-up/restore: %02X",
            status);
    }
    else {
        ESP_LOGW(TAG,
            "SPI self-check WARN R5 STATUS after active warm-up/restore: expected %02X, actual %02X",
            (unsigned int)ULX3S_REG_STATUS_EXPECTED,
            status);
    }
}

static esp_err_t ulx3s_spi_restore_trng_regs(const uint8_t saved_regs[ULX3S_SPI_REG_COUNT])
{
    esp_err_t ret;
    esp_err_t first_err;

    first_err = ESP_OK;

    ret = ulx3s_spi_write_reg(TT_REG_CTRL, ULX3S_REG_CTRL_DEFAULT);
    if ((ret != ESP_OK) && (first_err == ESP_OK)) {
        first_err = ret;
    }

    ret = ulx3s_spi_write_reg(TT_REG_SRC, saved_regs[TT_REG_SRC]);
    if ((ret != ESP_OK) && (first_err == ESP_OK)) {
        first_err = ret;
    }

    ret = ulx3s_spi_write_reg(TT_REG_DIV, saved_regs[TT_REG_DIV]);
    if ((ret != ESP_OK) && (first_err == ESP_OK)) {
        first_err = ret;
    }

    ret = ulx3s_spi_write_reg(TT_REG_MODE, saved_regs[TT_REG_MODE]);
    if ((ret != ESP_OK) && (first_err == ESP_OK)) {
        first_err = ret;
    }

    ret = ulx3s_spi_write_reg(TT_REG_OSCEN, saved_regs[TT_REG_OSCEN]);
    if ((ret != ESP_OK) && (first_err == ESP_OK)) {
        first_err = ret;
    }

    ret = ulx3s_spi_write_reg(TT_REG_CTRL, saved_regs[TT_REG_CTRL]);
    if ((ret != ESP_OK) && (first_err == ESP_OK)) {
        first_err = ret;
    }

    return first_err;
}

static esp_err_t ulx3s_spi_check_trng_raw_changes(
    const uint8_t saved_regs[ULX3S_SPI_REG_COUNT],
    unsigned int* pass_count,
    unsigned int* fail_count)
{
#if (ULX3S_SPI_WRITE_MODE != ULX3S_SPI_WRITE_MODE_MONITOR_ONLY)
    esp_err_t ret;
    uint8_t regs[ULX3S_SPI_REG_COUNT];
    uint16_t samples[ULX3S_SPI_SELF_CHECK_TRNG_SAMPLES];
    uint16_t raw;
    uint8_t sample;
    uint8_t unique_count;
    uint8_t index;
    uint8_t seen;

    ulx3s_spi_log_section("SPI self-check: active R6/R7 raw-change test");
    ESP_LOGI(TAG,
        "SPI self-check purpose: prove R6/R7 are not fixed when the TRNG is explicitly enabled");
    ESP_LOGI(TAG,
        "SPI self-check active config: write R0=00, R1=0x%02X, R2=0x%02X, R3=0x%02X, R4=0x%02X, then R0=0x%02X",
        (unsigned int)ULX3S_SPI_SELF_CHECK_TRNG_SRC,
        (unsigned int)ULX3S_SPI_SELF_CHECK_TRNG_DIV,
        (unsigned int)ULX3S_SPI_SELF_CHECK_TRNG_MODE,
        (unsigned int)ULX3S_SPI_SELF_CHECK_TRNG_OSCEN,
        (unsigned int)ULX3S_SPI_SELF_CHECK_TRNG_ENABLE);
    ESP_LOGI(TAG,
        "SPI self-check pass rule: at least two unique 16-bit raw values across %u samples",
        (unsigned int)ULX3S_SPI_SELF_CHECK_TRNG_SAMPLES);

    ret = ulx3s_spi_write_reg(TT_REG_CTRL, ULX3S_REG_CTRL_DEFAULT);
    if (ret != ESP_OK) {
        ESP_LOGE(TAG, "SPI self-check failed to write R0 CTRL disable: %s", esp_err_to_name(ret));
        return ret;
    }

    ret = ulx3s_spi_write_reg(TT_REG_SRC, ULX3S_SPI_SELF_CHECK_TRNG_SRC);
    if (ret != ESP_OK) {
        ESP_LOGE(TAG, "SPI self-check failed to write R1 SRC: %s", esp_err_to_name(ret));
        return ret;
    }

    ret = ulx3s_spi_write_reg(TT_REG_DIV, ULX3S_SPI_SELF_CHECK_TRNG_DIV);
    if (ret != ESP_OK) {
        ESP_LOGE(TAG, "SPI self-check failed to write R2 DIV: %s", esp_err_to_name(ret));
        (void)ulx3s_spi_restore_trng_regs(saved_regs);
        return ret;
    }

    ret = ulx3s_spi_write_reg(TT_REG_MODE, ULX3S_SPI_SELF_CHECK_TRNG_MODE);
    if (ret != ESP_OK) {
        ESP_LOGE(TAG, "SPI self-check failed to write R3 MODE: %s", esp_err_to_name(ret));
        (void)ulx3s_spi_restore_trng_regs(saved_regs);
        return ret;
    }

    ret = ulx3s_spi_write_reg(TT_REG_OSCEN, ULX3S_SPI_SELF_CHECK_TRNG_OSCEN);
    if (ret != ESP_OK) {
        ESP_LOGE(TAG, "SPI self-check failed to write R4 OSCEN: %s", esp_err_to_name(ret));
        (void)ulx3s_spi_restore_trng_regs(saved_regs);
        return ret;
    }

    ret = ulx3s_spi_write_reg(TT_REG_CTRL, ULX3S_SPI_SELF_CHECK_TRNG_ENABLE);
    if (ret != ESP_OK) {
        ESP_LOGE(TAG, "SPI self-check failed to write R0 CTRL enable: %s", esp_err_to_name(ret));
        (void)ulx3s_spi_restore_trng_regs(saved_regs);
        return ret;
    }

    ESP_LOGI(TAG,
        "SPI self-check active config applied; settling for %u ms before sampling...",
        (unsigned int)ULX3S_SPI_SELF_CHECK_TRNG_SETTLE_MS);

    vTaskDelay(pdMS_TO_TICKS(ULX3S_SPI_SELF_CHECK_TRNG_SETTLE_MS));

    unique_count = 0U;

    for (sample = 0U; sample < ULX3S_SPI_SELF_CHECK_TRNG_SAMPLES; sample++) {
        ret = ulx3s_spi_read_regs(regs);
        if (ret != ESP_OK) {
            ESP_LOGE(TAG, "SPI self-check raw read failed: %s", esp_err_to_name(ret));
            (void)ulx3s_spi_restore_trng_regs(saved_regs);
            return ret;
        }

        raw = ulx3s_spi_raw_from_regs(regs);
        samples[sample] = raw;

        seen = 0U;
        for (index = 0U; index < sample; index++) {
            if (samples[index] == raw) {
                seen = 1U;
                break;
            }
        }

        if (seen == 0U) {
            unique_count++;
        }

        ESP_LOGI(TAG,
            "SPI self-check raw sample %u: raw=0x%04X ctrl=0x%02X status=0x%02X src=%u div=0x%02X mode=0x%02X oscen=0x%02X",
            (unsigned int)sample,
            raw,
            regs[TT_REG_CTRL],
            regs[TT_REG_STATUS],
            (unsigned int)regs[TT_REG_SRC],
            regs[TT_REG_DIV],
            regs[TT_REG_MODE],
            regs[TT_REG_OSCEN]);

        vTaskDelay(pdMS_TO_TICKS(ULX3S_SPI_SELF_CHECK_TRNG_DELAY_MS));
    }

    ESP_LOGI(TAG, "SPI self-check: restoring saved config after active raw-change test");

    ret = ulx3s_spi_restore_trng_regs(saved_regs);
    if (ret != ESP_OK) {
        ESP_LOGE(TAG, "SPI self-check restore failed: %s", esp_err_to_name(ret));
        return ret;
    }

    if (unique_count <= 1U) {
        ESP_LOGE(TAG,
            "SPI self-check FAIL R6/R7 raw: fixed at 0x%04X across %u active TRNG samples",
            samples[0],
            (unsigned int)ULX3S_SPI_SELF_CHECK_TRNG_SAMPLES);
        (*fail_count)++;
        return ESP_FAIL;
    }

    ESP_LOGI(TAG,
        "SPI self-check PASS R6/R7 raw changed: unique=%u/%u first=0x%04X last=0x%04X",
        (unsigned int)unique_count,
        (unsigned int)ULX3S_SPI_SELF_CHECK_TRNG_SAMPLES,
        samples[0],
        samples[ULX3S_SPI_SELF_CHECK_TRNG_SAMPLES - 1U]);

    (*pass_count)++;
    ESP_LOGI(TAG, "--------------------------------------------------------");

    return ESP_OK;
#else
    ESP_LOGW(TAG, "SPI self-check SKIP R6/R7 raw-change check: SPI writes disabled");
    (void)saved_regs;
    (void)pass_count;
    (void)fail_count;
    return ESP_OK;
#endif
}


static esp_err_t ulx3s_spi_start_trng_source(
    uint8_t source,
    uint8_t oscen)
{
    esp_err_t ret;

    ESP_LOGI(TAG,
        "RO characterize setup: source=%u oscen=0x%02X; disabling sampling before config writes",
        (unsigned int)source,
        (unsigned int)oscen);
    ESP_LOGI(TAG,
        "RO characterize setup writes: R0=00, R1=0x%02X, R2=0x%02X, R3=0x%02X, R4=0x%02X, R0=0x%02X",
        (unsigned int)source,
        (unsigned int)ULX3S_SPI_RO_CHARACTERIZE_DIV,
        (unsigned int)ULX3S_SPI_RO_CHARACTERIZE_MODE,
        (unsigned int)oscen,
        (unsigned int)ULX3S_SPI_RO_CHARACTERIZE_ENABLE);

    ret = ulx3s_spi_write_reg(TT_REG_CTRL, ULX3S_REG_CTRL_DEFAULT);
    if (ret != ESP_OK) {
        ESP_LOGE(TAG, "RO characterize failed to write R0 CTRL disable: %s", esp_err_to_name(ret));
        return ret;
    }

    ret = ulx3s_spi_write_reg(TT_REG_SRC, source);
    if (ret != ESP_OK) {
        ESP_LOGE(TAG, "RO characterize failed to write R1 SRC: %s", esp_err_to_name(ret));
        return ret;
    }

    ret = ulx3s_spi_write_reg(TT_REG_DIV, ULX3S_SPI_RO_CHARACTERIZE_DIV);
    if (ret != ESP_OK) {
        ESP_LOGE(TAG, "RO characterize failed to write R2 DIV: %s", esp_err_to_name(ret));
        return ret;
    }

    ret = ulx3s_spi_write_reg(TT_REG_MODE, ULX3S_SPI_RO_CHARACTERIZE_MODE);
    if (ret != ESP_OK) {
        ESP_LOGE(TAG, "RO characterize failed to write R3 MODE: %s", esp_err_to_name(ret));
        return ret;
    }

    ret = ulx3s_spi_write_reg(TT_REG_OSCEN, oscen);
    if (ret != ESP_OK) {
        ESP_LOGE(TAG, "RO characterize failed to write R4 OSCEN: %s", esp_err_to_name(ret));
        return ret;
    }

    ret = ulx3s_spi_write_reg(TT_REG_CTRL, ULX3S_SPI_RO_CHARACTERIZE_ENABLE);
    if (ret != ESP_OK) {
        ESP_LOGE(TAG, "RO characterize failed to write R0 CTRL enable: %s", esp_err_to_name(ret));
        return ret;
    }

    ESP_LOGI(TAG,
        "RO characterize setup applied; settling for %u ms before collecting samples...",
        (unsigned int)ULX3S_SPI_RO_CHARACTERIZE_SETTLE_MS);

    vTaskDelay(pdMS_TO_TICKS(ULX3S_SPI_RO_CHARACTERIZE_SETTLE_MS));

    return ESP_OK;
}

static const char* ulx3s_spi_ro_source_name(uint8_t source)
{
    switch (source)
    {
    case ULX3S_SPI_RO_CHARACTERIZE_SOURCE_ROX:
        return "S2 ROX/fallback";

    case ULX3S_SPI_RO_CHARACTERIZE_SOURCE_MIX:
        return "S3 MIX/fallback";

    default:
        return "unknown";
    }
}

static esp_err_t ulx3s_spi_characterize_ro_mask(
    uint8_t source,
    uint8_t oscen,
    const char* source_label,
    const char* ro_label,
    unsigned int* pass_count,
    unsigned int* fail_count)
{
#if (ULX3S_SPI_WRITE_MODE != ULX3S_SPI_WRITE_MODE_MONITOR_ONLY)
    esp_err_t ret;
    uint8_t regs[ULX3S_SPI_REG_COUNT];
    uint16_t samples[ULX3S_SPI_RO_CHARACTERIZE_SAMPLES];
    uint16_t raw;
    uint16_t min_raw;
    uint16_t max_raw;
    uint16_t previous_raw;
    uint16_t first_raw;
    uint16_t last_raw;
    unsigned int sample;
    unsigned int index;
    unsigned int unique_count;
    unsigned int change_count;
    unsigned int ones_count;
    unsigned int bit_count;
    unsigned int percent_x10;
    uint8_t status_or;
    uint8_t status_and;
    uint8_t seen;
    uint8_t failed;

    ESP_LOGI(TAG,
        "RO characterize test: src=%u %s %s oscen=0x%02X",
        (unsigned int)source,
        source_label,
        ro_label,
        (unsigned int)oscen);
    ESP_LOGI(TAG,
        "RO characterize test purpose: one-hot activity screen using %u samples; this is not a frequency measurement",
        (unsigned int)ULX3S_SPI_RO_CHARACTERIZE_SAMPLES);

    ret = ulx3s_spi_start_trng_source(source, oscen);
    if (ret != ESP_OK) {
        return ret;
    }

    unique_count = 0U;
    change_count = 0U;
    ones_count = 0U;
    status_or = 0U;
    status_and = 0xFFU;
    min_raw = 0xFFFFU;
    max_raw = 0U;
    previous_raw = 0U;
    first_raw = 0U;
    last_raw = 0U;

    for (sample = 0U; sample < ULX3S_SPI_RO_CHARACTERIZE_SAMPLES; sample++) {
        ret = ulx3s_spi_read_regs(regs);
        if (ret != ESP_OK) {
            ESP_LOGE(TAG, "RO characterize read failed: %s", esp_err_to_name(ret));
            return ret;
        }

        raw = ulx3s_spi_raw_from_regs(regs);
        samples[sample] = raw;

        if (sample == 0U) {
            first_raw = raw;
        }
        last_raw = raw;

        if ((sample != 0U) && (raw != previous_raw)) {
            change_count++;
        }
        previous_raw = raw;

        if (raw < min_raw) {
            min_raw = raw;
        }

        if (raw > max_raw) {
            max_raw = raw;
        }

        ones_count += ulx3s_spi_popcount16(raw);
        status_or |= regs[TT_REG_STATUS];
        status_and &= regs[TT_REG_STATUS];

        seen = 0U;
        for (index = 0U; index < sample; index++) {
            if (samples[index] == raw) {
                seen = 1U;
                break;
            }
        }

        if (seen == 0U) {
            unique_count++;
        }

        vTaskDelay(pdMS_TO_TICKS(ULX3S_SPI_RO_CHARACTERIZE_DELAY_MS));
    }

    bit_count = ULX3S_SPI_RO_CHARACTERIZE_SAMPLES * 16U;
    percent_x10 = ((ones_count * 1000U) + (bit_count / 2U)) / bit_count;

    failed = 0U;

    if (unique_count <= 1U) {
        ESP_LOGE(TAG,
            "RO characterize reason: FAIL because unique_count <= 1 for src=%u %s oscen=0x%02X",
            (unsigned int)source,
            ro_label,
            (unsigned int)oscen);
        failed = 1U;
    }

    if ((ones_count == 0U) || (ones_count == bit_count)) {
        ESP_LOGE(TAG,
            "RO characterize reason: FAIL because ones_count is all-zero or all-one for src=%u %s oscen=0x%02X",
            (unsigned int)source,
            ro_label,
            (unsigned int)oscen);
        failed = 1U;
    }

    if (change_count == 0U) {
        ESP_LOGE(TAG,
            "RO characterize reason: FAIL because no adjacent raw samples changed for src=%u %s oscen=0x%02X",
            (unsigned int)source,
            ro_label,
            (unsigned int)oscen);
        failed = 1U;
    }

    ESP_LOGI(TAG,
        "src=%u %s %s oscen=0x%02X unique=%u/%u changes=%u/%u ones=%u/%u (%u.%u%%) first=0x%04X last=0x%04X min=0x%04X max=0x%04X status_or=0x%02X status_and=0x%02X",
        (unsigned int)source,
        source_label,
        ro_label,
        oscen,
        unique_count,
        (unsigned int)ULX3S_SPI_RO_CHARACTERIZE_SAMPLES,
        change_count,
        (unsigned int)(ULX3S_SPI_RO_CHARACTERIZE_SAMPLES - 1U),
        ones_count,
        bit_count,
        percent_x10 / 10U,
        percent_x10 % 10U,
        first_raw,
        last_raw,
        min_raw,
        max_raw,
        status_or,
        status_and);
    ESP_LOGI(TAG, "RO characterize %s", (failed == 0U) ? "PASS" : "FAIL");

    if (failed != 0U) {
        (*fail_count)++;
        return ESP_FAIL;
    }

    (*pass_count)++;
    ESP_LOGI(TAG, ".....................");

    return ESP_OK;
#else
    ESP_LOGW(TAG, "RO characterize SKIP %s %s: SPI writes disabled", source_label, ro_label);
    (void)source;
    (void)oscen;
    (void)source_label;
    (void)ro_label;
    (void)pass_count;
    (void)fail_count;
    return ESP_OK;
#endif
}

esp_err_t ulx3s_spi_characterize_ro_sources_once(void)
{
#if (ULX3S_SPI_WRITE_MODE != ULX3S_SPI_WRITE_MODE_MONITOR_ONLY)
    esp_err_t ret;
    uint8_t saved_regs[ULX3S_SPI_REG_COUNT];
    uint8_t ro_index;
    uint8_t oscen;
    unsigned int pass_count;
    unsigned int fail_count;

    static const char* const ro_labels[ULX3S_SPI_RO_CHARACTERIZE_RO_COUNT] = {
        "RO0",
        "RO1",
        "RO2",
        "RO3",
        "RO4",
        "RO5",
        "RO6",
        "RO7"
    };

    pass_count = 0U;
    fail_count = 0U;

    ulx3s_spi_log_section("RO characterize: begin");
    ESP_LOGI(TAG,
        "RO characterize purpose: verify each one-hot oscillator-enable path produces non-fixed SPI-visible raw samples");
    ESP_LOGI(TAG,
        "RO characterize scope: S2 ROX/fallback RO0-RO7, S3 MIX/fallback RO0-RO7, then S3 ALL oscen=0xFF");
    ESP_LOGI(TAG,
        "RO characterize config: samples=%u div=0x%02X mode=0x%02X sample_delay_ms=%u settle_ms=%u",
        (unsigned int)ULX3S_SPI_RO_CHARACTERIZE_SAMPLES,
        (unsigned int)ULX3S_SPI_RO_CHARACTERIZE_DIV,
        (unsigned int)ULX3S_SPI_RO_CHARACTERIZE_MODE,
        (unsigned int)ULX3S_SPI_RO_CHARACTERIZE_DELAY_MS,
        (unsigned int)ULX3S_SPI_RO_CHARACTERIZE_SETTLE_MS);
    ESP_LOGI(TAG,
        "RO characterize pass rules: unique_count > 1, change_count > 0, ones_count not all 0 or all 1");
    ESP_LOGI(TAG,
        "RO characterize note: this is an activity screen, not a per-RO frequency or entropy proof");

    ret = ulx3s_spi_read_regs(saved_regs);
    if (ret != ESP_OK) {
        ESP_LOGE(TAG, "RO characterize failed to save registers: %s", esp_err_to_name(ret));
        return ret;
    }

    ESP_LOGI(TAG, "--------------------------------------------------------");
    ESP_LOGI(TAG,
        "RO characterize phase 1/3: src=2 %s, one-hot RO0-RO7",
        ulx3s_spi_ro_source_name(ULX3S_SPI_RO_CHARACTERIZE_SOURCE_ROX));
    ESP_LOGI(TAG, "--------------------------------------------------------");

    for (ro_index = 0U; ro_index < ULX3S_SPI_RO_CHARACTERIZE_RO_COUNT; ro_index++) {
        oscen = (uint8_t)(1U << ro_index);

        ret = ulx3s_spi_characterize_ro_mask(
            ULX3S_SPI_RO_CHARACTERIZE_SOURCE_ROX,
            oscen,
            ulx3s_spi_ro_source_name(ULX3S_SPI_RO_CHARACTERIZE_SOURCE_ROX),
            ro_labels[ro_index],
            &pass_count,
            &fail_count);

        if ((ret != ESP_OK) && (ret != ESP_FAIL)) {
            (void)ulx3s_spi_restore_trng_regs(saved_regs);
            return ret;
        }
    }

    ESP_LOGI(TAG, "--------------------------------------------------------");
    ESP_LOGI(TAG,
        "RO characterize phase 2/3: src=3 %s, one-hot RO0-RO7",
        ulx3s_spi_ro_source_name(ULX3S_SPI_RO_CHARACTERIZE_SOURCE_MIX));
    ESP_LOGI(TAG, "--------------------------------------------------------");

    for (ro_index = 0U; ro_index < ULX3S_SPI_RO_CHARACTERIZE_RO_COUNT; ro_index++) {
        oscen = (uint8_t)(1U << ro_index);

        ret = ulx3s_spi_characterize_ro_mask(
            ULX3S_SPI_RO_CHARACTERIZE_SOURCE_MIX,
            oscen,
            ulx3s_spi_ro_source_name(ULX3S_SPI_RO_CHARACTERIZE_SOURCE_MIX),
            ro_labels[ro_index],
            &pass_count,
            &fail_count);

        if ((ret != ESP_OK) && (ret != ESP_FAIL)) {
            (void)ulx3s_spi_restore_trng_regs(saved_regs);
            return ret;
        }
    }

    ESP_LOGI(TAG, "--------------------------------------------------------");
    ESP_LOGI(TAG,
        "RO characterize phase 3/3: src=3 %s, all oscillator enables oscen=0xFF",
        ulx3s_spi_ro_source_name(ULX3S_SPI_RO_CHARACTERIZE_SOURCE_MIX));
    ESP_LOGI(TAG, "--------------------------------------------------------");

    ret = ulx3s_spi_characterize_ro_mask(
        ULX3S_SPI_RO_CHARACTERIZE_SOURCE_MIX,
        0xFFU,
        ulx3s_spi_ro_source_name(ULX3S_SPI_RO_CHARACTERIZE_SOURCE_MIX),
        "ALL",
        &pass_count,
        &fail_count);

    if ((ret != ESP_OK) && (ret != ESP_FAIL)) {
        (void)ulx3s_spi_restore_trng_regs(saved_regs);
        return ret;
    }

    ESP_LOGI(TAG, "RO characterize: restoring saved SPI config after characterization sweep");

    ret = ulx3s_spi_restore_trng_regs(saved_regs);
    if (ret != ESP_OK) {
        ESP_LOGE(TAG, "RO characterize restore failed: %s", esp_err_to_name(ret));
        return ret;
    }

    ESP_LOGI(TAG, "RO characterize: restore complete");

    if (fail_count != 0U) {
        ESP_LOGE(TAG,
            "RO characterize result: FAIL, pass=%u fail=%u",
            pass_count,
            fail_count);
        return ESP_FAIL;
    }

    ESP_LOGI(TAG,
        "RO characterize result: PASS, pass=%u fail=%u",
        pass_count,
        fail_count);

    return ESP_OK;
#else
    ESP_LOGW(TAG, "RO characterize SKIP: SPI writes disabled");
    return ESP_OK;
#endif
}

esp_err_t ulx3s_spi_self_check_regs_once(void)
{
    esp_err_t ret;
    uint8_t regs[ULX3S_SPI_REG_COUNT];
    unsigned int pass_count;
    unsigned int fail_count;
    size_t index;

    static const ulx3s_spi_reg_check_t reg_checks[] = {
        { TT_REG_CTRL,   "R0 CTRL",     ULX3S_REG_CTRL_DEFAULT,    0xFFU, ULX3S_SPI_CHECK_EQUAL },
        { TT_REG_SRC,    "R1 SRC",      ULX3S_REG_SRC_DEFAULT,     0xFFU, ULX3S_SPI_CHECK_EQUAL },
        { TT_REG_DIV,    "R2 DIV",      ULX3S_REG_DIV_DEFAULT,     0xFFU, ULX3S_SPI_CHECK_EQUAL },
        { TT_REG_MODE,   "R3 MODE",     ULX3S_REG_MODE_DEFAULT,    0xFFU, ULX3S_SPI_CHECK_EQUAL },
        { TT_REG_OSCEN,  "R4 OSCEN",    ULX3S_REG_OSCEN_DEFAULT,   0xFFU, ULX3S_SPI_CHECK_EQUAL },

        /*
         * R5 is checked separately because it can be 0x04 immediately after
         * FPGA/project reset before the TRNG status path has been warmed up.
         */

        /*
         * R6/R7 are checked separately as a combined active TRNG non-fixed value.
         */

#ifdef TT_MACRO_BIG16_SPI_REG
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

    ulx3s_spi_log_section("SPI self-check: begin");
    ESP_LOGI(TAG,
        "SPI self-check purpose: verify R0-RF SPI register map, expected defaults, pin snapshots, and active raw movement");
    ESP_LOGI(TAG,
        "SPI self-check expected defaults after reset: R0=0x%02X R1=0x%02X R2=0x%02X R3=0x%02X R4=0x%02X",
        (unsigned int)ULX3S_REG_CTRL_DEFAULT,
        (unsigned int)ULX3S_REG_SRC_DEFAULT,
        (unsigned int)ULX3S_REG_DIV_DEFAULT,
        (unsigned int)ULX3S_REG_MODE_DEFAULT,
        (unsigned int)ULX3S_REG_OSCEN_DEFAULT);
    ESP_LOGI(TAG,
        "SPI self-check expected R5 status: cold/reset 0x%02X is allowed before TRNG warm-up; warmed/default is 0x%02X",
        (unsigned int)ULX3S_REG_STATUS_COLD_EXPECTED,
        (unsigned int)ULX3S_REG_STATUS_EXPECTED);
#ifdef TT_MACRO_BIG16_SPI_REG
    ESP_LOGI(TAG,
        "SPI self-check expected BIG16 registers: R8 has UART RX idle bit set, RC=0xF4, RD/RE/RF=0x00");
#endif

#if (ULX3S_SPI_WRITE_MODE != ULX3S_SPI_WRITE_MODE_MONITOR_ONLY)
    ulx3s_spi_log_section("SPI self-check: reset config registers to known defaults");
    ESP_LOGI(TAG,
        "SPI self-check reset reason: ESP32 reset may not reset the FPGA register state");

    ret = ulx3s_spi_reset_config_registers();
    if (ret != ESP_OK) {
        ESP_LOGE(TAG, "SPI self-check reset failed: %s", esp_err_to_name(ret));
        return ret;
    }

    vTaskDelay(pdMS_TO_TICKS(ULX3S_SPI_SELF_CHECK_TRNG_SETTLE_MS));
#else
    ESP_LOGW(TAG, "SPI self-check: not resetting config registers because SPI writes are disabled");
#endif

    ulx3s_spi_log_section("SPI self-check: read R0-RF and compare register-map expectations");

    ret = ulx3s_spi_read_regs(regs);
    if (ret != ESP_OK) {
        ESP_LOGE(TAG, "SPI self-check failed to read registers: %s", esp_err_to_name(ret));
        return ret;
    }

    ulx3s_spi_log_regs(regs);

    ESP_LOGI(TAG,
        "SPI self-check step 1/3: compare stable registers and log dynamic pin snapshot registers");

    for (index = 0U; index < (sizeof(reg_checks) / sizeof(reg_checks[0])); index++) {
        if (reg_checks[index].addr >= ULX3S_SPI_REG_COUNT) {
            ESP_LOGE(TAG,
                "SPI self-check FAIL %s: addr %u outside register count %u",
                reg_checks[index].name,
                (unsigned int)reg_checks[index].addr,
                (unsigned int)ULX3S_SPI_REG_COUNT);
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

    if (ulx3s_spi_check_status_initial(regs[TT_REG_STATUS]) == 0U) {
        pass_count++;
    }
    else {
        fail_count++;
    }

    ESP_LOGI(TAG,
        "SPI self-check step 2/3: record passive R6/R7 snapshot before active TRNG check");
    ESP_LOGI(TAG,
        "SPI self-check INFO R6/R7 raw initial snapshot: 0x%04X",
        ulx3s_spi_raw_from_regs(regs));

    ESP_LOGI(TAG,
        "SPI self-check step 3/3: temporarily enable TRNG and require R6/R7 to change");

    ret = ulx3s_spi_check_trng_raw_changes(regs, &pass_count, &fail_count);
    if ((ret != ESP_OK) && (ret != ESP_FAIL)) {
        return ret;
    }

    ESP_LOGI(TAG,
        "SPI self-check step 3/3: re-read R0-RF after active warm-up and restore");

    ret = ulx3s_spi_read_regs(regs);
    if (ret != ESP_OK) {
        ESP_LOGE(TAG, "SPI self-check final read failed: %s", esp_err_to_name(ret));
        return ret;
    }

    ulx3s_spi_log_regs(regs);
    ulx3s_spi_log_status_after_warmup(regs[TT_REG_STATUS]);

#ifdef TT_MACRO_BIG16_SPI_REG
    ESP_LOGI(TAG,
        "SPI self-check final pin snapshot after warm-up/restore: ui=0x%02X uo=0x%02X uio_in=0x%02X uio_out=0x%02X uio_oe=0x%02X",
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

    //ret = ulx3s_spi_write_reg(TT_REG_DIV, 0x10U);
    //if (ret != ESP_OK) {
    //    ESP_LOGE(TAG, "ulx3s_spi_write_reg failed: %s", esp_err_to_name(ret));
    //    return;
    //}

    //ret = ulx3s_spi_write_reg(TT_REG_MODE, 0x00U);
    //if (ret != ESP_OK) {
    //    ESP_LOGE(TAG, "ulx3s_spi_write_reg failed: %s", esp_err_to_name(ret));
    //    return;
    //}

    //ret = ulx3s_spi_write_reg(TT_REG_OSCEN, 0x01U);
    //if (ret != ESP_OK) {
    //    ESP_LOGE(TAG, "ulx3s_spi_write_reg failed: %s", esp_err_to_name(ret));
    //    return;
    //}

    ulx3s_spi_log_section("SPI boot config: apply safe defaults once");
    ESP_LOGI(TAG,
        "SPI boot config purpose: leave firmware/demo in monitor-friendly defaults after diagnostics");
    ESP_LOGI(TAG,
        "SPI boot config writes: R0=0x%02X R1=0x%02X R2=0x%02X R3=0x%02X R4=0x%02X",
        (unsigned int)ULX3S_REG_CTRL_DEFAULT,
        (unsigned int)ULX3S_REG_SRC_DEFAULT,
        (unsigned int)ULX3S_REG_DIV_DEFAULT,
        (unsigned int)ULX3S_REG_MODE_DEFAULT,
        (unsigned int)ULX3S_REG_OSCEN_DEFAULT);

    ret = ulx3s_spi_reset_config_registers();
    if (ret != ESP_OK) {
        ESP_LOGE(TAG, "ulx3s_spi_reset_config_registers failed: %s", esp_err_to_name(ret));
        return;
    }

    ESP_LOGI(TAG, "SPI boot config: defaults written; dumping registers for confirmation");

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
