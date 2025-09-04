from pyuvm import uvm_env, uvm_sequencer

from .driver import Driver
from .monitor import Monitor
from .scoreboard import Scoreboard
from .coverage import Coverage

class Env(uvm_env):
    def build_phase(self):
        self.logger.info("Build ENV")
        self.sequencer = uvm_sequencer("sequencer", self)
        self.driver = Driver(self)
        self.monitor = Monitor(self)
        self.scoreboard = Scoreboard(self)
        self.coverage = Coverage("coverage", self)
    
    def connect_phase(self):
        self.logger.info("Connect ENV")
        self.driver.seq_item_port.connect(self.sequencer.seq_item_export)
        self.monitor.analysis_port.connect(self.scoreboard.analysis_export)
        self.monitor.analysis_port.connect(self.coverage.analysis_export)