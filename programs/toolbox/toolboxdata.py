import programs.toolbox.tools.pen as pen
import programs.toolbox.tools.line as line
from enum import Enum
penTool = pen.Pen()
lineTool = line.Line()
class ToolboxData:
    class ToolType(Enum):
        PEN = 0
        LINE = 1
    def __init__(self):
        self.tools = [penTool, lineTool]
        self.current_tool = ToolboxData.ToolType.PEN
        self.tools[self.current_tool.value].enable_tool()
    def get_current_tool(self):
        return self.tools[self.current_tool.value]
    def set_current_tool(self, tool_name):
        self.get_current_tool().disable_tool()
        self.current_tool = tool_name
        self.get_current_tool().enable_tool()