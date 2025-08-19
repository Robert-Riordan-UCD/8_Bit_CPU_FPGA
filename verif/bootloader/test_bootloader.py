import cocotb, pyuvm

from bootloader_pkg.test import Test

@cocotb.test
async def run_test(dut):
    await pyuvm.uvm_root().run_test("Test")