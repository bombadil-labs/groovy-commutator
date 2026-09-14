// Exact first-floor DT2 census. Compile: g++ -O3 -std=c++17 audit_dt2_holdouts.cpp -o audit_dt2_holdouts
// Source bit j of sample w represents coordinate j-5. Only dependency-safe
// central outputs/patches are used; radius-two probe dependencies are [-5,5].
#include <algorithm>
#include <array>
#include <chrono>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <sstream>
#include <string>
#include <vector>
using namespace std;
constexpr int N=2048,W=11,C=5;
constexpr uint32_t ZERO=1u<<18;
using Line=array<uint8_t,W>;
struct Data { array<uint8_t,5> a{},u{}; array<uint8_t,5> flip{},center{}; array<uint8_t,2> want{}; uint8_t source=0; };
const char* masks[]={"birth","death","stay_one","stay_zero"};
const char* gates[]={"native","source","raw","centered0","centered1"};
int at(int x){return (x+W)%W;}
Line deriv(const Line& x,int rule){Line y{};for(int i=0;i<W;i++)y[i]=((rule^204)>>(4*x[at(i-1)]+2*x[i]+x[at(i+1)]))&1;return y;}
Line xors(const Line& a,const Line& b){Line r{};for(int i=0;i<W;i++)r[i]=a[i]^b[i];return r;}
int maskbit(int x,int d,int m){if(m==0)return(1-x)&d;if(m==1)return x&d;if(m==2)return x&(1-d);return(1-x)&(1-d);}
int qbit(const Line& x,int i,int q){int a=q%2==0?-2:-1,b=q%2==0?1:2;int l=x[at(i+a)],r=x[at(i+b)];if(q==2)r^=1;if(q==3)l^=1;return l&r;}
uint32_t payload(int sample,int phase,bool probe,int raw,int src,int centered){return raw|(src<<1)|(centered<<2)|(probe<<3)|(phase<<4)|(sample<<7);}
uint32_t patch(const array<uint8_t,5>& row,const vector<int>& order,int phase){uint32_t k=0;int n=order.size();for(int dy=-2;dy<=2;dy++)k=(k<<5)|row[order[(phase+dy+n)%n]];return k;}
vector<Data> prepare(int rule,int m,int sign,int q){
 vector<Data> out(N);
 for(int w=0;w<N;w++){
  array<Line,4> s{};for(int i=0;i<W;i++)s[0][i]=(w>>i)&1;
  array<Line,3>d{};for(int t=0;t<3;t++){d[t]=deriv(s[t],rule);s[t+1]=xors(s[t],d[t]);}
  auto dd=deriv(d[0],rule);Line g{};for(int i=0;i<W;i++)g[i]=d[1][i]^d[0][i]^dd[i];
  auto& z=out[w];z.source=s[0][C];
  for(int x=C-2;x<=C+2;x++){
   array<int,5>a={s[0][x]^s[0][at(x+sign)],d[0][x],s[0][x]^s[2][x],maskbit(s[0][x],d[0][x],m),q<0?0:qbit(s[0],x,q)};
   array<int,5>b={s[1][x]^s[1][at(x+sign)],d[1][x],s[1][x]^s[3][x],maskbit(s[1][x],d[1][x],m),q<0?0:qbit(s[1],x,q)};
   for(int f=0;f<5;f++){z.a[f]=(z.a[f]<<1)|a[f];z.u[f]=(z.u[f]<<1)|(a[f]^b[f]);if(x==C){z.flip[f]=a[f]^b[f];z.center[f]=a[f];}}
  }
  z.want[0]=z.center[0]^s[2][C]^s[2][C+sign]^g[C]^g[C+sign];
  z.want[1]=d[0][C]^d[2][C]^g[C];
 }
 return out;
}
void evaluate(const vector<Data>& data,int rule,int m,int sign,int q,const vector<int>& order,ostream& out){
 int n=order.size();vector<uint64_t> ev;ev.reserve(N*(n+2)+1);
 for(int w=0;w<N;w++){
  auto& z=data[w];for(int p=0;p<n;p++){
   int f=order[p],v=z.flip[f];ev.push_back((uint64_t(patch(z.a,order,p))<<32)|payload(w,p,false,v,z.source,v));
   if(f==0||f==1){int r=z.want[f],c=r^((rule&1)&&(f==1));ev.push_back((uint64_t(patch(z.u,order,p))<<32)|payload(w,p,true,r,0,c));}
  }
 }
 ev.push_back(ZERO);sort(ev.begin(),ev.end());
 array<bool,5> pass;pass.fill(true);array<array<uint32_t,3>,5> witness{};
 int nk=0,pk=0,overlap=0,unionk=0;
 for(size_t i=0;i<ev.size();){
  size_t j=i;uint32_t key=ev[i]>>32;array<int,5> bits{};array<array<uint32_t,2>,5> example{};bool beam=false,probe=false;
  auto add=[&](int g,int bit,uint32_t p){if(!(bits[g]&(1<<bit)))example[g][bit]=p;bits[g]|=1<<bit;};
  while(j<ev.size()&&uint32_t(ev[j]>>32)==key){uint32_t p=uint32_t(ev[j++]);if(p&ZERO){add(3,0,p);add(4,1,p);continue;}bool u=(p>>3)&1;int raw=p&1,cb=(p>>2)&1;
   if(!u){beam=true;add(0,raw,p);add(1,(p>>1)&1,p);}else probe=true;
   add(2,raw,p);add(3,cb,p);add(4,cb^int(u),p);
  }
  nk+=beam;pk+=probe;overlap+=beam&&probe;unionk+=beam||probe;
  for(int g=0;g<5;g++)if(bits[g]==3&&pass[g]){pass[g]=false;witness[g]={key,example[g][0],example[g][1]};}
  i=j;
 }
 out<<"{\"rule\":"<<rule<<",\"mask\":\""<<masks[m]<<"\",\"shift\":"<<sign<<",\"reference\":"<<q<<",\"order\":[";
 for(int p=0;p<n;p++)out<<(p?",":"")<<order[p];out<<"],\"gates\":{";
 for(int g=0;g<5;g++)out<<(g?",":"")<<'"'<<gates[g]<<"\":"<<(pass[g]?"true":"false");
 out<<"},\"witnesses\":{";bool sep=false;for(int g=0;g<5;g++)if(!pass[g]){auto w=witness[g];out<<(sep?",":"")<<'"'<<gates[g]<<"\":["<<w[0]<<','<<w[1]<<','<<w[2]<<']';sep=true;}
 out<<"},\"native_keys\":"<<nk<<",\"probe_keys\":"<<pk<<",\"overlap_keys\":"<<overlap<<",\"native_probe_union_keys\":"<<unionk<<"}\n";
}
int main(int argc,char**argv){
 if(argc!=4){cerr<<"usage: audit_dt2_holdouts RULES_CSV OUTPUT_JSONL BUDGET_SECONDS\n";return 2;}
 vector<int> rules;stringstream ss(argv[1]);string v;while(getline(ss,v,','))rules.push_back(stoi(v));ofstream out(argv[2]);if(!out)return 3;
 const auto start=chrono::steady_clock::now();double budget=stod(argv[3]);int count=0,done=0;
 for(int rule:rules){
  double elapsed=chrono::duration<double>(chrono::steady_clock::now()-start).count();if(elapsed>=budget)break;
  for(int m=0;m<4;m++)for(int sign:{-1,1})for(int q=-1;q<4;q++){
   auto data=prepare(rule,m,sign,q);int n=q<0?4:5;vector<int> order(n);for(int i=0;i<n;i++)order[i]=i;
   do{evaluate(data,rule,m,sign,q,order,out);count++;}while(next_permutation(order.begin()+1,order.end()));
  }
  done++;out.flush();cerr<<"rule "<<rule<<" complete; "<<count<<" recipes; "<<chrono::duration<double>(chrono::steady_clock::now()-start).count()<<" seconds\n";
 }
 out.close();cerr<<"completed_rules="<<done<<"/"<<rules.size()<<" cases="<<count<<"\n";return done==int(rules.size())?0:10;
}
