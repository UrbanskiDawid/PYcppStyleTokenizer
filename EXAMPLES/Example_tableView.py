import sys
sys.path.append("..") # Adds location od PYcppStyleTokenizer.py to python modules path.

from PYcppStyleTokenizer import tokenize

input = '''//comment1
void functionA(int a,int b)
{
  int a1[2] = {1,0};

  int banana2[2][2] = {
   {0, 1},   /*  row 0 */
   {4, 5},   /*  row 1 */
  };

/*multi
line
 comment2*/
int c = 0;
 "this is a \\"string\\""
 {
        a = b + c *  0.05;
 }
if(a <= b) { f_do(a); }


for(int i=0;i<10;i++)
{
  print( functionA(i,i) );
}

}'''

print "== INPUT =========================================="
line=0
for lineStr in input.split("\n"):
  print '%4d: %s' % (line,lineStr)
  line+=1

print "==================================================="

print "== OUTPUT: ========================================"
line = 0

def twoLiner(a,b):
  l=len(a)
  if len(b)>l: l=len(b)
  return (a.ljust(l),b.ljust(l))
  
lineA=lineB="|"
for token in tokenize(input):

  if line!= token.line:
    line=token.line
    print lineA+"\n"+lineB
    lineA=lineB="|"

  ab=twoLiner(token.typ,token.value.replace("\n","\\n"))

  lineA+=ab[0]+"|"
  lineB+=ab[1]+"|"

print "==================================================="
