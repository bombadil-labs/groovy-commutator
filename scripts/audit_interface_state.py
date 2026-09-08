"""Independent packed truth-set encoders, mux update, and validity audit."""
from pathlib import Path
import hashlib,json,time,zlib
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
STEM=ROOT/'results/interface_state_20260908'
FULL=np.uint64(2**64-1)


def advance(g):
    left,center,right=g[1:-1,:-2],g[1:-1,1:-1],g[1:-1,2:]
    west=~(left|right);middle=left^right;east=left&right
    above=(west&g[:-2,:-2])|(middle&g[:-2,1:-1])|(east&g[:-2,2:])
    below=(west&g[2:,:-2])|(middle&g[2:,1:-1])|(east&g[2:,2:])
    return (~center&above)|(center&below)


def generate(mode,ticks):
    nbits=18 if mode=='free' else 2*(ticks+1)
    numbers=np.arange(1<<nbits,dtype=np.uint64)
    variables=[]
    for bit in range(nbits):
        raw=np.packbits(((numbers>>bit)&1).astype(np.uint8),bitorder='little')
        variables.append(np.frombuffer(raw.tobytes(),dtype='<u8'))
    ys=list(range(-2*ticks,4+2*ticks));xs=list(range(-ticks,2+ticks))
    g=np.empty((len(ys),len(xs),len(numbers)//64),dtype=np.uint64)
    for iy,y in enumerate(ys):
        for ix,x in enumerate(xs):
            g[iy,ix]=FULL if x%2 else 0
            block=(x+ticks)//2
            if mode=='free':
                # Direct coordinate -> truth-variable map, independent of the primary encoder.
                address={(0,1):0,(1,0):1,(1,1):2,(2,0):3,(2,1):4,(3,0):5}.get((y,x%2))
                if address is not None:g[iy,ix]=variables[6*block+address]
            else:
                if y==0 and x%2:g[iy,ix]=~variables[2*block]
                if y==1 and not x%2:g[iy,ix]=variables[2*block]
                if y==2 and x%2:g[iy,ix]=~variables[2*block+1]
                if y==3 and not x%2:g[iy,ix]=variables[2*block+1]
    for _ in range(ticks):g=advance(g)
    words=np.zeros(len(numbers),dtype=np.uint64)
    for j,cell in enumerate(g.reshape(-1,len(numbers)//64)):
        unpacked=np.unpackbits(np.frombuffer(cell.astype('<u8').tobytes(),dtype=np.uint8),bitorder='little')
        words|=unpacked.astype(np.uint64)<<np.uint64(j)
    return words


def verify(record,words):
    rows=list(range(-record['ticks'],4+record['ticks']))
    expected_free={(0,1),(1,0),(1,1),(2,0),(2,1),(3,0)}
    violations=np.zeros(len(words),dtype=np.uint64)
    exterior=np.zeros(len(words),dtype=bool)
    affected=[];counts={}
    for iy,y in enumerate(rows):
        for x in [0,1]:
            j=2*iy+x
            change=(((words>>np.uint64(j))&1)!=x)
            if change.any():affected.append(y)
            if (y,x) not in expected_free:
                violations|=change.astype(np.uint64)<<np.uint64(j)
                counts[(y,x)]=int(change.sum())
            if y<0 or y>3:exterior|=change
    assert record['inputs']==len(words)
    assert record['valid_inputs']==int((violations==0).sum())
    assert record['exterior_changed_inputs']==int(exterior.sum())
    assert record['affected_row_bounds']==([min(affected),max(affected)] if affected else None)
    assert record['output_rows']==rows
    assert record['output_sha256']==hashlib.sha256(words.astype('<u8').tobytes()).hexdigest()
    def verify_witness(w,q):
        assert w['input_index']==q and w['output_word']==int(words[q])
        assert w['input_bits']==[(q>>j)&1 for j in range(len(w['input_bits']))]
        assert w['output']==[[(int(words[q])>>(2*i+x))&1 for x in [0,1]] for i in range(len(rows))]
        assert w['failed_cells']==[[y,x] for i,y in enumerate(rows) for x in [0,1] if int(violations[q])&(1<<(2*i+x))]
    bad=np.flatnonzero(violations)
    if len(bad):verify_witness(record['first_failure'],int(bad[0]))
    else:assert record['first_failure'] is None
    assert len(record['fixed_cell_violations'])==len(counts)
    for c in record['fixed_cell_violations']:
        assert c['count']==counts[(c['y'],c['x'])]
        if c['count']:
            bit=2*(c['y']+record['ticks'])+c['x']
            first=int(np.flatnonzero((violations>>np.uint64(bit))&1)[0])
            verify_witness(c['first_witness'],first)
        else:assert c['first_witness'] is None


def main():
    start=time.time();data=json.loads(Path(str(STEM)+'_census.json').read_text());total=0
    for record in data['censuses']:
        mode,ticks=record['mode'],record['ticks'];words=generate(mode,ticks)
        verify(record,words)
        cache=Path('/tmp/interface_state_'+mode+'_'+str(ticks)+'.npy')
        if cache.exists():assert np.array_equal(words,np.load(cache))
        if mode=='free':
            saved=json.loads(Path(str(STEM)+'_free_outputs.json').read_text())
            raw=zlib.decompress(bytes.fromhex(saved['data']))
            assert raw==words.astype('<u8').tobytes()
            assert hashlib.sha256(raw).hexdigest()==saved['output_sha256']
        total+=len(words);print(mode,ticks,'all outputs and summaries match',flush=True)
    result=dict(audited_fields=total,censuses=len(data['censuses']),all_fields_counts_and_witnesses_match=True,
                seconds=round(time.time()-start,3),script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
    Path(str(STEM)+'_audit.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))


if __name__=='__main__':main()
