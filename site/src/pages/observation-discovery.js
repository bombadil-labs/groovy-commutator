import data from '../../../results/observation_discovery_20260923.json';
import './observation-discovery.css';
const $ = id => document.getElementById(id);
let showWinner = false;
function currentCase() { return data.cases[Number($('case').value)]; }
function selected(mask) { return data.grammar.filter(f => (mask & (1 << f.id)) !== 0); }
function bit(row, id) { return (row.features >> id) & 1; }
function fillWitnesses() {
  $('witness').replaceChildren(...currentCase().arms.guided.witnesses.map((w,i) => {
    const o = document.createElement('option'); o.value = String(i);
    o.textContent = `${i+1} · ${selected(w.candidate_mask).length} added features`; return o;
  }));
  showWinner = false; render();
}
function world(row, label, fs, rule) {
  const card = document.createElement('article'); card.className = 'world';
  const title = document.createElement('h2'); title.textContent = `${label} · seed ${row.seed}`; card.append(title);
  const grid = document.createElement('div'); grid.className = 'grid';
  const header = document.createElement('span'); header.textContent = 'site'; grid.append(header);
  for (let x=-4;x<=4;x++) { const e=document.createElement('span');e.className='axis';e.textContent=String(x);grid.append(e); }
  const operands = new Set(fs.flatMap(f=>f.operands.map(op=>op.join(':'))));
  const baseSupport = rule===30 ? [-2,-1,0,1,2] : [0];
  for (const t of [-1,0]) {
    const timeLabel=document.createElement('span');timeLabel.className='time';timeLabel.textContent=t===-1?'past':'now';grid.append(timeLabel);
    for (let x=-4;x<=4;x++) {
      const cell=document.createElement('span');const exists=t===-1 || Math.abs(x)<=3;
      const value=t===-1 ? (row.seed>>(x+4))&1 : row.now[x+3];
      cell.className=`cell ${exists ? 'v'+value : 'empty'}`;
      cell.textContent=exists?String(value):'·';
      if (operands.has(`${t}:${x}`)) cell.classList.add(t===-1?'past-read':'read');
      else if(t===0 && baseSupport.includes(x)) cell.classList.add('base-read');
      cell.title=`${t===-1?'Past':'Current'} site ${x}${exists?`: ${value}`:''}`;grid.append(cell);
    }
  }
  card.append(grid);
  const output=document.createElement('p');output.className='output';output.textContent=`Next ${rule===30?'central G':'central source'} bit: ${row.target}`;card.append(output);
  const base=document.createElement('p');base.className='muted';base.textContent=`Mandatory current ${rule===30?'G':'source'} bit: ${row.base}. Dotted outlines show its raw support in the frozen acquisition recipe.`;card.append(base);
  return card;
}
function render() {
  const c=currentCase(), w=c.arms.guided.witnesses[Number($('witness').value)];
  const win=c.arms.guided.winner, mask=showWinner?win.mask:w.candidate_mask;
  const fs=selected(mask), [a,b]=w.pair.map(i=>c.rows[i]);
  const different=fs.some(f=>bit(a,f.id)!==bit(b,f.id)) || a.base!==b.base;
  $('verdict').textContent=different?'The winning view separates these two worlds.':'Same observed input. Different next output. This view cannot be sufficient.';
  $('verdict').className=different?'separated':'collision';
  $('toggle').textContent=showWinner?'Show failed view':'Show winning view';
  $('worlds').replaceChildren(world(a,'World A',fs,c.rule),world(b,'World B',fs,c.rule));
  $('features').replaceChildren(...fs.map(f=>{const e=document.createElement('span');e.className='feature '+(bit(a,f.id)!==bit(b,f.id)?'split':'');e.textContent=`${f.name} → A: ${bit(a,f.id)} / B: ${bit(b,f.id)}`;return e;}));
  if (!fs.length) $('features').textContent='Only the mandatory base bit; no added feature.';
  $('finding').textContent=c.rule===30
    ? 'Six current bits, sites −2 through +3, are optimal in this grammar. Offered XOR and history features save no bits. Witnesses reduce full checks sharply, but raw-only search is faster overall. The current G bit is redundant once these six source bits are read.'
    : 'The known side XOR needs one added feature; raw-only needs two. Both read the same raw cells. This calibration checks that the search can select a useful relation when the grammar contains one.';
  $('costs').replaceChildren(...['scan','guided','raw'].map(name=>{
    const arm=c.arms[name], k=arm.winner.costs, tr=document.createElement('tr');
    const labels={scan:'Full grammar scan',guided:'Witness-guided grammar',raw:'Raw-only scan'};
    for(const value of [labels[name],k.retained_bits_including_base,k.raw_read_count_including_base,k.past_buffer_cells,arm.full_oracle_calls,arm.total_seconds.toFixed(4)]) { const td=document.createElement('td');td.textContent=String(value);tr.append(td); }
    return tr;
  }));
}
$('case').addEventListener('change',fillWitnesses);
$('witness').addEventListener('change',render);
$('toggle').addEventListener('click',()=>{showWinner=!showWinner;render();});
fillWitnesses();
