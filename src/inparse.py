from os import path, abort

def read(file):
    if (path.exists(file) == True):
        fd = open(file, "r")
        inf = fd.read()
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

    def magic(self, inf):
        blocks = inf.split(";\n")
        for i in blocks:
            border = i.index(":")
            block_name = i[:border]
            match block_name:
                case "__domains__":
                    self.domains = i[border + 2:].split(", ")
                case "__sertificates__":
                    None
                # Other points ...
