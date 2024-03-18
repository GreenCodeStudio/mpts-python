"""
import {getUniqName} from "../utils";
import {TNode} from "./TNode";

export class TDocumentFragment extends TNode{
    children = []

    execute(env) {
        let ret = env.document.createDocumentFragment();
        for (const child of this.children) {
            ret.appendChild(child.execute(env))
        }
        return ret;
    }

    compileJS(scopedVariables=new Set()) {
        let rootName = getUniqName();
        let code = 'const ' + rootName + '=document.createDocumentFragment();';
        for (const child of this.children) {
            let childResult = child.compileJS(scopedVariables);
            code += childResult.code;
            code += rootName + ".append(" + childResult.rootName + ");"
        }
        return {code, rootName};
    }
    compileJSVue(scopedVariables = new Set()) {
        return `[${this.children.map(x=>x.compileJSVue(scopedVariables)).join(',')}]`;
    }
}

"""
from mpts.nodes.TNode import TNode


class TDocumentFragment(TNode):
    def __init__(self):
        self.children = []

    def execute(self, env):
        ret = env.document.createDocumentFragment()
        for child in self.children:
            ret.appendChild(child.execute(env))
        return ret
