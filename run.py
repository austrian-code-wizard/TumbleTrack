from twHandler.handlerMethods import handler
from twParser.twParser import Parser
from twModules.atmos import Atmos
from twDevices.mcp9808 import MCP9808
from twDevices.testDevice import TestDevice
from twDevices.mpl2115a2 import MPL3115A2
from twDevices.htu21df import HTU21DF
from twDevices.pms5003 import PMS5003
from twDevices.ultimateGPS import UltimateGPS

if __name__ == "__main__":
	parser = Parser(handler) # make sure that the right transceiver device is selected in Parser.__init__()
	handler.register_object(parser, "parser")
	atmos = Atmos(handler, parser)
	handler.register_object(atmos, "atmos")
	#mcp = MCP9808(atmos)
	#handler.register_object(mcp, "mcp")
	#mpl = MPL3115A2(atmos)
	#handler.register_object(mpl, "mpl")
	#htu = HTU21DF(atmos)
	#handler.register_object(htu, "htu")
	#testdev = TestDevice(atmos)
	#handler.register_object(testdev, "testdev")
	#pms = PMS5003(atmos)
	#handler.register_object(pms, "pms")
	gps = UltimateGPS(atmos)
	handler.register_object(gps, "gps")
	parser.connect(port="/dev/tty.usbmodem141401")
	parser.run()
	atmos.run()
