from pyuvm import uvm_component, uvm_analysis_export

class Coverage(uvm_component):
    def __init__(self, parent, name="coverage"):
        super().__init__(name, parent)
        self.logger.info("Init COV")
        self.analysis_export = uvm_analysis_export("analysis export", parent)
        self.covered_ops = set()
    
    def write(self, op):
        self.logger.info("Write COV")
        self.covered_ops.add((op.a, op.b, op.subtract))
