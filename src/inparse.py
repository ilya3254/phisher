import json
from os import path, abort

def read(file):
    if (path.exists(file) == True):
        fd = open(file, "r")
        inf = json.load(fd)
        fd.close()
        return inf
    else:
        print("read error: File does not exist")
        abort()

class Inparse:
    def __init__(self):
        self.domains = None
        self.sertificates = None
        # Other points ...
    def parse(self, inf):
        for i in inf:
            match i:
                case "domains":
                    self.domains = inf["domains"]
                case "sertificates":
                    self.sertificates = inf["sertificates"] # Just as example
                # Other points ...