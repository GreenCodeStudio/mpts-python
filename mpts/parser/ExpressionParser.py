"""
import {TDocumentFragment} from "../nodes/TDocumentFragment";
import {TEVariable} from "../nodes/expressions/TEVariable";
import {TEBoolean} from "../nodes/expressions/TEBoolean";
import {TENumber} from "../nodes/expressions/TENumber";
import {TEString} from "../nodes/expressions/TEString";
import {TEEqual} from "../nodes/expressions/TEEqual";
import {AbstractParser} from "./AbstractParser";
import {TEProperty} from "../nodes/expressions/TEProperty";
import {TEMethodCall} from "../nodes/expressions/TEMethodCall";
import {TEConcatenate} from "../nodes/expressions/TEConcatenate";
import {TEAdd} from "../nodes/expressions/TEAdd";
import {TESubtract} from "../nodes/expressions/TESubtract";
import {TEOrNull} from "../nodes/expressions/TEOrNull";

export class ExpressionParser extends AbstractParser {
    constructor(text) {
        super();
        this.text = text;
        this.position = 0;
    }

    static Parse(text, endLevel=0) {
        return (new ExpressionParser(text)).parseNormal(endLevel);
    }

    parseNormal(endLevel = 0) {
        let lastNode = null;
        while (this.position < this.text.length) {
            const char = this.text[this.position];
            if (/\s/.test(char)) {
                this.position++;
            } else if (lastNode && char == '.') {
                this.position++;
                let name = this.readUntill(/['"\(\)=\.:\s>+\-*?]/);
                lastNode = new TEProperty(lastNode, name);
            } else if (/[0-9\.]/.test(char)) {
                this.position++;
                let value = char+this.readUntill(/[^0-9\.e]/);
                lastNode = new TENumber(+value);
            } else if (char == '"') {
                this.position++;
                let value = this.readUntill(/"/);
                this.position++;
                lastNode = new TEString(value);
            } else if (char == "'") {
                this.position++;
                let value = this.readUntill(/'/);
                this.position++;
                lastNode = new TEString(value);
            } else if (char == "(") {
                if (lastNode) {
                    lastNode = new TEMethodCall(lastNode);
                    this.position++;
                    this.skipWhitespace();
                    while (this.text[this.position] != ')') {
                        if (this.position >= this.text.length) throw new Error('Unexpected end of input');

                        let value = this.parseNormal(2);
                        lastNode.args.push(value);
                        if(this.text[this.position] ==',')
                            this.position++;
                    }
                    this.position++;
                } else {
                    this.position++;
                    let value = this.parseNormal(1);
                    this.position++;
                    lastNode = value;
                }
            } else if (char == ")") {
                if (endLevel >= 1) {
                    break;
                } else {
                    throw new Error("( not opened");
                }
            } else if (char == "=" && this.text[this.position + 1] == "=") {
                this.position += 2;
                let right = this.parseNormal(2);
                lastNode = new TEEqual(lastNode, right);
            }  else if (char == "?"&& this.text[this.position + 1] == "?") {
                if (endLevel >= 5) {
                    break;
                }
                this.position+=2;
                let right = this.parseNormal(5);
                lastNode = new TEOrNull(lastNode, right);
            } else if (char == ",") {
                if (endLevel >= 2) {
                    break;
                }
                else {
                    throw new Error("Unexpected character");
                }
            }else if (char == "+") {
                if (endLevel >= 4) {
                    break;
                }
                this.position++;
                let right = this.parseNormal(4);
                lastNode = new TEAdd(lastNode, right);
            } else if (char == "-") {
                if (endLevel >= 4) {
                    break;
                }
                this.position++;
                let right = this.parseNormal(4);
                lastNode = new TESubtract(lastNode, right);
            } else if (char == ":") {
                this.position++;
                let right = this.parseNormal(3);
                lastNode = new TEConcatenate(lastNode, right);
            } else if (char == ">" || char == "\\") {
                if (lastNode) {
                    break
                } else {
                    throw new Error("Unexpected character");
                }
            } else {
                if (lastNode) {
                    break;
                }
                let name = this.readUntill(/['"\(\)=\.\s:>/+\-*?,]/);
                if (name == 'true')
                    lastNode = new TEBoolean(true)
                else if (name == 'false')
                    lastNode = new TEBoolean(false)
                else
                    lastNode = new TEVariable(name);
            }
        }
        return lastNode;
    }

}

"""
import re

from mpts.nodes.expressions.TEAdd import TEAdd
from mpts.nodes.expressions.TEBoolean import TEBoolean
from mpts.nodes.expressions.TEConcatenate import TEConcatenate
from mpts.nodes.expressions.TEEqual import TEEqual
from mpts.nodes.expressions.TEMethodCall import TEMethodCall
from mpts.nodes.expressions.TENumber import TENumber
from mpts.nodes.expressions.TEOrNull import TEOrNull
from mpts.nodes.expressions.TEProperty import TEProperty
from mpts.nodes.expressions.TEString import TEString
from mpts.nodes.expressions.TESubtract import TESubtract
from mpts.nodes.expressions.TEVariable import TEVariable
from mpts.parser.AbstractParser import AbstractParser


class ExpressionParser(AbstractParser):
    def __init__(self, text):
        self.text = text
        self.position = 0

    @staticmethod
    def Parse(text, endLevel=0):
        return (ExpressionParser(text)).parseNormal(endLevel)

    def parseNormal(self, endLevel=0):
        lastNode = None
        while self.position < len(self.text):
            char = self.text[self.position]
            if re.search(r'\s', char):
                self.position += 1
            elif lastNode and char == '.':
                self.position += 1
                name = self.readUntill(r"['\"\(\)=\.:\s>+\-*?]")
                lastNode = TEProperty(lastNode, name)
            elif re.search(r'[0-9\.]', char):
                self.position += 1
                value = char + self.readUntill(r'[^0-9\.e]')
                lastNode = TENumber(float(value))
            elif char == '"':
                self.position += 1
                value = self.readUntill(r'"')
                self.position += 1
                lastNode = TEString(value)
            elif char == "'":
                self.position += 1
                value = self.readUntill(r"'")
                self.position += 1
                lastNode = TEString(value)
            elif char == "(":
                if lastNode:
                    lastNode = TEMethodCall(lastNode)
                    self.position += 1
                    self.skipWhitespace()
                    while self.text[self.position] != ')':
                        if self.position >= len(self.text):
                            raise Error('Unexpected end of input')
                        value = self.parseNormal(2)
                        lastNode.args.append(value)
                        if self.text[self.position] == ',':
                            self.position += 1
                    self.position += 1
                else:
                    self.position += 1
                    value = self.parseNormal(1)
                    self.position += 1
                    lastNode = value
            elif char == ")":
                if endLevel >= 1:
                    break
                else:
                    raise Error("( not opened")
            elif char == "=" and self.text[self.position + 1] == "=":
                self.position += 2
                right = self.parseNormal(2)
                lastNode = TEEqual(lastNode, right)
            elif char == "?" and self.text[self.position + 1] == "?":
                if endLevel >= 5:
                    break
                self.position += 2
                right = self.parseNormal(5)
                lastNode = TEOrNull(lastNode, right)
            elif char == ",":
                if endLevel >= 2:
                    break
                else:
                    raise Error("Unexpected character")
            elif char == "+":
                if endLevel >= 4:
                    break
                self.position += 1
                right = self.parseNormal(4)
                lastNode = TEAdd(lastNode, right)
            elif char == "-":
                if endLevel >= 4:
                    break
                self.position += 1
                right = self.parseNormal(4)
                lastNode = TESubtract(lastNode, right)
            elif char == ":":
                self.position += 1
                right = self.parseNormal(3)
                lastNode = TEConcatenate(lastNode, right)
            elif char == ">" or char == "\\":
                if lastNode:
                    break
                else:
                    raise Error("Unexpected character")
            else:
                if lastNode:
                    break
                name = self.readUntill(r"['\"\(\)=\.\s:>/+\-*?,]")
                if name == 'true':
                    lastNode = TEBoolean(True)
                elif name == 'false':
                    lastNode = TEBoolean(False)
                else:
                    lastNode = TEVariable(name)
        return lastNode

