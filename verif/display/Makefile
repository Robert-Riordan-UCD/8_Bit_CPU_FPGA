DUT ?= display
TOPLEVEL_LANG = verilog
VERILOG_SOURCES = ../../src/$(DUT).sv ./tb_$(DUT).sv
VERILOG_SOURCES += ../../src/clock.sv
TOPLEVEL = tb_$(DUT)
# Python test module
MODULE = test_$(DUT)
PYUVM = 1
SIM = icarus
WAVES = 1

# cocotb Makefiles
include $(shell cocotb-config --makefiles)/Makefile.sim

waves:
	gtkwave sim_build/tb_$(DUT).fst &
