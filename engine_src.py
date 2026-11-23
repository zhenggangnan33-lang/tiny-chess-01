import json,os,sys,random,urllib.request
ENV=os.environ.get("MAKEFUN_ENV_URL") or sys.exit(1)
V=[0,100,320,330,500,900,0];PH=[0,0,1,1,2,4,0]
ND=[14,18,31,33,-14,-18,-31,-33];KD=[16,-16,1,-1,17,15,-15,-17]
OD=[16,-16,1,-1];DD=[17,15,-15,-17];CF=[0,1,2,3,3,2,1,0]
F="abcdefgh";AJ=[2,5,10,20,40,80,160,64];SQ=[s for s in range(128) if not s&0x88];PP=[0,8,16,32,55,85,120];PE=[0,12,24,48,80,120,170]
random.seed(1);Z=[random.getrandbits(64) for _ in range(1690)]
def zi(p,s):return Z[(p+6)*128+s]
ZS=Z[13*128]
def zc(c):return Z[13*128+1+c]
def ze(e):return Z[13*128+17+(e%16 if e>=0 else 8)]
B=[0]*128;H=0;CR=0;EP=-1;HM=0;SD=1;WK=4;BK=116;ST=[];N=0;NB=150000;T={}
KL=[[0,0] for _ in range(200)];HI=[0]*16384;PTH=[];GH={};NPM=0
def pf(f):
 global B,H,CR,EP,HM,SD,WK,BK,NPM,PTH,ST
 PTH=[];ST=[];p=f.split();B=[0]*128;H=0
 for i,row in enumerate(p[0].split("/")):
  r=7-i;fl=0
  for c in row:
   if c.isdigit():fl+=int(c)
   else:
    sq=r*16+fl;pc="PNBRQK".index(c.upper())+1
    if c.islower():pc=-pc
    B[sq]=pc;H^=zi(pc,sq)
    if pc==6:WK=sq
    elif pc==-6:BK=sq
    fl+=1
 SD=1 if p[1]=="w" else -1;NPM=0
 for q in B:
  if q and abs(q) not in(1,6):NPM+=V[abs(q)]
 CR=0
 if p[2]!="-":
  for c in p[2]:CR|={"K":1,"Q":2,"k":4,"q":8}[c]
 EP=-1 if p[3]=="-" else F.index(p[3][0])+(int(p[3][1])-1)*16
 HM=int(p[4]) if len(p)>4 else 0
 if SD<0:H^=ZS
 H^=zc(CR)^ze(EP)
def lk():return at(WK if SD<0 else BK,SD)
def at(s,by):
 d=16 if by>0 else -16
 for o in(d-1,d+1):
  t=s-o
  if t&0x88==0 and B[t]==by:return True
 for o in ND:
  t=s+o
  if t&0x88==0 and B[t]==by*2:return True
 for o in KD:
  t=s+o
  if t&0x88==0 and B[t]==by*6:return True
 for o in OD:
  t=s+o
  while t&0x88==0:
   q=B[t]
   if q:
    if q==by*4 or q==by*5:return True
    break
   t+=o
 for o in DD:
  t=s+o
  while t&0x88==0:
   q=B[t]
   if q:
    if q==by*3 or q==by*5:return True
    break
   t+=o
 return False
def mk(m):
 global H,CR,EP,HM,SD,WK,BK,NPM
 fr=m&127;to=(m>>7)&127;pr=(m>>14)&7;cap=(m>>17)&7;fl=(m>>20)&7;pc=B[fr]
 ST.append((m,cap,CR,EP,HM,H))
 H^=zi(pc,fr)^ZS^zc(CR)^ze(EP)
 if cap:
  cs=to if not(fl&2) else to-16*SD;H^=zi(B[cs],cs);B[cs]=0
  if cap>1:NPM-=V[cap]
 if pr:NPM+=V[pr]
 B[fr]=0;B[to]=(SD*pr) if pr else pc;H^=zi(B[to],to)
 if fl&4:
  rs,rt=(to+1,to-1) if to in(6,118) else (to-2,to+1)
  rp=B[rs];H^=zi(rp,rs)^zi(rp,rt);B[rt]=rp;B[rs]=0
 if abs(pc)==6:
  if SD>0:WK=to;CR&=~3
  else:BK=to;CR&=~12
 if fr==7 or to==7:CR&=~1
 if fr==0 or to==0:CR&=~2
 if fr==119 or to==119:CR&=~4
 if fr==112 or to==112:CR&=~8
 EP=(fr+to)//2 if(fl&1) else -1
 HM=0 if abs(pc)==1 or cap else HM+1
 H^=zc(CR)^ze(EP);SD=-SD
def um():
 global H,CR,EP,HM,SD,WK,BK,NPM
 m,cap,cr,ep,hm,h=ST.pop();fr=m&127;to=(m>>7)&127;pr=(m>>14)&7;fl=(m>>20)&7
 SD=-SD;H,CR,EP,HM=h,cr,ep,hm;pc=B[to];B[to]=0;B[fr]=SD if pr else pc
 if cap>1:NPM+=V[cap]
 if pr:NPM-=V[pr]
 if pc==6 or pc==-6:
  if SD>0:WK=fr
  else:BK=fr
 if cap:
  cs=to if not(fl&2) else to-16*SD;B[cs]=-SD*cap
 if fl&4:
  rs,rt=(to+1,to-1) if to in(6,118) else (to-2,to+1)
  B[rs]=B[rt];B[rt]=0
def gen(co):
 ms=[]
 for s in range(128):
  if s&0x88:continue
  p=B[s]
  if not p or(p>0)!=(SD>0):continue
  a=abs(p)
  if a==1:
   d=16*SD;t=s+d
   if not co and B[t]==0:
    if(t>>4)==(7 if SD>0 else 0):
     for pr in(5,4,3,2):ms.append(s|(t<<7)|(pr<<14))
    else:
     ms.append(s|(t<<7))
     if(s>>4)==(1 if SD>0 else 6) and B[s+2*d]==0:ms.append(s|((s+2*d)<<7)|(1<<20))
   for o in(d-1,d+1):
    t=s+o
    if t&0x88:continue
    q=B[t]
    if q and(q>0)!=(SD>0):
     c=abs(q)
     if(t>>4)==(7 if SD>0 else 0):
      for pr in(5,4,3,2):ms.append(s|(t<<7)|(pr<<14)|(c<<17))
     else:ms.append(s|(t<<7)|(c<<17))
    elif t==EP and EP>=0:ms.append(s|(t<<7)|(1<<17)|(2<<20))
  elif a==2:
   for o in ND:
    t=s+o
    if t&0x88:continue
    q=B[t]
    if q==0:
     if not co:ms.append(s|(t<<7))
    elif(q>0)!=(SD>0):ms.append(s|(t<<7)|(abs(q)<<17))
  elif a==6:
   for o in KD:
    t=s+o
    if t&0x88:continue
    q=B[t]
    if q==0:
     if not co:ms.append(s|(t<<7))
    elif(q>0)!=(SD>0):ms.append(s|(t<<7)|(abs(q)<<17))
   if not co and s==(WK if SD>0 else BK) and not at(s,-SD):
    if SD>0:
     if CR&1 and B[5]==0 and B[6]==0 and B[7]==4 and not at(5,-1) and not at(6,-1):ms.append(4|(6<<7)|(4<<20))
     if CR&2 and B[3]==0 and B[2]==0 and B[1]==0 and B[0]==4 and not at(3,-1) and not at(2,-1):ms.append(4|(2<<7)|(4<<20))
    else:
     if CR&4 and B[117]==0 and B[118]==0 and B[119]==-4 and not at(117,1) and not at(118,1):ms.append(116|(118<<7)|(4<<20))
     if CR&8 and B[115]==0 and B[114]==0 and B[113]==0 and B[112]==-4 and not at(115,1) and not at(114,1):ms.append(116|(114<<7)|(4<<20))
  else:
   ry=OD if a==4 else DD if a==3 else OD+DD
   for o in ry:
    t=s+o
    while t&0x88==0:
     q=B[t]
     if q==0:
      if not co:ms.append(s|(t<<7))
     else:
      if(q>0)!=(SD>0):ms.append(s|(t<<7)|(abs(q)<<17))
      break
     t+=o
 return ms
def mo(m,t,ply):
 if m==t:return 1<<20
 c=(m>>17)&7;pr=(m>>14)&7
 if c:return 10000+V[c]*16-V[abs(B[m&127])]+(V[pr] if pr else 0)
 if pr:return 9000+V[pr]
 if m==KL[ply][0]:return 8000
 if m==KL[ply][1]:return 7000
 return HI[(m&127)*128+((m>>7)&127)]
def ev():
 mg=eg=ph=0;wp=bp=0;wpr=[8]*8;bpr=[-1]*8;wpc=[0]*8;bpc=[0]*8;wb=bb=0;rk=[];ps=[]
 for s in SQ:
  p=B[s]
  if not p:continue
  f=s&7;r=s>>4;rr=r if p>0 else 7-r;ce=CF[f]+CF[rr];a=abs(p);ph+=PH[a]
  if a==1:
   ps.append(s)
   if p>0:
    wp|=1<<f;wpc[f]+=1
    if rr<wpr[f]:wpr[f]=rr
    mg+=100+rr*6+CF[f]*3;eg+=100+rr*10+CF[f]*2
   else:
    bp|=1<<f;bpc[f]+=1
    if r>bpr[f]:bpr[f]=r
    mg-=100+rr*6+CF[f]*3;eg-=100+rr*10+CF[f]*2
  elif a==2:
   mg+=(320+ce*6) if p>0 else-(320+ce*6);eg+=(320+ce*4) if p>0 else-(320+ce*4)
  elif a==3:
   mg+=(330+ce*5) if p>0 else-(330+ce*5);eg+=(330+ce*3) if p>0 else-(330+ce*3)
   if p>0:wb+=1
   else:bb+=1
  elif a==4:
   mg+=(500+(12 if rr==6 else 0)+CF[f]*2) if p>0 else-(500+(12 if rr==6 else 0)+CF[f]*2)
   eg+=(500+(8 if rr==6 else 0)) if p>0 else-(500+(8 if rr==6 else 0));rk.append(s)
  elif a==5:
   mg+=(900+ce*3) if p>0 else-(900+ce*3);eg+=(900+ce*5) if p>0 else-(900+ce*5)
  else:
   mg-=ce*6 if p>0 else-ce*6;eg+=ce*9 if p>0 else-ce*9;rk.append(s)
 if wb>=2:mg+=25;eg+=35
 if bb>=2:mg-=25;eg-=35
 for s in ps:
  p=B[s];f=s&7;r=s>>4
  if p>0:
   pas=True
   for ff in(f-1,f,f+1):
    if 0<=ff<=7 and bpr[ff]>r:pas=False;break
   if pas:mg+=PP[r];eg+=PE[r]
   if wpc[f]>1:mg-=8;eg-=12
   if not(wp&AJ[f]):mg-=8;eg-=10
  else:
   rr=7-r;pas=True
   for ff in(f-1,f,f+1):
    if 0<=ff<=7 and wpr[ff]<r:pas=False;break
   if pas:mg-=PP[rr];eg-=PE[rr]
   if bpc[f]>1:mg+=8;eg+=12
   if not(bp&AJ[f]):mg+=8;eg+=10
 for s in rk:
  p=B[s];f=s&7
  if abs(p)==4:
   own=wp if p>0 else bp;foe=bp if p>0 else wp;sg=1 if p>0 else-1
   if not(own&(1<<f)) and not(foe&(1<<f)):mg+=sg*12;eg+=sg*10
   elif not(own&(1<<f)):mg+=sg*6;eg+=sg*5
  else:
   d=16 if p>0 else-16;sh=0
   for o in(d-1,d,d+1):
    t=s+o
    if t&0x88==0 and B[t]==(1 if p>0 else-1):sh+=1
   if p>0:mg-=(3-sh)*10;eg-=(3-sh)*6
   else:mg+=(3-sh)*10;eg+=(3-sh)*6
 sc=(mg*ph+eg*(24-ph))//24 if ph<=24 else mg
 return(sc+8)*SD
class AB(Exception):pass
def qs(a,b,ply):
 global N;N+=1
 if N>NB:raise AB
 ks=WK if SD>0 else BK;ik=at(ks,-SD)
 if ik:
  ms=gen(False);ms.sort(key=lambda m:mo(m,0,ply),reverse=True)
  for m in ms:
   mk(m)
   if lk():um();continue
   sc=-qs(-b,-a,ply+1);um()
   if sc>=b:return b
   if sc>a:a=sc
  return a if ms else-30000+ply
 st=ev()
 if st>=b:return b
 if st>a:a=st
 ms=gen(True);ms.sort(key=lambda m:mo(m,0,ply),reverse=True)
 for m in ms:
  c=(m>>17)&7;pr=(m>>14)&7
  if st+V[c]+(V[pr] if pr else 0)+200<a:continue
  mk(m)
  if lk():um();continue
  sc=-qs(-b,-a,ply+1);um()
  if sc>=b:return b
  if sc>a:a=sc
 return a
def sr(d,a,b,ply):
 global N,H,EP,HM,SD;N+=1
 if N>NB:raise AB
 if HM>=100 or H in PTH or GH.get(H,0)>=2:return 0
 ks=WK if SD>0 else BK;ik=at(ks,-SD)
 if ik:d+=1
 if d<=0:return qs(a,b,ply)
 e=T.get(H);tt=0
 if e:
  tt=e[3]
  if e[0]>=d:
   fl,sc=e[1],e[2]
   if fl==0:return sc
   if fl==1:a=max(a,sc)
   else:b=min(b,sc)
   if a>=b:return sc
 if d<=2 and not ik:
  v=ev()
  if v+150*d<=a:return qs(a,b,ply)
  if v-150*d>=b:return v
 if d>=3 and not ik and NPM>900 and b<29000:
  sv=(H,EP,HM,SD);H^=ZS^ze(EP);EP=-1;HM+=1;SD=-SD;H^=ze(EP)
  try:sc=-sr(d-4,-b,-b+1,ply+1)
  finally:H,EP,HM,SD=sv
  if sc>=b:return sc
 ms=gen(False);ms.sort(key=lambda m:mo(m,tt,ply),reverse=True);PTH.append(H)
 best=-30000;bm=0;fl=2;i=0
 for m in ms:
  mk(m)
  if lk():um();continue
  i+=1;cap=(m>>17)&7;pr=(m>>14)&7
  if i==1:sc=-sr(d-1,-b,-a,ply+1)
  else:
   rd=d-1
   if d>=3 and i>3 and not cap and not pr and not ik:rd=d-2
   sc=-sr(rd,-a-1,-a,ply+1)
   if sc>a and sc<b:sc=-sr(d-1,-b,-a,ply+1)
  um()
  if sc>best:
   best=sc;bm=m
   if sc>a:
    a=sc;fl=0
    if a>=b:
     fl=1
     if not cap:
      KL[ply][1]=KL[ply][0];KL[ply][0]=m
      HI[(m&127)*128+((m>>7)&127)]+=d*d
     break
 PTH.pop()
 if i==0:return-30000+ply if ik else 0
 if len(T)<400000:T[H]=(d,fl,best,bm)
 return best
def uc(m):
 s=F[m&7]+str(((m>>4)&7)+1)+F[(m>>7)&7]+str(((m>>11)&7)+1);pr=(m>>14)&7
 return s+("nbrq"[pr-2] if pr else "")
def ch():
 global N,PTH
 PTH=[];ms=gen(False);lg=[]
 for m in ms:
  mk(m)
  if not lk():lg.append(m)
  um()
 if not lg:return None
 if len(lg)==1:return lg[0]
 lg.sort(key=lambda m:mo(m,0,0),reverse=True);bm=lg[0];pr=0;d=1;N=0
 while d<=20:
  a,b=-30000,30000
  if d>1:a,b=pr-40,pr+40
  while True:
   try:
    cur=bm;ca=a
    for i,m in enumerate(lg):
     mk(m)
     if i==0:sc=-sr(d-1,-b,-a,1)
     else:
      sc=-sr(d-1,-a-1,-a,1)
      if sc>a and sc<b:sc=-sr(d-1,-b,-a,1)
     um()
     if sc>ca:ca=sc;cur=m
   except AB:return bm
   if ca<=a:a=-30000;continue
   if ca>=b:b=30000;continue
   break
  bm=cur;pr=ca;lg.sort(key=lambda m:mo(m,bm,0),reverse=True);d+=1
 return bm
def po(p,bo):
 r=urllib.request.Request(ENV+p,data=json.dumps(bo).encode(),headers={"content-type":"application/json"})
 try:
  with urllib.request.urlopen(r) as x:return json.load(x)
 except Exception as e:sys.exit(f"{p}: {e}")
def rh(mv):
 global GH;GH={}
 pf("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1");GH[H]=1
 for u in mv:
  fr=F.index(u[0])+(int(u[1])-1)*16;to=F.index(u[2])+(int(u[3])-1)*16
  pc=B[fr];cap=abs(B[to]) if B[to] else 0;fl=0
  if abs(pc)==1:
   if to==EP:fl=2;cap=1
   elif abs(to-fr)==32:fl=1
  if abs(pc)==6 and abs(to-fr)==2:fl=4
  pr="nbrq".index(u[4])+2 if len(u)==5 else 0
  mk(fr|(to<<7)|(pr<<14)|(cap<<17)|(fl<<20));GH[H]=GH.get(H,0)+1
if __name__=="__main__":
 while True:
  g=po("/game",{})
  if g["status"]=="done":break
  pf(g["fen"]);rh(g["moves"]);pf(g["fen"])
  while g["status"]=="your_move":
   m=ch()
   if m is None:break
   g=po("/move",{"game":g["game"],"move":uc(m)})
   if g["status"]=="your_move":pf(g["fen"]);rh(g["moves"]);pf(g["fen"])
  print(g["game"],g.get("outcome"),g.get("reason"),file=sys.stderr)
 print(g.get("wins"),g.get("draws"),g.get("losses"),file=sys.stderr)
