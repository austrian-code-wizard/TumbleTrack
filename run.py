from twHandler.handlerMethods import handler
from twParser.twParser import Parser
from twModules.atmos import Atmos
from twDevices.mcp9808 import MCP9808

if __name__ == "__main__":
	parser = Parser(handler)
	handler.register_object(parser, "parser")
	atmos = Atmos(handler, parser)
	handler.register_object(atmos, "atmos")
	mcp = MCP9808(atmos)
	handler.register_object(mcp, "mcp")
	parser.connect()
	parser.run()
	atmos.run()
