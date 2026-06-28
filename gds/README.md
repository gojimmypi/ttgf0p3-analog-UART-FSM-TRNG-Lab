# Setup notes


See:

- https://tinytapeout.com/specs/analog/
- https://www.youtube.com/watch?v=DQAA4MrG8pM
- https://github.com/RTimothyEdwards/magic.git
- https://github.com/TinyTapeout/tt-support-tools/tree/main/tech/gf180mcuD

### Toolchain

```bash
sudo apt update

sudo apt install -y python3-tk
sudo apt install -y magic

mkdir ~/ttsetup
python3 -m venv ~/ttsetup/venv
source ~/ttsetup/venv/bin/activate

pip install -r /mnt/c/workspace/tt-support-tools-gojimmypi/requirements.txt

# also needed
python3 -m pip install gdstk

export PDK_ROOT=~/ttsetup/pdk
export PDK=gf180mcuD
export LIBRELANE_TAG=3.0.3

pip install librelane==$LIBRELANE_TAG

git clone https://github.com/TinyTapeout/tt-support-tools tt

cd /mnt/c/workspace/ttgf0p3-analog-UART-FSM-TRNG-Lab/

mkdir -p gds lef mag 

/mnt/c/workspace/tt-support-tools-gojimmypi/tt_tool.py --create-user-config

/mnt/c/workspace/tt-support-tools-gojimmypi/tt_tool.py --gf --harden --no-docker

export PDK_ROOT="$HOME/ttsetup/pdk/ciel/gf180mcu/versions/54435919abffb937387ec956209f9cf5fd2dfbee"
export PDK=gf180mcuD

which magic
magic --version
ls -l mag

./tools/export_magic_gds_lef.sh
```

### Python environment

```
gojimmypi:~
$ mkdir ~/ttsetup
python3 -m venv ~/ttsetup/venv
source ~/ttsetup/venv/bin/activate
(venv) gojimmypi:~
$ pip install -r /mnt/c/workspace/tt-support-tools-gojimmypi/requirements.txt
```

Install magic

See https://github.com/RTimothyEdwards/magic.git

```bash
cd "$HOME/ttsetup"

sudo apt update
sudo apt install -y \
    build-essential git m4 csh tcsh \
    libx11-dev tcl-dev tk-dev \
    libcairo2-dev libncurses-dev \
    libglu1-mesa-dev freeglut3-dev mesa-common-dev


cd /mnt/c/workspace
git clone https://github.com/RTimothyEdwards/magic.git
cd magic

./configure --prefix="$HOME/ttsetup/magic"
make -j"$(nproc)"
make install

export PATH="$HOME/ttsetup/magic/bin:$PATH"
which magic
magic --version
```


## Populate `mag` directory

** NOTE ** The `def` files have moved since [the video](https://www.youtube.com/watch?v=DQAA4MrG8pM) was recorded. 
It is no longer in the root, rather one of the platforms in [tech](https://github.com/TinyTapeout/tt-support-tools/tree/main/tech).

In the case of this project:

https://github.com/TinyTapeout/tt-support-tools/tree/main/tech/gf180mcuD/def


Fetch some key files:

```
cd /mnt/c/workspace/ttgf0p3-analog-UART-FSM-TRNG-Lab/

# Get the analog template
cd mag
wget https://raw.githubusercontent.com/TinyTapeout/tt-support-tools/refs/heads/gf180mcu-analog/tech/gf180mcuD/def/analog/tt_analog_1x2.def


# Fetch the magic script
wget https://github.com/TinyTapeout/tt-support-tools/blob/tt10/def/analog/magic_init_project.tcl

# magic_init_project.tcl edited as appropriate
```


Edits to `magic_init_project.tcl`:

```
set TOP_LEVEL_CELL     tt_um_gojimmypi_ttgfa_UART_FSM_TRNG_Lab
set TEMPLATE_FILE      tt_analog_1x2.def
```

