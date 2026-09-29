from pathlib import Path
p=Path('frontend/src/App.tsx'); s=p.read_text(encoding='utf-8')
a=s.index('</div>{asked&&answer.evidence.length?')
b=s.index('<div className="evidence-footer">',a)
part='''</div>{asked&&answer.evidence.length?answer.evidence.map((item,i)=><div className="evidence-card" key={item.standard}><div className="evidence-tag"><ShieldCheck size={13}/> BIS SOURCE</div><h4>{item.standard}</h4><p>{item.title}</p><div className="clause">SOURCE LOCATION <b>{item.clause}</b></div><div className="relevance"><span>DOCUMENT MATCH</span><b>{i===0?'Primary':'Related'}</b></div><a className="evidence-link" href={item.url} target="_blank" rel="noreferrer">Open source document ↗</a></div>):<div className="evidence-empty"><FileText size={23}/><b>Evidence appears here</b><span>Ask a question to see matched BIS references and supporting material.</span></div>}'''
s=s[:a]+part+s[b:]
p.write_text(s,encoding='utf-8')
