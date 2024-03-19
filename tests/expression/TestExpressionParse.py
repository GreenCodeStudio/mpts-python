"""
import {expect} from "chai";
import {TEString} from "../../src/nodes/expressions/TEString";
import {TENumber} from "../../src/nodes/expressions/TENumber";
import {TEEqual} from "../../src/nodes/expressions/TEEqual";
import {TEProperty} from "../../src/nodes/expressions/TEProperty";
import {TEMethodCall} from "../../src/nodes/expressions/TEMethodCall";
import {TEOrNull} from "../../src/nodes/expressions/TEOrNull";

const {ExpressionParser} = require("../../src/parser/ExpressionParser");
const {TEVariable} = require("../../src/nodes/expressions/TEVariable");
const {TEBoolean} = require("../../src/nodes/expressions/TEBoolean");
const {TEConcatenate} = require("../../src/nodes/expressions/TEConcatenate");

describe('ExpressionTest', () => {
    describe('parse', () => {
        it('variable', async () => {
            const obj = ExpressionParser.Parse("var1");
            expect(obj).to.be.instanceOf(TEVariable)
            expect(obj.name).to.be.equal("var1")
        });
        it('boolTrue', async () => {
            const obj = ExpressionParser.Parse("true");
            expect(obj).to.be.instanceOf(TEBoolean)
            expect(obj.value).to.be.equal(true)
        });
        it('boolFalse', async () => {
            const obj = ExpressionParser.Parse("false");
            expect(obj).to.be.instanceOf(TEBoolean)
            expect(obj.value).to.be.equal(false)
        });
        it('property', async () => {
            const obj = ExpressionParser.Parse("var1.sub.sub2");
            expect(obj).to.be.instanceOf(TEProperty)
            expect(obj.name).to.be.equal("sub2")
            expect(obj.source).to.be.instanceOf(TEProperty)
            expect(obj.source.name).to.be.equal("sub")
            expect(obj.source.source).to.be.instanceOf(TEVariable)
            expect(obj.source.source.name).to.be.equal("var1")
        });
        it('number', async () => {
            const obj = ExpressionParser.Parse("123");
            expect(obj).to.be.instanceOf(TENumber)
            expect(obj.value).to.be.equal(123)
        });
        it('numberDecimal', async () => {
            const obj = ExpressionParser.Parse("1.23");
            expect(obj).to.be.instanceOf(TENumber)
            expect(obj.value).to.be.equal(1.23)
        });
        it('numberE', async () => {
            const obj = ExpressionParser.Parse("1.23e2");
            expect(obj).to.be.instanceOf(TENumber)
            expect(obj.value).to.be.equal(123)
        });
        it('string1', async () => {
            const obj = ExpressionParser.Parse("'text'");
            expect(obj).to.be.instanceOf(TEString)
            expect(obj.value).to.be.equal("text")
        });
        it('string2', async () => {
            const obj = ExpressionParser.Parse('"text"');
            expect(obj).to.be.instanceOf(TEString)
            expect(obj.value).to.be.equal("text")
        });
        it('equal', async () => {
            const obj = ExpressionParser.Parse('a==b');
            expect(obj).to.be.instanceOf(TEEqual)
            expect(obj.left).to.be.instanceOf(TEVariable)
            expect(obj.left.name).to.be.equal("a")
            expect(obj.right).to.be.instanceOf(TEVariable)
            expect(obj.right.name).to.be.equal("b")
        });
        it('equal double', async () => {
            const obj = ExpressionParser.Parse('(a==b)==(c==d)');
            expect(obj).to.be.instanceOf(TEEqual)
            expect(obj.left).to.be.instanceOf(TEEqual)
            expect(obj.left.left.name).to.be.equal("a")
            expect(obj.left.right.name).to.be.equal("b")
            expect(obj.right).to.be.instanceOf(TEEqual)
            expect(obj.right.left.name).to.be.equal("c")
            expect(obj.right.right.name).to.be.equal("d")
        });
        it('methodCall', async () => {
            const obj = ExpressionParser.Parse('fun(x)');
            expect(obj).to.be.instanceOf(TEMethodCall)
            expect(obj.source).to.be.instanceOf(TEVariable)
            expect(obj.source.name).to.be.equal("fun")
            expect(obj.args[0]).to.be.instanceOf(TEVariable)
            expect(obj.args[0].name).to.be.equal("x")
        });
        it('methodCallMultiArgument', async () => {
            const obj = ExpressionParser.Parse('fun(x,y,z)');
            expect(obj).to.be.instanceOf(TEMethodCall)
            expect(obj.source).to.be.instanceOf(TEVariable)
            expect(obj.source.name).to.be.equal("fun")
            expect(obj.args[0]).to.be.instanceOf(TEVariable)
            expect(obj.args[0].name).to.be.equal("x")
            expect(obj.args[1]).to.be.instanceOf(TEVariable)
            expect(obj.args[1].name).to.be.equal("y")
            expect(obj.args[2]).to.be.instanceOf(TEVariable)
            expect(obj.args[2].name).to.be.equal("z")
        });
        it('methodCallString', async () => {
            const obj = ExpressionParser.Parse('fun("x")');
            expect(obj).to.be.instanceOf(TEMethodCall)
            expect(obj.source).to.be.instanceOf(TEVariable)
            expect(obj.source.name).to.be.equal("fun")
            expect(obj.args[0]).to.be.instanceOf(TEString)
            expect(obj.args[0].value).to.be.equal("x")
        });
        it('concatenation', async () => {
            const obj = ExpressionParser.Parse('var1:var2');
            expect(obj).to.be.instanceOf(TEConcatenate)
            expect(obj.left).to.be.instanceOf(TEVariable)
            expect(obj.left.name).to.be.equal("var1")
            expect(obj.right).to.be.instanceOf(TEVariable)
            expect(obj.right.name).to.be.equal("var2")
        });
        it('concatenation string', async () => {
            const obj = ExpressionParser.Parse('"string1":var2');
            expect(obj).to.be.instanceOf(TEConcatenate)
            expect(obj.left).to.be.instanceOf(TEString)
            expect(obj.left.value).to.be.equal("string1")
            expect(obj.right).to.be.instanceOf(TEVariable)
            expect(obj.right.name).to.be.equal("var2")
        });
        it('orNull', async () => {
            const obj = ExpressionParser.Parse('var1??"empty"');
            expect(obj).to.be.instanceOf(TEOrNull)
            expect(obj.left).to.be.instanceOf(TEVariable)
            expect(obj.left.name).to.be.equal("var1")
            expect(obj.right).to.be.instanceOf(TEString)
            expect(obj.right.value).to.be.equal("empty")
        });
        it('orNullProperty', async () => {
            const obj = ExpressionParser.Parse('var1.property??"empty"');
            expect(obj).to.be.instanceOf(TEOrNull)
            expect(obj.left).to.be.instanceOf(TEProperty)
            expect(obj.left.name).to.be.equal("property")
            expect(obj.left.source).to.be.instanceOf(TEVariable)
            expect(obj.left.source.name).to.be.equal("var1")
            expect(obj.right).to.be.instanceOf(TEString)
            expect(obj.right.value).to.be.equal("empty")
        });
    });
});

"""

import unittest

from mpts.nodes.expressions.TEBoolean import TEBoolean
from mpts.nodes.expressions.TEConcatenate import TEConcatenate
from mpts.nodes.expressions.TEEqual import TEEqual
from mpts.nodes.expressions.TEMethodCall import TEMethodCall
from mpts.nodes.expressions.TENumber import TENumber
from mpts.nodes.expressions.TEOrNull import TEOrNull
from mpts.nodes.expressions.TEProperty import TEProperty
from mpts.nodes.expressions.TEString import TEString
from mpts.nodes.expressions.TEVariable import TEVariable
from mpts.parser.ExpressionParser import ExpressionParser


class TestExpressionParse(unittest.TestCase):
    def test_variable(self):
        obj = ExpressionParser.Parse("var1")
        self.assertIsInstance(obj, TEVariable)
        self.assertEqual(obj.name, "var1")

    def test_boolTrue(self):
        obj = ExpressionParser.Parse("true")
        self.assertIsInstance(obj, TEBoolean)
        self.assertEqual(obj.value, True)

    def test_boolFalse(self):
        obj = ExpressionParser.Parse("false")
        self.assertIsInstance(obj, TEBoolean)
        self.assertEqual(obj.value, False)

    def test_property(self):
        obj = ExpressionParser.Parse("var1.sub.sub2")
        self.assertIsInstance(obj, TEProperty)
        self.assertEqual(obj.name, "sub2")
        self.assertIsInstance(obj.source, TEProperty)
        self.assertEqual(obj.source.name, "sub")
        self.assertIsInstance(obj.source.source, TEVariable)
        self.assertEqual(obj.source.source.name, "var1")

    def test_number(self):
        obj = ExpressionParser.Parse("123")
        self.assertIsInstance(obj, TENumber)
        self.assertEqual(obj.value, 123)

    def test_numberDecimal(self):
        obj = ExpressionParser.Parse("1.23")
        self.assertIsInstance(obj, TENumber)
        self.assertEqual(obj.value, 1.23)

    def test_numberE(self):
        obj = ExpressionParser.Parse("1.23e2")
        self.assertIsInstance(obj, TENumber)
        self.assertEqual(obj.value, 123)

    def test_string1(self):
        obj = ExpressionParser.Parse("'text'")
        self.assertIsInstance(obj, TEString)
        self.assertEqual(obj.value, "text")

    def test_string2(self):
        obj = ExpressionParser.Parse('"text"')
        self.assertIsInstance(obj, TEString)
        self.assertEqual(obj.value, "text")

    def test_equal(self):
        obj = ExpressionParser.Parse('a==b')
        self.assertIsInstance(obj, TEEqual)
        self.assertIsInstance(obj.left, TEVariable)
        self.assertEqual(obj.left.name, "a")
        self.assertIsInstance(obj.right, TEVariable)
        self.assertEqual(obj.right.name, "b")

    def test_equal_double(self):
        obj = ExpressionParser.Parse('(a==b)==(c==d)')
        self.assertIsInstance(obj, TEEqual)
        self.assertIsInstance(obj.left, TEEqual)
        self.assertEqual(obj.left.left.name, "a")
        self.assertEqual(obj.left.right.name, "b")
        self.assertIsInstance(obj.right, TEEqual)
        self.assertEqual(obj.right.left.name, "c")
        self.assertEqual(obj.right.right.name, "d")

    def test_methodCall(self):
        obj = ExpressionParser.Parse('fun(x)')
        self.assertIsInstance(obj, TEMethodCall)
        self.assertIsInstance(obj.source, TEVariable)
        self.assertEqual(obj.source.name, "fun")
        self.assertIsInstance(obj.args[0], TEVariable)
        self.assertEqual(obj.args[0].name, "x")

    def test_methodCallMultiArgument(self):
        obj = ExpressionParser.Parse('fun(x,y,z)')
        self.assertIsInstance(obj, TEMethodCall)
        self.assertIsInstance(obj.source, TEVariable)
        self.assertEqual(obj.source.name, "fun")
        self.assertIsInstance(obj.args[0], TEVariable)
        self.assertEqual(obj.args[0].name, "x")
        self.assertIsInstance(obj.args[1], TEVariable)
        self.assertEqual(obj.args[1].name, "y")
        self.assertIsInstance(obj.args[2], TEVariable)
        self.assertEqual(obj.args[2].name, "z")

    def test_methodCallString(self):
        obj = ExpressionParser.Parse('fun("x")')
        self.assertIsInstance(obj, TEMethodCall)
        self.assertIsInstance(obj.source, TEVariable)
        self.assertEqual(obj.source.name, "fun")
        self.assertIsInstance(obj.args[0], TEString)
        self.assertEqual(obj.args[0].value, "x")

    def test_concatenation(self):
        obj = ExpressionParser.Parse('var1:var2')
        self.assertIsInstance(obj, TEConcatenate)
        self.assertIsInstance(obj.left, TEVariable)
        self.assertEqual(obj.left.name, "var1")
        self.assertIsInstance(obj.right, TEVariable)
        self.assertEqual(obj.right.name, "var2")

    def test_concatenation_string(self):
        obj = ExpressionParser.Parse('"string1":var2')
        self.assertIsInstance(obj, TEConcatenate)
        self.assertIsInstance(obj.left, TEString)
        self.assertEqual(obj.left.value, "string1")
        self.assertIsInstance(obj.right, TEVariable)
        self.assertEqual(obj.right.name, "var2")

    def test_orNull(self):
        obj = ExpressionParser.Parse('var1??"empty"')
        self.assertIsInstance(obj, TEOrNull)
        self.assertIsInstance(obj.left, TEVariable)
        self.assertEqual(obj.left.name, "var1")
        self.assertIsInstance(obj.right, TEString)
        self.assertEqual(obj.right.value, "empty")

    def test_orNullProperty(self):
        obj = ExpressionParser.Parse('var1.property??"empty"')
        self.assertIsInstance(obj, TEOrNull)
        self.assertIsInstance(obj.left, TEProperty)
        self.assertEqual(obj.left.name, "property")
        self.assertIsInstance(obj.left.source, TEVariable)
        self.assertEqual(obj.left.source.name, "var1")
        self.assertIsInstance(obj.right, TEString)
        self.assertEqual(obj.right.value, "empty")


if __name__ == '__main__':
    unittest.main()
