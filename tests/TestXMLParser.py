"""
const {expect} = require("chai");
const {XMLParser} = require("../src/parser/XMLParser");
const {TDocumentFragment} = require("../src/nodes/TDocumentFragment");
const {TText} = require("../src/nodes/TText");
const {TElement} = require("../src/nodes/TElement");
const {TAttribute} = require("../src/nodes/TAttribute");
const {TIf} = require("../src/nodes/TIf");
const {TEVariable} = require("../src/nodes/expressions/TEVariable");
const {TEString} = require("../src/nodes/expressions/TEString");
const {TEBoolean} = require("../src/nodes/expressions/TEBoolean");
const {TENumber} = require("../src/nodes/expressions/TENumber");
const {TLoop} = require("../src/nodes/TLoop");
const {TComment} = require("../src/nodes/TComment");
const {TForeach} = require("../src/nodes/TForeach");
const {MptsParserError} = require("../src/parser/MptsParserError");
const {TEOrNull} = require("../src/nodes/expressions/TEOrNull");
const {TEProperty} = require("../src/nodes/expressions/TEProperty");
const {TEMethodCall} = require("../src/nodes/expressions/TEMethodCall");
const {UniParserTest} = require("./UniParserTest");

describe('XMLParser', () => {
    UniParserTest(XMLParser);


    it('not closed element', async () => {
        expect(()=>XMLParser.Parse("<div>")).to.throw(MptsParserError);
        expect(()=>XMLParser.Parse("<div>")).to.throw(/Element <div> not closed/);
        expect(()=>XMLParser.Parse("<div>")).to.throw(/1:5/);
    });

    it('bad order of close', async () => {
        expect(()=>XMLParser.Parse("<span><strong></span></strong>")).to.throw(MptsParserError);
        expect(()=>XMLParser.Parse("<span><strong></span></strong>")).to.throw(/Last opened element is not <span>/);
    });

    describe('cases from real life', () => {
        it('1', async () => {
            const obj = XMLParser.Parse("<input name=\"realizationTime\" type=\"number\" step=\"0.01\" value=(data.realizationTime??t('roomsList.sumPrice.realizationTime.value')) />");
            expect(obj).to.be.instanceOf(TDocumentFragment);
            expect(obj.children[0]).to.be.instanceOf(TElement);
            expect(obj.children[0].attributes[0]).to.be.instanceOf(TAttribute);
            expect(obj.children[0].attributes[0].name).to.be.equals("name");
            expect(obj.children[0].attributes[0].expression).to.be.instanceOf(TEString);
            expect(obj.children[0].attributes[0].expression.value).to.be.equal("realizationTime");
            expect(obj.children[0].attributes[1]).to.be.instanceOf(TAttribute);
            expect(obj.children[0].attributes[1].name).to.be.equals("type");
            expect(obj.children[0].attributes[1].expression).to.be.instanceOf(TEString);
            expect(obj.children[0].attributes[1].expression.value).to.be.equal("number");
            expect(obj.children[0].attributes[2]).to.be.instanceOf(TAttribute);
            expect(obj.children[0].attributes[2].name).to.be.equals("step");
            expect(obj.children[0].attributes[2].expression).to.be.instanceOf(TEString);
            expect(obj.children[0].attributes[2].expression.value).to.be.equal("0.01");
            expect(obj.children[0].attributes[3]).to.be.instanceOf(TAttribute);
            expect(obj.children[0].attributes[3].name).to.be.equals("value");
            expect(obj.children[0].attributes[3].expression).to.be.instanceOf(TEOrNull);
            expect(obj.children[0].attributes[3].expression.left).to.be.instanceOf(TEProperty);
            expect(obj.children[0].attributes[3].expression.left.source).to.be.instanceOf(TEVariable);
            expect(obj.children[0].attributes[3].expression.right).to.be.instanceOf(TEMethodCall);
            expect(obj.children[0].attributes[3].expression.right.source).to.be.instanceOf(TEVariable);

        });
    });

})

"""


"""
import {parser} from "../src";
import {expect} from "chai";
import {TDocumentFragment} from "../src/nodes/TDocumentFragment";
import {TText} from "../src/nodes/TText";
import {TElement} from "../src/nodes/TElement";
import {MptsParserError} from "../src/parser/MptsParserError";
import {TAttribute} from "../src/nodes/TAttribute";
import {TEString} from "../src/nodes/expressions/TEString";
import {TEVariable} from "../src/nodes/expressions/TEVariable";
import {TEMethodCall} from "../src/nodes/expressions/TEMethodCall";
import {TComment} from "../src/nodes/TComment";
import {TIf} from "../src/nodes/TIf";
import {TEBoolean} from "../src/nodes/expressions/TEBoolean";
import {TLoop} from "../src/nodes/TLoop";
import {TENumber} from "../src/nodes/expressions/TENumber";
import {TForeach} from "../src/nodes/TForeach";

export function UniParserTest(parser){
    it('basic text', async () => {
        const obj = parser.Parse("Hello, world!");
        expect(obj).to.be.instanceOf(TDocumentFragment);
        expect(obj.children[0]).to.be.instanceOf(TText);
        expect(obj.children[0].text).to.be.equals("Hello, world!");
    });

    it('basic element', async () => {
        const obj = parser.Parse("<br/>");
        expect(obj).to.be.instanceOf(TDocumentFragment);
        expect(obj.children[0]).to.be.instanceOf(TElement);
        expect(obj.children[0].tagName).to.be.equals("br");
    });
    it('basic element2', async () => {
        const obj = parser.Parse("<div></div>");
        expect(obj).to.be.instanceOf(TDocumentFragment);
        expect(obj.children[0]).to.be.instanceOf(TElement);
        expect(obj.children[0].tagName).to.be.equals("div");
    });
    it('not opened element', async () => {
        expect(()=>parser.Parse("</div>")).to.throw(MptsParserError);
        expect(()=>parser.Parse("</div>")).to.throw(/Last opened element is not <div>/);
        expect(()=>parser.Parse("</div>")).to.throw(/1:0/);
    });
    it('elementsinside', async () => {
        const obj = parser.Parse("<div><p><strong></strong><span></span></p></div>");
        expect(obj.children[0]).to.be.instanceOf(TElement);
        expect(obj.children[0].tagName).to.be.equals("div");
        expect(obj.children[0].children[0]).to.be.instanceOf(TElement);
        expect(obj.children[0].children[0].tagName).to.be.equals("p");
        expect(obj.children[0].children[0].children[0]).to.be.instanceOf(TElement);
        expect(obj.children[0].children[0].children[0].tagName).to.be.equals("strong");
        expect(obj.children[0].children[0].children[1]).to.be.instanceOf(TElement);
        expect(obj.children[0].children[0].children[1].tagName).to.be.equals("span");
    });
    it('element with attributes', async () => {
        const obj = parser.Parse("<img src=\"a.png\" alt='a'/>");
        expect(obj).to.be.instanceOf(TDocumentFragment);
        expect(obj.children[0]).to.be.instanceOf(TElement);
        expect(obj.children[0].tagName).to.be.equals("img");
        expect(obj.children[0].attributes[0]).to.be.instanceOf(TAttribute);
        expect(obj.children[0].attributes[0].name).to.be.equals("src");
        expect(obj.children[0].attributes[0].expression).to.be.instanceOf(TEString);
        expect(obj.children[0].attributes[0].expression.value).to.be.equal("a.png");
        expect(obj.children[0].attributes[1]).to.be.instanceOf(TAttribute);
        expect(obj.children[0].attributes[1].name).to.be.equals("alt");
        expect(obj.children[0].attributes[1].expression).to.be.instanceOf(TEString);
        expect(obj.children[0].attributes[1].expression.value).to.be.equal("a");
    });

    it('element with attributes with variables', async () => {
        const obj = parser.Parse("<img src=(v1) alt=v2 class=(getClass())/>");
        expect(obj).to.be.instanceOf(TDocumentFragment);
        expect(obj.children[0]).to.be.instanceOf(TElement);
        expect(obj.children[0].tagName).to.be.equals("img");
        expect(obj.children[0].attributes[0]).to.be.instanceOf(TAttribute);
        expect(obj.children[0].attributes[0].name).to.be.equals("src");
        expect(obj.children[0].attributes[0].expression).to.be.instanceOf(TEVariable);
        expect(obj.children[0].attributes[0].expression.name).to.be.equal("v1");
        expect(obj.children[0].attributes[1]).to.be.instanceOf(TAttribute);
        expect(obj.children[0].attributes[1].name).to.be.equals("alt");
        expect(obj.children[0].attributes[1].expression).to.be.instanceOf(TEVariable);
        expect(obj.children[0].attributes[1].expression.name).to.be.equal("v2");
        expect(obj.children[0].attributes[2]).to.be.instanceOf(TAttribute);
        expect(obj.children[0].attributes[2].name).to.be.equals("class");
        expect(obj.children[0].attributes[2].expression).to.be.instanceOf(TEMethodCall);
        expect(obj.children[0].attributes[2].expression.source).to.be.instanceOf(TEVariable);
        expect(obj.children[0].attributes[2].expression.source.name).to.be.equal("getClass");
    });

    it('element with boolean atributes', async () => {
        const obj = parser.Parse("<textarea required/>");
        expect(obj).to.be.instanceOf(TDocumentFragment);
        expect(obj.children[0]).to.be.instanceOf(TElement);
        expect(obj.children[0].tagName).to.be.equals("textarea");
        expect(obj.children[0].attributes[0]).to.be.instanceOf(TAttribute);
        expect(obj.children[0].attributes[0].name).to.be.equals("required");
        expect(obj.children[0].attributes[0].expression).to.be.equal(null);
    });

    it('comment', async () => {
        const obj = parser.Parse("<!--comment-->");
        expect(obj).to.be.instanceOf(TDocumentFragment);
        expect(obj.children[0]).to.be.instanceOf(TComment);
        expect(obj.children[0].text).to.be.equals("comment");
    });
    it('2 comments', async () => {
        const obj = parser.Parse("<!--comment1--><!--comment2-->");
        expect(obj).to.be.instanceOf(TDocumentFragment);
        expect(obj.children[0]).to.be.instanceOf(TComment);
        expect(obj.children[0].text).to.be.equals("comment1");
        expect(obj.children[1]).to.be.instanceOf(TComment);
        expect(obj.children[1].text).to.be.equals("comment2");
    });

    it('if', async () => {
        const obj = parser.Parse("<:if condition=false>text</:if><:else>text</:else>");
        expect(obj).to.be.instanceOf(TDocumentFragment);
        expect(obj.children[0]).to.be.instanceOf(TIf);
        expect(obj.children[0].conditions[0].expression).to.be.instanceOf(TEBoolean);
        expect(obj.children[0].conditions[0].children[0]).to.be.instanceOf(TText);
        expect(obj.children[0].else.children[0]).to.be.instanceOf(TText);
    });
    it('loop', async () => {
        const obj = parser.Parse("<:loop count=10>b</:loop>");
        expect(obj).to.be.instanceOf(TDocumentFragment);
        expect(obj.children[0]).to.be.instanceOf(TLoop);
        expect(obj.children[0].count).to.be.instanceOf(TENumber);
        expect(obj.children[0].count.value).to.be.equal(10);
        expect(obj.children[0].children[0]).to.be.instanceOf(TText);
        expect(obj.children[0].children[0].text).to.be.equal('b');
    })
    it('foreach basic', async () => {
        const obj = parser.Parse("<:foreach collection=a>b</:foreach>");
        expect(obj).to.be.instanceOf(TDocumentFragment);
        expect(obj.children[0]).to.be.instanceOf(TForeach);
        expect(obj.children[0].collection).to.be.instanceOf(TEVariable);
        expect(obj.children[0].collection.name).to.be.equal('a');
        expect(obj.children[0].children[0]).to.be.instanceOf(TText);
        expect(obj.children[0].children[0].text).to.be.equal('b');
    });
    it('foreach advanced', async () => {
        const obj = parser.Parse("<:foreach collection=a item=b key=c><div>{{c}}:{{b}}</div></:foreach>");
        expect(obj).to.be.instanceOf(TDocumentFragment);
        expect(obj.children[0]).to.be.instanceOf(TForeach);
        expect(obj.children[0].collection).to.be.instanceOf(TEVariable);
        expect(obj.children[0].collection.name).to.be.equal('a');
        expect(obj.children[0].item).to.be.equal('b');
        expect(obj.children[0].key).to.be.equal('c');
        expect(obj.children[0].children[0]).to.be.instanceOf(TElement);
    });
    it('foreach inside element', async () => {
        const obj = parser.Parse("<select><:foreach collection=a>b</:foreach></select>");
        expect(obj).to.be.instanceOf(TDocumentFragment);
        expect(obj.children[0]).to.be.instanceOf(TElement);
        expect(obj.children[0].children[0]).to.be.instanceOf(TForeach);
    });

    it('comment after element', async () => {
        const obj = parser.Parse("<tr data-amount=article.amount><!--comment--></tr>");
        expect(obj).to.be.instanceOf(TDocumentFragment);
        expect(obj.children[0]).to.be.instanceOf(TElement);
        expect(obj.children[0].children[0]).to.be.instanceOf(TComment);
    });
}

"""
import unittest

from mpts.nodes.TDocumentFragment import TDocumentFragment
from mpts.nodes.TText import TText
from .context import mpts

from mpts.parser import XMLParser


class TestXMLParser():
    def __init__(self):
        self.parser = XMLParser
        pass;

    def test_basicTest(self):
        obj = self.parser.Parse("Hello, world!")
        self.assertIsInstance(obj, TDocumentFragment)
        self.assertIsInstance(obj.children[0], TText)
        self.assertEqual(obj.children[0].text, "Hello, world!")

if __name__ == '__main__':
    unittest.main()
