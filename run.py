from twHandler.handlerMethods import handler
from twParser.twParser import Parser
from twModules.atmos import Atmos
import signal
from twTesting import sensor_test
from twDevices.mcp9808 import MCP9808
from twDevices.testDevice import TestDevice
from twDevices.mpl2115a2 import MPL3115A2
from twDevices.htu21df import HTU21DF
from twDevices.pms5003 import PMS5003
from twDevices.ultimateGPS import UltimateGPS
from twDevices.ads1115 import ADS1115
from twDevices.amg8833 import AMG8833
from twDevices.tsl2561 import TSL2561
from twDevices.ccs811 import CCS811
from twDevices.sht31d import SHT31D

if __name__ == "__main__":
	try:
		parser = Parser(handler)  # make sure that the right transceiver device is selected in Parser.__init__()
		handler.register_object(parser, "parser")
		atmos = Atmos(handler, parser)
		# handler.register_object(atmos, "atmos")
		# mcp = MCP9808(atmos)
		# mpl = MPL3115A2(atmos)
		# htu = HTU21DF(atmos)
		# testdev = TestDevice(atmos)
		# pms = PMS5003(atmos)
		# gps = UltimateGPS(atmos)
		# ads = ADS1115(atmos)
		# amg = AMG8833(atmos)
		tsl = TSL2561(atmos)
		# ccs = CCS811(atmos)
		sht = SHT31D(atmos)
		
		parser.connect(port="/dev/tty.usbmodem141401")
		parser.run()
		atmos.run()
		signal.pause()
	except KeyboardInterrupt:
		atmos.stop()
		parser.stop()
		print("Thank you for rolling with Team Tumbleweed\n\n")
		message = """\
████████╗███████╗ █████╗ ███╗   ███╗    ████████╗██╗   ██╗███╗   ███╗██████╗ ██╗     ███████╗██╗    ██╗███████╗███████╗██████╗ 
╚══██╔══╝██╔════╝██╔══██╗████╗ ████║    ╚══██╔══╝██║   ██║████╗ ████║██╔══██╗██║     ██╔════╝██║    ██║██╔════╝██╔════╝██╔══██╗
   ██║   █████╗  ███████║██╔████╔██║       ██║   ██║   ██║██╔████╔██║██████╔╝██║     █████╗  ██║ █╗ ██║█████╗  █████╗  ██║  ██║
   ██║   ██╔══╝  ██╔══██║██║╚██╔╝██║       ██║   ██║   ██║██║╚██╔╝██║██╔══██╗██║     ██╔══╝  ██║███╗██║██╔══╝  ██╔══╝  ██║  ██║
   ██║   ███████╗██║  ██║██║ ╚═╝ ██║       ██║   ╚██████╔╝██║ ╚═╝ ██║██████╔╝███████╗███████╗╚███╔███╔╝███████╗███████╗██████╔╝
   ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝       ╚═╝    ╚═════╝ ╚═╝     ╚═╝╚═════╝ ╚══════╝╚══════╝ ╚══╝╚══╝ ╚══════╝╚══════╝╚═════╝ 
 ██╗ ██╗ ██████╗  ██████╗  █████╗ ██████╗ ████████╗ ██████╗ ███╗   ███╗ █████╗ ██████╗ ███████╗                                
████████╗██╔══██╗██╔═══██╗██╔══██╗██╔══██╗╚══██╔══╝██╔═══██╗████╗ ████║██╔══██╗██╔══██╗██╔════╝                                
╚██╔═██╔╝██████╔╝██║   ██║███████║██║  ██║   ██║   ██║   ██║██╔████╔██║███████║██████╔╝███████╗                                
████████╗██╔══██╗██║   ██║██╔══██║██║  ██║   ██║   ██║   ██║██║╚██╔╝██║██╔══██║██╔══██╗╚════██║                                
╚██╔═██╔╝██║  ██║╚██████╔╝██║  ██║██████╔╝   ██║   ╚██████╔╝██║ ╚═╝ ██║██║  ██║██║  ██║███████║                                
 ╚═╝ ╚═╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝╚═════╝    ╚═╝    ╚═════╝ ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝"""
print(message)
