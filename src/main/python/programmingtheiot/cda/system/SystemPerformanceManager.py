#####
# 
# This class is part of the Programming the Internet of Things project.
# 
# It is provided as a simple shell to guide the student and assist with
# implementation for the Programming the Internet of Things exercises,
# and designed to be modified by the student as needed.
#

import logging

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers import SchedulerNotRunningError

import programmingtheiot.common.ConfigConst as ConfigConst

from programmingtheiot.common.ConfigUtil import ConfigUtil
from programmingtheiot.common.IDataMessageListener import IDataMessageListener

from programmingtheiot.cda.system.SystemCpuUtilTask import SystemCpuUtilTask
from programmingtheiot.cda.system.SystemMemUtilTask import SystemMemUtilTask

from programmingtheiot.data.SystemPerformanceData import SystemPerformanceData

class SystemPerformanceManager(object):
    """
    Shell representation of class for student implementation.
    
    """

    def __init__(self):
        logging.info("Initializing System PerormanceManager...")

        configUtil = ConfigUtil()
        self.poolRate = configUtil.getInteger(
            section=ConfigConst.CONSTRAINED_DEVICE,
            key=ConfigConst.POLL_CYCLES_KEY,
            defaultVal=ConfigConst.DEFAULT_POLL_CYCLES
        )
        self.getlocationId = configUtil.getProperty(
            section=ConfigConst.CONSTRAINED_DEVICE,
            key=ConfigConst.DEVICE_LOCATION_ID_KEY,
            defaultVal=ConfigConst.NOT_SET
        )
        if self.poolRate <= 0:
            self.poolRate = ConfigConst.DEFAULT_POLL_CYCLES
            
        self.dataMsgListener = None
        
        self.scheduler = BackgroundScheduler()
        self.scheduler.add_job(self.handleTelemetry, 
                               trigger = 'interval', 
                               seconds = self.poolRate,
                               max_instances=2,
                               coalesce=True,
                               misfire_grace_time = 15
                               )

    def handleTelemetry(self):
        cpuUtilPct = SystemCpuUtilTask().getTelemetryValue()
        memUtilPct = SystemMemUtilTask().getTelemetryValue()

        logging.debug('CPU util is %.2f percent, and memory util is %.2f percent',
                      cpuUtilPct, memUtilPct)
        
    def setDataMessageListener(self, listener: IDataMessageListener) -> bool:
        pass
    
    def startManager(self):
        logging.info("Starting SystemPerformanceManager...")

        if not self.scheduler.running:
            self.scheduler.start()
            logging.info("Started SystemPerformanceManager")
        else:
            logging.info("SystemPerformanceManager already started. Ignoring.")
        
    def stopManager(self):
        logging.info("Stopping SystemPerformanceManager...")

        try:
            self.scheduler.shutdown()
            logging.info("Stopped SystemPerformanceManager")
        except SchedulerNotRunningError:
            logging.warning("SystemPerformanceManager scheduler already stopped. Ignoring.")
