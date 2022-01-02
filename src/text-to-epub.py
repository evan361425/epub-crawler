import sys


class Parser:
    def __init__(self, filename: str):
        self.filename = filename

    def start(self):
        finishDescription = False
        with open(f"{self.filename}.epub.txt", "w") as output:
            self.output = output
            with open(f"{self.filename}.txt") as input:
                for line in input:
                    if not finishDescription:
                        if not self.parseDescription(line):
                            finishDescription = True
                    else:
                        self.parseContent(line)

    def parseDescription(self, line: str):
        if line != "---\n":
            self.output.write(line)
            return True
        else:
            return False

    def parseContent(self, line: str):
        if line[0].isspace():
            self.output.write(line.lstrip())
        else:
            self.output.write(f"\n# {line}\n")


if __name__ == "__main__":
    parser = Parser(sys.argv[1])
    parser.start()
