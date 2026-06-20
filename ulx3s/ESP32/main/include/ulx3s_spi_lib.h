/*
 * Copyright (c) 2026 gojimmypi
 * SPDX-License-Identifier: Apache-2.0
 *
 * See ATTRIBUTION.md for third-party sources and credits.
 *
 * file: ./ulx3s/ESP32/main/include/ulx3s_spi_lib.h
 *
 * ESP32 ulx3s_spi_lib FPGA SPI library
 *
 */

#ifndef _ULX3S_SPI_LIB_H_
#define _ULX3S_SPI_LIB_H_

#include <stdint.h>
#include <stdbool.h>

/* Espressif */
#include <esp_err.h>

#include "tt_trng.h"

/* Generated defined from src/project_config.v
 *   ./show_effective_defines.sh  ../src/project_config.v  --header tt_effective_defines.h
 */
#include "tt_effective_defines.h"

#ifndef TT_MACRO_BIG16_SPI_REG
    #error "missing TT_MACRO_BIG16_SPI_REG?"
#endif

/*
 * SPI write policy:
 *
 * 0: monitor only. Never write FPGA registers from ESP32.
 * 1: boot config once. Write safe defaults once at startup, then monitor only.
 * 2: self-test once. Save, write, verify, restore, then monitor only.
 *
 * Monitor-only is the safe default for concurrent UART regression tests.
 */
#define ULX3S_SPI_WRITE_MODE_MONITOR_ONLY       0
#define ULX3S_SPI_WRITE_MODE_BOOT_CONFIG_ONCE   1
#define ULX3S_SPI_WRITE_MODE_SELF_TEST_ONCE     2

//#define ULX3S_SPI_WRITE_MODE    ULX3S_SPI_WRITE_MODE_MONITOR_ONLY
#define ULX3S_SPI_WRITE_MODE    ULX3S_SPI_WRITE_MODE_BOOT_CONFIG_ONCE

#define ULX3S_SPI_MONITOR_LOG_CHANGES_ONLY      1
#define ULX3S_SPI_MONITOR_POLL_DELAY_MS         1000U

#define TT_REG_CTRL                             0U
#define TT_REG_SRC                              1U
#define TT_REG_DIV                              2U
#define TT_REG_MODE                             3U
#define TT_REG_OSCEN                            4U
#define TT_REG_STATUS                           5U
#define TT_REG_RAWLO                            6U
#define TT_REG_RAWHI                            7U

#ifdef TT_MACRO_BIG16_SPI_REG
    /* Additional registers in BIG16_SPI_REG: */
    #define TT_REG_UI_IN                        8U
    #define TT_REG_UO_OUT                       9U
    #define TT_REG_UIO_IN                       10U
    #define TT_REG_UIO_OUT                      11U
    #define TT_REG_UIO_OE                       12U
    #define TT_REG_BUILD                        13U
    #define TT_REG_UNUSED_D                     TT_REG_BUILD
    #define TT_REG_UNUSED_E                     14U
    #define TT_REG_UNUSED_F                     15U
    #define ULX3S_SPI_REG_COUNT                    16U
#else
    /* Just the basic list, above */
    #define ULX3S_SPI_REG_COUNT                     8U
#endif

#define TT_BUILD_TARGET_UNKNOWN             0x00U
#define TT_BUILD_TARGET_ASIC_SKY130          0x41U
#define TT_BUILD_TARGET_ASIC_GF180           0x42U
#define TT_BUILD_TARGET_FPGA                 0x81U
#define TT_BUILD_TARGET_FPGA_ULX3S_12K       0x82U
#define TT_BUILD_TARGET_FPGA_ULX3S_85F       0x83U
#define TT_BUILD_TARGET_SIM                  0xF0U

#define TT_BUILD_TARGET_CLASS_MASK           0xF0U
#define TT_BUILD_TARGET_CLASS_FPGA           0x80U

#define ULX3S_REG_CTRL_DEFAULT     0x00U
#define ULX3S_REG_SRC_DEFAULT      0x00U
#define ULX3S_REG_DIV_DEFAULT      0x10U
#define ULX3S_REG_MODE_DEFAULT     0x00U
#define ULX3S_REG_OSCEN_DEFAULT    0x01U


esp_err_t ulx3s_spi_init(bool verbose);

esp_err_t ulx3s_spi_reset_config_registers(void);

esp_err_t ulx3s_spi_self_check_regs_once(void);

esp_err_t ulx3s_spi_characterize_ro_sources_once(void);

esp_err_t ulx3s_spi_dump_regs(void);

esp_err_t ulx3s_spi_read_reg(
    uint8_t addr,
    uint8_t* value);

esp_err_t ulx3s_spi_write_reg(
    uint8_t addr,
    uint8_t value);

esp_err_t ulx3s_spi_read_regs(uint8_t regs[ULX3S_SPI_REG_COUNT]);

void ulx3s_spi_log_regs(const uint8_t regs[ULX3S_SPI_REG_COUNT]);

esp_err_t ulx3s_spi_monitor_once(void);

#if (ULX3S_SPI_WRITE_MODE == ULX3S_SPI_WRITE_MODE_BOOT_CONFIG_ONCE)
void ulx3s_spi_apply_default_config_once(void);
#endif /* conditional ULX3S_SPI_WRITE_MODE == ULX3S_SPI_WRITE_MODE_BOOT_CONFIG_ONCE */

#if (ULX3S_SPI_WRITE_MODE == ULX3S_SPI_WRITE_MODE_SELF_TEST_ONCE)
void ulx3s_spi_self_test_once(void);
#endif /* conditional ULX3S_SPI_WRITE_MODE == ULX3S_SPI_WRITE_MODE_SELF_TEST_ONCE */

#endif /* _ULX3S_SPI_LIB_H_ */
