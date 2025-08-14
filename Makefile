# PI_USERNAME
include .secrets
export

all: fpga_interface.sv src/* tangnano9k.cst
	rm -rf ./build
	mkdir ./build
	make synth
	make pnr
	make bitstream

synth:
	yosys -p "read_verilog -D WAIT_TIME=13500000 -D DISPLAY_WAIT_TIME=7000000 -sv fpga_interface.sv; synth_gowin -json ./build/synth.json"

pnr: 
	nextpnr-gowin --json ./build/synth.json --write ./build/pnr.json --device GW1NR-LV9QN88PC6/I5 --family GW1N-9C --cst tangnano9k.cst

bitstream:
	gowin_pack -d GW1N-9C -o ./build/bitstream.fs ./build/pnr.json

push-to-pi:
	scp ./build/bitstream.fs ${PI_USERNAME}@${PI_IP_ADDRESS}:${PI_DIR}/bitstream.fs
	(echo cd ${PI_DIR}; echo pwd; echo make) | ssh ${PI_USERNAME}@${PI_IP_ADDRESS}

# test:
# 	cd verif/; make

# waves:
# 	cd verif/; make waves

clean:
	rm -rf build/
	cd verif; make clean