import sys


class Parser:
    def __init__(self, filename: str):
        self.filename = filename

    def start(self):
        finish_description = False
        with open(f"{self.filename}.epub.txt", "w", encoding="utf-8") as output:
            with open(f"{self.filename}.txt", encoding="utf-8") as lines:
                for line in lines:
                    if not finish_description:
                        if not self.parseDescription(line, output):
                            finish_description = True
                    else:
                        self.parseContent(line, output)

    def parseDescription(self, line: str, output):
        if line != "---\n":
            output.write(line)
            return True
        return False

    def parseContent(self, line: str, output):
        if line[0].isspace():
            output.write(line.lstrip())
        else:
            output.write(f"\n# {line}\n")


if __name__ == "__main__":
    parser = Parser(sys.argv[1])
    parser.start()
