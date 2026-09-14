// State-independent row-polarity experiment; old DT2 implementation is a pinned dependency.
#define main preserved_dt2_main
#include "audit_dt2_holdouts.cpp"
#undef main
using Event=uint64_t;
Event signature(Event x){return (x&0xffffffff00000000ULL)|(x&15ULL);}
void compact(vector<Event>& v){
 sort(v.begin(),v.end(),[](Event a,Event b){auto sa=signature(a),sb=signature(b);return sa==sb?a<b:sa<sb;});
 v.erase(unique(v.begin(),v.end(),[](Event a,Event b){return signature(a)==signature(b);}),v.end());
}
struct Prepared {vector<vector<Event>> native;vector<Event> probe;};
Prepared constraints(const vector<Data>& data,int rule,const vector<int>& order){
 int n=order.size();Prepared b;b.native.resize(n);
 for(int p=0;p<n;p++){
  int f=order[p];auto& v=b.native[p];
  // Native patches depend on [-4,4]; set the two unused outer bits to zero.
  for(int w=0;w<1024;w+=2){auto& z=data[w];int flip=z.flip[f];v.push_back((Event(patch(z.a,order,p))<<32)|payload(w,p,false,flip,z.source,flip));}
  compact(v);
  if(f==0||f==1)for(int w=0;w<N;w++){auto& z=data[w];int raw=z.want[f],cb=raw^((rule&1)&&(f==1));b.probe.push_back((Event(patch(z.u,order,p))<<32)|payload(w,p,true,raw,0,cb));}
 }
 compact(b.probe);return b;
}
void polarity_case(const Prepared& b,int rule,int m,int sign,int q,const vector<int>& order,int polarity,ostream& out){
 int n=order.size();vector<Event> ev=b.probe;ev.reserve(ev.size()+N*n+1);
 for(int p=0;p<n;p++){
  uint32_t shift=0;for(int dy=-2;dy<=2;dy++)shift=(shift<<5)|(((polarity>>order[(p+dy+n)%n])&1)?31:0);
  for(auto e:b.native[p])ev.push_back(e^(Event(shift)<<32));
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
 for(int p=0;p<n;p++)out<<(p?",":"")<<order[p];out<<"],\"polarity\":"<<polarity<<",\"gates\":{";
 for(int g=0;g<5;g++)out<<(g?",":"")<<'"'<<gates[g]<<"\":"<<(pass[g]?"true":"false");
 out<<"},\"witnesses\":{";bool sep=false;for(int g=0;g<5;g++)if(!pass[g]){auto w=witness[g];out<<(sep?",":"")<<'"'<<gates[g]<<"\":["<<w[0]<<','<<w[1]<<','<<w[2]<<']';sep=true;}
 out<<"},\"native_keys\":"<<nk<<",\"probe_keys\":"<<pk<<",\"overlap_keys\":"<<overlap<<",\"native_probe_union_keys\":"<<unionk<<"}\n";
}
int main(int argc,char**argv){
 if(argc!=4){cerr<<"usage: audit_row_complements RULES_CSV OUTPUT_JSONL BUDGET_SECONDS\n";return 2;}
 vector<int> rules;stringstream ss(argv[1]);string v;while(getline(ss,v,','))rules.push_back(stoi(v));ofstream out(argv[2]);if(!out)return 3;
 const auto start=chrono::steady_clock::now();double budget=stod(argv[3]);int count=0,done=0;
 for(int rule:rules){
  if(chrono::duration<double>(chrono::steady_clock::now()-start).count()>=budget)break;
  for(int m=0;m<4;m++)for(int sign:{-1,1})for(int q=-1;q<4;q++){
   auto data=prepare(rule,m,sign,q);int n=q<0?4:5;vector<int> order(n);for(int i=0;i<n;i++)order[i]=i;
   do{auto b=constraints(data,rule,order);for(int polarity=0;polarity<(1<<n);polarity++){polarity_case(b,rule,m,sign,q,order,polarity,out);count++;}}while(next_permutation(order.begin()+1,order.end()));
  }
  done++;out.flush();cerr<<"rule "<<rule<<" complete; "<<count<<" cases; "<<chrono::duration<double>(chrono::steady_clock::now()-start).count()<<" seconds\n";
 }
 out.close();cerr<<"completed_rules="<<done<<"/"<<rules.size()<<" cases="<<count<<"\n";return done==int(rules.size())?0:10;
}
