import re
import os

class RawHelper():
    def __init__(self, filename):
        self._file = str(filename)
        self._format = r"^(.+?)\.\[([^\]]*)\]\:(.*)$"
        if not os.path.exists(filename):
            open(self._file, 'w').close()

    def read(self) -> dict:
        data = {}
        if not os.path.exists(self._file):
            return data
            
        with open(self._file, 'r') as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue
                match = re.match(self._format, line)
                if match:
                    id, author, msg = match.groups()
                    data[id] = {"author": author, "content": msg}
        return data
    
    def write(self, id, data: dict):
        author = data["author"]
        msg = data["content"]
        with open(self._file, 'a') as file:
            file.write(f"{id}.[{author}]:{msg}\n")

    def rewrite(self, datas: dict):
        with open(self._file, 'w') as file:
            for id, data in datas.items():
                author = data["author"]
                msg = data["content"]
                file.write(f"{id}.[{author}]:{msg}\n")