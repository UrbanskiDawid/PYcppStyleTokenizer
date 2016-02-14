from PYcppStyleTokenizer import tokenize 

input = '''//comment1
void functionA(int a=10,int b=20)
{
/*multi
line
 comment2*/
int a = 0;
 "this is a \\"string\\""
 {
        a = b + c *  0.05;
 }
if(a <= b) {f_do(a);}

for(int i=0;i<10;i++)
{
  print(i);
}

}'''

print "== INPUT =========================================="
line=0
for lineStr in input.split("\n"):
 line+=1
 print '%4d: %s' % (line,lineStr)
print "==================================================="

print "\n== OUTPUT: ========================================"
line = -1
for token in tokenize(input):
  if line != token.line:
    line=token.line
    print "\nline %d:" % line

  argSpc = '' 
  if token.argDepth:
    argSpc = ''.join([ '-' for i in range(0,token.argDepth) ])+'>'

  blockSpc = ''
  if token.blockDepth:
    blockSpc= ''.join([ '-' for i in range(0,token.blockDepth) ])+'>'

  print '%s[%4d]: %10s %s %s' % (blockSpc,token.column,token.typ,argSpc, token.value)

print "\n==================================================="
