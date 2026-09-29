from pathlib import Path
p=Path('frontend/src/App.tsx'); s=p.read_text(encoding='utf-8')
s=s.replace('import React,{useState}from\'react\';','import React,{useState}from\'react\';')
s=s.replace("const side:Page[]=['Overview','AI Assistant','Standards','Compliance','Certification','Hallmarking','Laboratories','Dashboard'];", "const side:Page[]=['Overview','AI Assistant','Standards','Compliance'];")
old="function App(){const[page,setPage]=useState<Page>('Overview'),[query,setQuery]=useState(''),[asked,setAsked]=useState(false),[dark,setDark]=useState(false),[filter,setFilter]=useState('All standards'),[huid,setHuid]=useState(''),[verified,setVerified]=useState(false),[road,setRoad]=useState(1),[mobile,setMobile]=useState(false);const ask=()=>{if(query.trim()){setAsked(true);setPage('AI Assistant')}};const searchStandards=standards.filter(s=>s.join(' ').toLowerCase().includes(filter==='All standards'?'':filter.toLowerCase()));const answer=getGuidance(query);"
new="function App(){const[page,setPage]=useState<Page>('Overview'),[query,setQuery]=useState(''),[asked,setAsked]=useState(false),[turns,setTurns]=useState<Array<{question:string;guidance:ReturnType<typeof getGuidance>;createdAt:number}>>([]),[activeTurn,setActiveTurn]=useState(-1),[productForm,setProductForm]=useState({productName:'',material:'',category:'',sector:'',intendedUse:''}),[complianceSubmitted,setComplianceSubmitted]=useState(false),[dark,setDark]=useState(false),[filter,setFilter]=useState('All standards'),[huid,setHuid]=useState(''),[verified,setVerified]=useState(false),[road,setRoad]=useState(1),[mobile,setMobile]=useState(false);const submitQuestion=(value:string)=>{const question=value.trim();if(!question)return;const item={question,guidance:getGuidance(question),createdAt:Date.now()};setTurns(prev=>[item,...prev].slice(0,20));setActiveTurn(0);setQuery('');setAsked(true);setPage('AI Assistant')};const ask=()=>submitQuestion(query);const searchStandards=standards.filter(s=>s.join(' ').toLowerCase().includes(filter==='All standards'?'':filter.toLowerCase()));const answer=activeTurn>=0&&turns[activeTurn]?turns[activeTurn].guidance:getGuidance(query);const complianceAnswer=getGuidance(Object.values(productForm).filter(Boolean).join(' '));"
assert old in s, 'App state prefix not found'
s=s.replace(old,new)
s=s.replace('<div className="toplinks"><span>भारत सरकार&nbsp; | &nbsp;Government of India</span><span className="topdivider"/> <span>Bureau of Indian Standards</span></div>','')
s=s.replace('<div className="composer-note">AI answers include evidence links. Verify critical decisions with official BIS publications.</div>','')
# Recent queries become real session entries; clicking one reopens that answer.
start=s.index('<div className="side-label">RECENT CONVERSATIONS</div>')
end=s.index('<div className="side-label saved-label">',start)
recent='''<div className="side-label">RECENT CONVERSATIONS</div>{turns.length?turns.map((turn,index)=><button className={'history '+(index===activeTurn?'selected':'')} key={turn.createdAt} onClick={()=>{setActiveTurn(index);setAsked(true)}}><Clock3 size={15}/><span>{turn.question}</span></button>):<div className="history-empty">Questions you send will appear here.</div>}'''
s=s[:start]+recent+s[end:]
# Starting a new chat preserves recents but clears current selection and draft.
s=s.replace("onClick={()=>{setAsked(false);setQuery('')}}><Plus", "onClick={()=>{setAsked(false);setQuery('');setActiveTurn(-1)}}><Plus")
# Shortcut prompts submit immediately and create a real history item.
s=s.replace("onClick={()=>{setQuery(x);setAsked(true)}}>{x}<ArrowUpRight", "onClick={()=>submitQuestion(x)}>{x}<ArrowUpRight")
s=s.replace("onClick={()=>{setQuery(x);setAsked(true);setPage('AI Assistant')}}>{x} <ArrowUpRight", "onClick={()=>submitQuestion(x)}>{x} <ArrowUpRight")
# Render the selected question, not whatever is being typed into the next one.
s=s.replace('<div className="user-question">{query}</div>', '<div className="user-question">{turns[activeTurn]?.question||query}</div>')
# Reopening a history item should show its saved guidance and evidence.
# The active answer is already derived from turns[activeTurn].
# Compliance form values now all feed its own recommendation matching.
s=s.replace('<input placeholder="e.g. Electric rice cooker" onChange={e=>setQuery(e.target.value)}/>', '<input placeholder="e.g. Electric rice cooker" value={productForm.productName} onChange={e=>setProductForm({...productForm,productName:e.target.value})}/>')
s=s.replace('<label>Material<input placeholder="e.g. Stainless steel"/></label>', '<label>Material<input placeholder="e.g. Stainless steel" value={productForm.material} onChange={e=>setProductForm({...productForm,material:e.target.value})}/></label>')
s=s.replace('<label>Product category<select><option>Select a category</option><option>Electrical appliances</option><option>Food & agriculture</option><option>Consumer products</option><option>Metals & materials</option></select></label>', '<label>Product category<select value={productForm.category} onChange={e=>setProductForm({...productForm,category:e.target.value})}><option value="">Select a category</option><option>Pressure cookers</option><option>Two-wheeler helmets</option><option>Toys</option><option>Water bottles</option><option>Stainless steel utensils</option></select></label>')
s=s.replace('<label>Manufacturing sector<select><option>Select a sector</option><option>Electronics & electrical</option><option>Engineering</option><option>Consumer goods</option></select></label>', '<label>Manufacturing sector<select value={productForm.sector} onChange={e=>setProductForm({...productForm,sector:e.target.value})}><option value="">Select a sector</option><option>Electronics & electrical</option><option>Engineering</option><option>Consumer goods</option></select></label>')
s=s.replace('<label>Intended use<input placeholder="e.g. Domestic household use"/></label>', '<label>Intended use<input placeholder="e.g. Domestic household use" value={productForm.intendedUse} onChange={e=>setProductForm({...productForm,intendedUse:e.target.value})}/></label>')
s=s.replace('onClick={()=>setAsked(true)}>Find applicable standards', 'onClick={()=>setComplianceSubmitted(true)}>Find applicable standards')
s=s.replace('{asked&&answer.evidence.length?<><div className="risk">', '{complianceSubmitted&&complianceAnswer.evidence.length?<><div className="risk">')
# Only in compliance detail, scope between the form and certification route.
a=s.index(":page==='Compliance'?"); b=s.index(":page==='Certification'?",a)
seg=s[a:b].replace('answer.evidence','complianceAnswer.evidence').replace('answer.standard','complianceAnswer.standard').replace('answer.category','complianceAnswer.category').replace('answer.clause','complianceAnswer.clause')
s=s[:a]+seg+s[b:]
p.write_text(s,encoding='utf-8')
