"""
import {getUniqName} from "../../utils";
import {TEExpression} from "./TEExpression";

export class TEMethodCall extends TEExpression {
    source = "";
    args=[];

    constructor(source, args=[]) {
        super();
        this.source = source;
        this.args=[]
    }

    execute(env) {
        return this.source.execute(env)(...this.args.map(x=>x.execute(env)));
    }

    compileJS(scopedVariables = new Set()) {
        let code=this.source.compileJS(scopedVariables).code;
        code+='(';
        code+=this.args.map(x=>x.compileJS(scopedVariables).code).join(',');
        code+=')';
        return {code};
    }
}
"""
class TEMethodCall:
    def __init__(self, source, args):
        self.source = source
        self.args = args
