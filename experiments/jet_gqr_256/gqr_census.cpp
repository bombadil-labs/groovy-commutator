#include <algorithm>
#include <array>
#include <chrono>
#include <cmath>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <sstream>
#include <string>
#include <vector>
using namespace std;

static constexpr int STATES=256, PAIR_NODES=65536;
int f(int rule,int l,int c,int r){return (rule >> ((l<<2)|(c<<1)|r))&1;}
int bit(int word,int at){return (word>>at)&1;}
struct GraphStats{
 int rule=0, edges=0, used_nodes=0, recurrent_components=0, diagonal_recurrent=0, mixed_recurrent=0, pure_recurrent=0;
 int branching_mixed=0, branching_pure=0, cycles_mixed=0, cycles_pure=0, max_cycle_period=0;
 int gqr_symbols=0, G_nz=0, Q_nz=0, R_nz=0, biggest_branching_size=0;
 int first_nonzero_component=-1;
};
struct Graph{
 vector<int> head, revhead, src, dest, next, revdest, revnext;
 explicit Graph(int maxedges) :head(PAIR_NODES,-1),revhead(PAIR_NODES,-1){
  src.reserve(maxedges);dest.reserve(maxedges);next.reserve(maxedges);
  revdest.reserve(maxedges);revnext.reserve(maxedges);
 }
 void add(int s,int d){int i=(int)dest.size();src.push_back(s);dest.push_back(d);next.push_back(head[s]);head[s]=i;
                      revdest.push_back(s);revnext.push_back(revhead[d]);revhead[d]=i;}
};
vector<vector<uint8_t>> local_tables(int rule){
 vector<vector<uint8_t>> levels;
 levels.emplace_back(8);
 for(int w=0;w<8;w++) levels[0][w]=bit(w,1)^f(rule,bit(w,0),bit(w,1),bit(w,2));
 for(int k=0;k<3;k++){
  int radius=k+1, windowsize=2*(radius+1)+1;
  vector<uint8_t> v(1<<windowsize);int mask=(1<<(2*radius+1))-1;
  for(int w=0;w<(1<<windowsize);w++){
   int hword=0;
   for(int pos=0;pos<2*radius+1;pos++)
    hword|=f(rule,bit(w,pos),bit(w,pos+1),bit(w,pos+2))<<pos;
   int transported=levels[k][hword];
   int a=levels[k][(w>>0)&mask],b=levels[k][(w>>1)&mask],c=levels[k][(w>>2)&mask];
   v[w]=transported ^ f(rule,a,b,c);
  }
  levels.push_back(move(v));
 }
 return levels;
}
GraphStats run(int rule){
 GraphStats stat;stat.rule=rule;
 auto levels=local_tables(rule);
 for(int k=1;k<=3;k++) for(auto b:levels[k]) (k==1?stat.G_nz:k==2?stat.Q_nz:stat.R_nz)+=b;
 array<vector<int>,8> buckets;
 array<uint8_t,8> used{};
 for(int w=0;w<512;w++){
  int label=levels[1][(w>>2)&31] | (levels[2][(w>>1)&127]<<1) | (levels[3][w]<<2);
  buckets[label].push_back(w);used[label]=1;
 }
 for(int i=0;i<8;i++) stat.gqr_symbols += used[i];
 int predicted=0;for(auto& b:buckets)predicted+=(int)b.size()*(int)b.size();
 Graph graph(predicted);
 for(auto& b:buckets){for(auto a:b)for(auto c:b){
  int s=(a&255)*256+(c&255),d=(a>>1)*256+(c>>1);
  graph.add(s,d);
 }}
 stat.edges=(int)graph.dest.size();
 vector<uint8_t> seen(PAIR_NODES,0);
 vector<int> order;order.reserve(PAIR_NODES);
 vector<pair<int,int>> stack;stack.reserve(PAIR_NODES);
 for(int root=0;root<PAIR_NODES;root++){
  if(seen[root])continue;
  seen[root]=1;stack.push_back({root,graph.head[root]});
  while(!stack.empty()){
   auto& fr=stack.back();int edge=fr.second;
   while(edge>=0 && seen[graph.dest[edge]])edge=graph.next[edge];
   if(edge<0){order.push_back(fr.first);stack.pop_back();continue;}
   fr.second=graph.next[edge];int w=graph.dest[edge];seen[w]=1;stack.push_back({w,graph.head[w]});
  }
 }
 vector<int> cid(PAIR_NODES,-1),sizes,diags;
 int ccount=0;
 for(int oi=PAIR_NODES-1;oi>=0;oi--){int root=order[oi];if(cid[root]>=0)continue;
  int size=0,diag=0;
  vector<int> pile={root};cid[root]=ccount;
  while(!pile.empty()){
   int v=pile.back();pile.pop_back();size++;diag+=(v/256==v%256);
   for(int e=graph.revhead[v];e>=0;e=graph.revnext[e]){
    int w=graph.revdest[e];if(cid[w]<0){cid[w]=ccount;pile.push_back(w);}
   }
  }
  sizes.push_back(size);diags.push_back(diag);ccount++;
 }
 vector<int> internal(ccount,0);
 for(size_t i=0;i<graph.src.size();i++) if(cid[graph.src[i]]==cid[graph.dest[i]])internal[cid[graph.src[i]]]++;
 for(int c=0;c<ccount;c++){
  int n=sizes[c], e=internal[c],diag=diags[c]; if(e==0)continue;
  if(diag==n)stat.diagonal_recurrent++;
  else if(diag==0){stat.pure_recurrent++;if(e>n){stat.branching_pure++;stat.biggest_branching_size=max(stat.biggest_branching_size,n);}else{stat.cycles_pure++;stat.max_cycle_period=max(stat.max_cycle_period,n);}}
  else{stat.mixed_recurrent++;if(e>n){stat.branching_mixed++;stat.biggest_branching_size=max(stat.biggest_branching_size,n);}else{stat.cycles_mixed++;stat.max_cycle_period=max(stat.max_cycle_period,n);}}
  stat.recurrent_components++;
 }
 return stat;
}
int main(int argc,char** argv){
 if(argc!=2){cerr<<"Usage: gqr_census output.tsv\n";return 2;}
 auto start=chrono::steady_clock::now();
 ofstream out(argv[1]);
 out<<"rule\tedges\tgqr_symbols\tG_nz\tQ_nz\tR_nz\trecurrent\tdiag\tmixed\tpure\tbranch_mixed\tbranch_pure\tcycles_mixed\tcycles_pure\tmax_cycle_period\tbiggest_branch_scc\n";
 for(int rule=0;rule<256;rule++){
  GraphStats a=run(rule);
  out<<a.rule<<'\t'<<a.edges<<'\t'<<a.gqr_symbols<<'\t'<<a.G_nz<<'\t'<<a.Q_nz<<'\t'<<a.R_nz<<'\t'
     <<a.recurrent_components<<'\t'<<a.diagonal_recurrent<<'\t'<<a.mixed_recurrent<<'\t'<<a.pure_recurrent<<'\t'
     <<a.branching_mixed<<'\t'<<a.branching_pure<<'\t'<<a.cycles_mixed<<'\t'<<a.cycles_pure<<'\t'
     <<a.max_cycle_period<<'\t'<<a.biggest_branching_size<<'\n';
  if(rule%32==31){cerr<<"completed "<<rule+1<<"/256\n";out.flush();}
 }
 out.close();
 double sec=chrono::duration<double>(chrono::steady_clock::now()-start).count();
 cout<<"COMPLETE all 256 GQR exact SCC classification in "<<sec<<" s\n";
 return 0;
}
