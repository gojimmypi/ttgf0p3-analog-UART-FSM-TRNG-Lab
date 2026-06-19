#!/usr/bin/env bash
#
# Copyright (c) 2026 gojimmypi
# SPDX-License-Identifier: Apache-2.0
#
# file: show_effective_defines.sh

set -euo pipefail

# Run shellcheck to ensure this is a good script.
# Specify the executable shell checker you want to use:
MY_SHELLCHECK="shellcheck"

# Check if the executable is available in the PATH
if command -v "$MY_SHELLCHECK" >/dev/null 2>&1; then
    # Run your command here
    shellcheck "$0" || exit 1
else
    echo "$MY_SHELLCHECK is not installed. Please install it if changes to this script have been made."
fi

CONFIG="../src/project_config.v"
TARGET="FPGA"
HEADER_FILE=""
C_PREFIX=""
IVERILOG_ARGS=()

if [[ $# -gt 0 && "$1" != -* ]]; then
    CONFIG="$1"
    shift
fi

while [[ $# -gt 0 ]]; do
    case "$1" in
        --target)
            if [[ $# -lt 2 ]]; then
                echo "error: --target requires fpga or asic" >&2
                exit 1
            fi
            TARGET="$2"
            shift 2
            ;;
        --target=*)
            TARGET="${1#--target=}"
            shift
            ;;
        --header)
            if [[ $# -lt 2 ]]; then
                echo "error: --header requires an output file" >&2
                exit 1
            fi
            HEADER_FILE="$2"
            shift 2
            ;;
        --header=*)
            HEADER_FILE="${1#--header=}"
            shift
            ;;
        --prefix)
            if [[ $# -lt 2 ]]; then
                echo "error: --prefix requires a C macro prefix" >&2
                exit 1
            fi
            C_PREFIX="$2"
            shift 2
            ;;
        --prefix=*)
            C_PREFIX="${1#--prefix=}"
            shift
            ;;
        --)
            shift
            while [[ $# -gt 0 ]]; do
                IVERILOG_ARGS+=("$1")
                shift
            done
            ;;
        *)
            IVERILOG_ARGS+=("$1")
            shift
            ;;
    esac
done

TARGET="$(printf "%s" "$TARGET" | tr '[:lower:]' '[:upper:]')"

case "$TARGET" in
    FPGA | ASIC)
        ;;
    *)
        echo "error: --target must be fpga or asic" >&2
        exit 1
        ;;
esac

if [[ -z "$C_PREFIX" ]]; then
    C_PREFIX="TT_${TARGET}_MACRO_"
fi

if [[ ! "$C_PREFIX" =~ ^[A-Za-z_][A-Za-z0-9_]*$ ]]; then
    echo "error: C macro prefix is not a valid C identifier prefix: $C_PREFIX" >&2
    exit 1
fi

if [[ ! -f "$CONFIG" ]]; then
    echo "error: config file not found: $CONFIG" >&2
    exit 1
else
    echo "Configuration in: $(realpath -- "$CONFIG")"
fi

if ! command -v iverilog >/dev/null 2>&1; then
    echo "error: iverilog is required for Verilog preprocessing" >&2
    echo "install with: sudo apt install iverilog" >&2
    exit 1
fi

TMPDIR="$(mktemp -d)"
trap 'rm -rf "$TMPDIR"' EXIT

CONFIG_DIR="$(cd "$(dirname "$CONFIG")" && pwd)"
CONFIG_FILE="$(basename "$CONFIG")"
CONFIG_REAL="$(realpath -- "$CONFIG")"

NAMES_FILE="$TMPDIR/define_names.txt"
PROBE_FILE="$TMPDIR/show_effective_defines_probe.v"
OUT_FILE="$TMPDIR/preprocessed.txt"
EFFECTIVE_FILE="$TMPDIR/effective_defines.txt"

perl -0777 -ne '
    s{/\*.*?\*/}{}gs;
    s{//.*$}{}mg;
    while (/^\s*`(?:define|ifdef|ifndef)\s+([A-Za-z_][A-Za-z0-9_\$]*)/mg) {
        print "$1\n";
    }
' "$CONFIG" | sort -u > "$NAMES_FILE"

for arg in "${IVERILOG_ARGS[@]}"; do
    case "$arg" in
        -D*)
            name="${arg#-D}"
            name="${name%%=*}"
            if [[ -n "$name" ]]; then
                echo "$name" >> "$NAMES_FILE"
            fi
            ;;
    esac
done

sort -u "$NAMES_FILE" -o "$NAMES_FILE"

{
    echo '`default_nettype none'
    printf '`include "%s"\n' "$CONFIG_FILE"
    echo '__EFFECTIVE_DEFINES_BEGIN__'

    while IFS= read -r name; do
        [[ -n "$name" ]] || continue

        printf '`ifdef %s\n' "$name"
        printf '%s=`%s\n' "$name" "$name"
        printf '`else\n'
        printf '%s=<undefined>\n' "$name"
        printf '`endif\n'
    done < "$NAMES_FILE"

    echo '__EFFECTIVE_DEFINES_END__'
    echo '`default_nettype wire'
} > "$PROBE_FILE"

iverilog -E -g2012 -I "$CONFIG_DIR" "${IVERILOG_ARGS[@]}" "$PROBE_FILE" -o "$OUT_FILE"

awk '
    /^__EFFECTIVE_DEFINES_BEGIN__/ { show = 1; next }
    /^__EFFECTIVE_DEFINES_END__/   { show = 0; next }

    show {
        sub(/^[[:space:]]+/, "")
        sub(/[[:space:]]+$/, "")

        if ($0 == "") {
            next
        }

        if ($0 ~ /<undefined>$/) {
            next
        }

        if ($0 ~ /^[A-Za-z_][A-Za-z0-9_\$]*=$/) {
            print $0 " (defined)"
        } else {
            print
        }
    }
' "$OUT_FILE" | sort > "$EFFECTIVE_FILE"

cat "$EFFECTIVE_FILE"

if [[ -n "$HEADER_FILE" ]]; then
    HEADER_GUARD="${C_PREFIX}EFFECTIVE_DEFINES_H"
    HEADER_TMP="$TMPDIR/effective_defines.h"

    perl - "$C_PREFIX" "$HEADER_GUARD" "$TARGET" "$CONFIG_REAL" "$EFFECTIVE_FILE" > "$HEADER_TMP" <<'PERL'
        use strict;
        use warnings;

        my ($prefix, $guard, $target, $config, $input) = @ARGV;

        sub clean_comment {
            my ($text) = @_;
            $text =~ s{\*/}{* /}g;
            return $text;
        }

        sub c_name {
            my ($name) = @_;
            $name =~ s/[^A-Za-z0-9_]/_/g;
            return $name;
        }

        sub int_from_base {
            my ($digits, $base) = @_;
            my $value = 0;

            $digits =~ s/_//g;

            for my $ch (split //, $digits) {
                my $digit;

                if ($ch =~ /[0-9]/) {
                    $digit = ord($ch) - ord("0");
                } elsif ($ch =~ /[a-f]/) {
                    $digit = ord($ch) - ord("a") + 10;
                } elsif ($ch =~ /[A-F]/) {
                    $digit = ord($ch) - ord("A") + 10;
                } else {
                    return undef;
                }

                return undef if $digit >= $base;
                $value = ($value * $base) + $digit;
            }

            return "$value";
        }

        sub c_value {
            my ($value) = @_;

            $value =~ s/^\s+//;
            $value =~ s/\s+$//;

            return "1" if $value eq "" || $value eq "(defined)";

            if ($value =~ /^"([^"\\]|\\.)*"$/) {
                return $value;
            }

            if ($value =~ /^(?:\d+)?'\s*([bBoOdDhH])\s*([0-9a-fA-F_xXzZ?]+)$/) {
                my $base = lc($1);
                my $digits = $2;

                return undef if $digits =~ /[xXzZ?]/;
                $digits =~ s/_//g;

                if ($base eq "h") {
                    return "0x" . uc($digits) . "u";
                }

                if ($base eq "d") {
                    return $digits . "u";
                }

                if ($base eq "o") {
                    my $converted = int_from_base($digits, 8);
                    return undef if !defined $converted;
                    return $converted . "u";
                }

                if ($base eq "b") {
                    my $converted = int_from_base($digits, 2);
                    return undef if !defined $converted;
                    return $converted . "u";
                }
            }

            if ($value =~ /^\d[\d_]*$/) {
                $value =~ s/_//g;
                return $value . "u";
            }

            $value =~ s/(\d+)?'\s*[hH]\s*([0-9a-fA-F_]+)/do {
                my $digits = $2;
                $digits =~ s|_||g;
                "0x" . uc($digits) . "u";
            }/eg;

            $value =~ s/(\d+)?'\s*[dD]\s*([0-9_]+)/do {
                my $digits = $2;
                $digits =~ s|_||g;
                $digits . "u";
            }/eg;

            $value =~ s/(\d+)?'\s*[oO]\s*([0-7_]+)/do {
                my $digits = $2;
                my $converted = int_from_base($digits, 8);
                defined $converted ? $converted . "u" : $&;
            }/eg;

            $value =~ s/(\d+)?'\s*[bB]\s*([01_]+)/do {
                my $digits = $2;
                my $converted = int_from_base($digits, 2);
                defined $converted ? $converted . "u" : $&;
            }/eg;

            $value =~ s/(?<=\d)_(?=\d)//g;

            return undef if $value =~ /[{}@]/;
            return undef if $value =~ /'[A-Za-z]/;

            if ($value =~ /^[A-Za-z0-9_()+\-*\/\%&|^~!<>=?:.,\s]+$/) {
                return $value;
            }

            return undef;
        }

        open my $fh, "<", $input or die "error: cannot read $input: $!\n";

        print "/* Generated by show_effective_defines.sh. Do not edit. */\n";
        print "/* Source config: " . clean_comment($config) . " */\n";
        print "/* Target: " . clean_comment($target) . " */\n";
        print "\n";
        print "#ifndef $guard\n";
        print "#define $guard\n";
        print "\n";

        while (my $line = <$fh>) {
            chomp $line;

            next if $line eq "";

            my ($name, $value);

            if ($line =~ /^([A-Za-z_][A-Za-z0-9_\$]*)=\s+\(defined\)$/) {
                $name = $1;
                $value = "1";
            } elsif ($line =~ /^([A-Za-z_][A-Za-z0-9_\$]*)=(.*)$/) {
                $name = $1;
                $value = $2;
            } else {
                next;
            }

            my $macro = $prefix . c_name($name);
            my $converted = c_value($value);

            if (defined $converted) {
                print "#define $macro $converted\n";
            } else {
                print "/* $macro skipped: unsupported Verilog value: " . clean_comment($value) . " */\n";
            }
        }

        print "\n";
        print "#endif /* $guard */\n";
PERL

    mv "$HEADER_TMP" "$HEADER_FILE"
    echo "C header written: $(realpath -- "$HEADER_FILE")"
fi
