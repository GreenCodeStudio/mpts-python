"""
import {MptsParserError} from "./MptsParserError";

export class AbstractParser {

    readUntill(regexp) {
        let ret = '';
        while (this.position < this.text.length) {
            const char = this.text[this.position];
            if (regexp.test(char))
                break;
            ret += char;
            this.position++;
        }
        return ret;
    }

    skipWhitespace() {
        this.readUntill(/\S/)
    }

    readUntillText(text) {
        let ret = '';
        while (this.position < this.text.length) {
            const char = this.text[this.position];
            if (this.text.substr(this.position, text.length) == text)
                break;
            ret += char;
            this.position++;
        }
        return ret;
    }

    throw(message) {
        let lines = this.text.substr(0, this.position).split('\n');
        throw new MptsParserError(message, lines.length, lines[lines.length - 1].length, this.text.substr(this.position, 10))
    }
}
"""
import re


class AbstractParser:
    def readUntill(self, regexp):
        ret = ''
        while self.position < len(self.text):
            char = self.text[self.position]
            if re.match(regexp,char):
                break
            ret += char
            self.position += 1
        return ret

    def skipWhitespace(self):
        self.readUntill(r'\S')

    def readUntillText(self, text):
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
