class ToolsManager:
    def __init__(self):
        self._tools_ls = {}


    def add_tool(self, tool):
        self._tools_ls[tool.__name__] = tool

    def add_tools(self, tools: list):
        for tool in tools:
            self.add_tool(tool)

    def get_tool(self, name: str):
        return self._tools_ls.get(name, None)


    def get_tools_dict(self) -> dict:
        return self._tools_ls
    
    def get_tools_list(self) -> list:
        return [x for _, x in self._tools_ls.items()]