import sys
sys.path.append("..") # Adds location od PYcppStyleTokenizer.py to python modules path.

from PYcppStyleTokenizer import tokenize

input = '''//comment1
void functionA(int a,int b)
{
 for(int i=0;i<10;i++){  print(i);}
}

int functionB() { return 1;}
int b();//ass

void c(){
}'''

print "== INPUT =========================================="
line=0
for lineStr in input.split("\n"):
  line+=1
  print '%4d: %s' % (line,lineStr)
print "==================================================="

print "== OUTPUT: (depth 0 declarations) ================="
inside=False
prevToken=False
for token in tokenize(input):

  if token.blockDepth!=0:
    inside=False
    continue

  if inside==False or prevToken.typ=='END':
    inside=True
    print "definition:"

  argSpc = '' #indentation of arguments
  if token.argDepth:
    argSpc = ''.join([ '-' for i in range(0,token.argDepth) ])+'>'

  print '[%4d:%4d]: %10s %s %s' % (token.line,token.column,token.typ,argSpc, token.value)
  prevToken=token

print "==================================================="
