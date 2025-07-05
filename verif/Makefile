TOPLEVEL_LANG = verilog
VERILOG_SOURCES = ../src/program_counter.sv ./tb_program_counter.sv
TOPLEVEL = tb_program_counter
# Python test module
MODULE = test_program_counter
PYUVM = 1
SIM = icarus
WAVES = 1

# cocotb Makefiles
include $(shell cocotb-config --makefiles)/Makefile.sim

waves:
	gtkwave sim_build/tb_program_counter.fst