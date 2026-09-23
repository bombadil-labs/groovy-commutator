// Persistent JSON-lines bridge. Protocol stdout is separate from engine logs.
import SWIPL from 'swipl-wasm';
import fs from 'node:fs';
import readline from 'node:readline';

const engine = await SWIPL({arguments:['-q'],
  print: x => process.stderr.write(`${x}\n`),
  printErr: x => process.stderr.write(`${x}\n`)});
engine.FS.writeFile('/grammar.pl', fs.readFileSync(new URL('./grammar.pl', import.meta.url)));
engine.prolog.query("consult('/grammar.pl').").once();
const ints = x => {
  if (!Array.isArray(x)) throw new Error('expected list');
  return '[' + x.map(v => Array.isArray(v) ? ints(v) :
    Number.isSafeInteger(v) && v >= 0 ? String(v) : (()=>{throw new Error('expected nonnegative integer');})()).join(',') + ']';
};
const query = goal => {
  const answer = engine.prolog.query(goal).once();
  if (!answer?.success) throw new Error(`failed goal: ${goal.slice(0,160)}`);
  return answer;
};
console.log(JSON.stringify({ready:true, version:query('current_prolog_flag(version,V).').V}));
for await (const line of readline.createInterface({input:process.stdin})) {
  try {
    const r=JSON.parse(line);
    let result;
    switch (r.op) {
      case 'generate': result=query(`encoders(${ints(r.target)},Ps).`).Ps; break;
      case 'install': result=query(`install(${ints(r.rows)}).`).success; break;
      case 'next': {
        const mode=r.guided ? 'guided' : 'scan';
        if (![1,8].includes(r.limit)) throw new Error('invalid batch size');
        result=query(`batch(${mode},${r.limit},Is).`).Is; break;
      }
      case 'mark': result=query(`mark(${ints([r.index]).slice(1,-1)}).`).success; break;
      case 'witness': result=query(`add_witness(${ints([r.id]).slice(1,-1)},${ints(r.a)},${ints(r.b)}).`).success; break;
      case 'stats': {
        const s=query('stats(V,C,R).'); result={candidate_visits:s.V,witness_comparisons:s.C,rejections:s.R}; break;
      }
      case 'close': console.log(JSON.stringify({ok:true,result:true})); process.exit(0);
      default: throw new Error('unknown operation');
    }
    console.log(JSON.stringify({ok:true,result}));
  } catch (e) {
    console.log(JSON.stringify({ok:false,error:String(e)}));
  }
}
process.exit(0);
