"""
export class MptsParserError extends Error{
constructor(message, line, column, sample) {
    super(message+'\r\n'+sample.replace(/\n/g, '\\n')+'\r\n'+line+":"+column);
    this.messageRaw=message;
    this.line=line;
    this.column=column;
    this.sample=sample;
}
}
"""
class MptsParserError(Exception):
    def __init__(self, message, line, column, sample):
        super().__init__(f"{message}\r\n{sample}\r\n{line}:{column}")
        self.messageRaw = message
        self.line = line
        self.column = column
        self.sample = sample
