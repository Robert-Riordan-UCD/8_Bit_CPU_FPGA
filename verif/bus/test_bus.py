import cocotb, pyuvm

from bus_pkg.test import Test

@cocotb.test
async def run_test(dut):
    await pyuvm.uvm_root().run_test("Test")