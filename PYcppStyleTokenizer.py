import collections
import re

#strucure returned by 'tokenize'
Token = collections.namedtuple('Token', [
 'typ',         #name of type
 'value',       #string form imput
 'line',        #line mumber (0..n)
 'column',      #column in line (0...n)
 'blockDepth',  # {} block depth
 'argDepth'     # () arguments depth
]) 

def tokenize(input):
    keywords      = {'if', 'private', 'for', 'while', 'return'}
    keywordsTypes = {'void', 'int','float'}

    #token names starting with _ are not returned
    token_specification = [
        ('NUMBER',     r'\d+(\.\d*)?'),    # Integer or decimal number
        ('ASSIGN',     r'='),              # Assignment operator
        ('END',        r';'),              # Statement terminator
        ('NEXT',       r','),              # Argumnet separator
        ('BLOCKSTART',r'{'),               # Start of new block of code
        ('BLOCKEND',  r'}'),               # End of block of code
        ('ARGSTART',   r'\('),             # Start of new agrument block
        ('ARGEND',     r'\)'),             # End of argument block
        ('STRING',     r'"([^"\\]|\\.)*"'),# String (can contain quotes)
        ('ID',         r'[A-Za-z_]+'),     # Identifiers
        ('_COMMENT1',  r'\/\/[^\n]*'),     # single line comment
        ('_COMMENT2',  r'/\*.+?\*/'),      # multiline comment
        ('OP',         r'[+*\/\-]'),       # Arithmetic operators
        ('CMP',        r'[\<\>]\=?'),      # Comparators <,>,<=,>=
        ('_NL',        r'\n'),             # Line endings
        ('SKIP',       r'[ \t]')           # Skip over spaces and tabs
    ]
    tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification) #join all into one regexp
    get_token = re.compile(tok_regex,re.DOTALL).match #comile rexexp. '.' can be newnline

    line = pos = line_start = depth = arg =0 #values for while loop all 0

    mo = get_token(input)
    while mo is not None:
      typ = mo.lastgroup
      val = mo.group(typ)

      if typ != 'SKIP':
        if typ == 'BLOCKSTART':
          depth+=1
        if typ == 'ARGSTART':
          arg+=1
        if typ == '_NL' or typ == '_COMMENT1':
          line_start = pos
          line += 1
        if typ == '_COMMENT2':
          for x in val:
            if x=="\n":
              line+=1
        
        if typ[0] != '_': #ignore _TOKENs
          val = mo.group(typ)
          if typ == 'ID' and val in keywords: #translate ID to 'KEYWORD'
            typ = 'KEYWORD'
          elif  type == 'ID' and val in keywordsTypes: #translate ID to 'TYPE'
            typ = 'TYPE'
          yield Token(typ, val, line, mo.start()-line_start,depth,arg)

        if typ == 'ARGEND':
           arg-=1
        if typ == 'BLOCKEND':
          depth-=1
      #if skip

      pos = mo.end()
      mo = get_token(input, pos)
    #while
    if pos != len(input):
        raise RuntimeError('Unexpected character %r on line %d' %(input[pos], line))
