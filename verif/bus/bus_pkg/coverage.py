from pyuvm import uvm_subscriber, uvm_analysis_export, uvm_error
import math

def intxz(value):
    try:
        return int(value)
    except ValueError: # X and Z
        return

class Coverage(uvm_subscriber):
    def __init__(self, parent, name="coverage"):
        super().__init__(name, parent)
        self.logger.info("Init COV")

        self.input_data = dict()

        self.no_driver = set()

        self.lanes = set()
        self.lane_width = -1

        self.bus_outputs = set()
        self.bus_width = -1

    def write(self, op):
        self.logger.info("Write COV")

        if op.select == 0:
            self.no_driver.add(True)
            return
        self.no_driver.add(False)

        self.lane_width = max(self.lane_width, op.LANES)
        self.bus_width = max(self.bus_width, op.WIDTH)

        if not (l := intxz(op.select)) is None:
            self.lanes.add(intxz(l))
        
        if not (o := intxz(op.bus)) is None:
            self.bus_outputs.add(intxz(o))
        
        if not (l := intxz(op.select)) is None:
            if not (o := intxz(op.bus)) is None:
                try:
                    lane_data = self.input_data[l]
                except KeyError:
                    lane_data = set()
                lane_data.add(o)
                self.input_data[l] = lane_data
        

    def report_phase(self):
        self.logger.info("Report COV")

        assert False in self.no_driver, "Select never set"
        assert True in self.no_driver, "Select always set. No driver not tested"
        
        lane_cov = len(self.lanes)/self.lane_width
        if lane_cov == 1:
            self.logger.info(f"Coverage: All lanes selected")
        elif lane_cov > 0.8:
            self.logger.warning(f"Coverage MISS: {100*lane_cov:0.1f}% of lanes covered ({len(self.lanes)}/{self.lane_width})")
        else:
            self.logger.error(f"Coverage MISS: {100*lane_cov:0.1f}% of lanes covered ({len(self.lanes)}/{self.lane_width})")

        output_cov = len(self.bus_outputs)/(2**self.bus_width)
        if output_cov == 1:
            self.logger.info(f"Coverage: All bus outputs covered")
        elif output_cov > 0.8:
            self.logger.warning(f"Coverage MISS: {100*output_cov:0.1f}% bus outputs covered ({len(self.bus_outputs)}/{2**self.bus_width})")
        else:
            self.logger.error(f"Coverage MISS: {100*output_cov:0.1f}% bus outputs covered ({len(self.bus_outputs)}/{2**self.bus_width})")
        
        for lane, data in self.input_data.items():
            data_cov = len(data)/(2**self.bus_width)
            if data_cov == 1:
                self.logger.info(f"Coverage: All inputs covered for lane {int(math.log2(lane))}")
            elif data_cov > 0.8:
                self.logger.warning(f"Coverage MISS: {100*data_cov:0.1f}% lane {int(math.log2(lane))} inputs covered ({len(data)}/{2**self.bus_width})")
            else:
                self.logger.error(f"Coverage MISS: {100*data_cov:0.1f}% lane {int(math.log2(lane))} inputs covered ({len(data)}/{2**self.bus_width})")
        

        # print(self.input_data)
