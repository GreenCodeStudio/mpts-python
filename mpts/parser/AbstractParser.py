
import re

from mpts.parser.MptsParserError import MptsParserError


class AbstractParser:
    def __init__(self, text, position=0):
        self.text = text
        self.position = position

    def readUntil(self, regexp):
        ret = ''
        while self.position < len(self.text):
            char = self.text[self.position]
            if re.match(regexp, char):
                break
            ret += char
            self.position += 1
        return ret

    def skipWhitespace(self):
        self.readUntil(r'\S')

    def readUntilText(self, text):
        ret = ''
        while self.position < len(self.text):
            char = self.text[self.position]
            if self.text[self.position:self.position + len(text)] == text:
                break
            ret += char
            self.position += 1
        return ret

    def throw(self, message):
        lines = self.text[:self.position].split('\n')
        raise MptsParserError(message, len(lines), len(lines[-1]), self.text[self.position:self.position + 10])
