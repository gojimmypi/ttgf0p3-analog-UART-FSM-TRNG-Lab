#!/bin/bash

rm -f ./gds/tt_um_gojimmypi_ttgfa_UART_FSM_TRNG_Lab.gds
rm -f  ./lef/tt_um_gojimmypi_ttgfa_UART_FSM_TRNG_Lab.lef
rm -f  ./mag/tt_um_gojimmypi_ttgfa_UART_FSM_TRNG_Lab.mag

./tools/create_mag.sh            2>&1 | tee ./mag/mag.log

./tools/export_magic_gds_lef.sh  2>&1 | tee ./gds/gds.log
