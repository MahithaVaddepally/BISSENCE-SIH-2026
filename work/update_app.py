from pathlib import Path
import re
p=Path('frontend/src/App.tsx'); s=p.read_text(encoding='utf-8')
s=s.replace("import React,{useState}from'react';", "import React,{useState}from'react';import{getGuidance}from'./knowledge';")
s=s.replace("const searchStandards=standards.filter(s=>s.join(' ').toLowerCase().includes(filter==='All standards'?'':filter.toLowerCase()));", "const searchStandards=standards.filter(s=>s.join(' ').toLowerCase().includes(filter==='All standards'?'':filter.toLowerCase()));const answer=getGuidance(query);")
arr="const standards=[['IS 2347:2023','Domestic Pressure Cooker — Specification','Pressure cookers','2023','Compulsory'],['IS 4151:2015','Protective Helmets for Two Wheeler Riders — Specification','Two-wheeler helmets','2015','Compulsory'],['IS 9873 series','Safety of Toys — Product Manuals','Toys','2023','Compulsory'],['IS 17803:2022','Potable Water Bottles (Metallic)','Water bottles','2025','Compulsory'],['IS 14756:2022','Stainless Steel Utensils — Specification','Utensils','2024','Compulsory'],['Toys QCO','Toy safety certification framework','Toys','2024','Compulsory'],['Domestic Pressure Cooker QCO','Quality Control Order','Pressure cookers','2020','Compulsory'],['Helmet QCO','Two-Wheeler Helmet Quality Control Order','Two-wheeler helmets','2020','Compulsory']];"
s=re.sub(r'const standards=\[.*?\];',arr,s,count=1)
a=s.index('<div className="answer"><div className="user-question">'); b=s.index('<div className="composer">',a)
answer="""<div className="answer"><div className="user-question">{query}</div><div className="answer-title"><div className="assistant-mark small"><Sparkles size={15}/></div><b>{answer.evidence.length?'Evidence-matched BIS guidance':'No matching source found'}</b></div><h3>Answer</h3><p>{answer.answer}</p><div className="answer-detail"><span>APPLICABLE STANDARD</span><b>{answer.standard}</b><span>RELEVANT CLAUSE / SOURCE LOCATION</span><b>{answer.clause}</b><span>WHY IT APPLIES</span><p>{answer.why}</p></div>{answer.evidence.map((item,i)=><div className="source-inline" key={item.standard}><ShieldCheck size={15}/><div><b>{item.standard} · {item.title}</b><small>{item.clause} · {i===0?'Primary source':'Related BIS source'}</small></div><a href={item.url} target="_blank" rel="noreferrer">BIS source ↗</a></div>)}<p className="disclaimer">Prototype guidance, grounded in the cited manual. Standards and QCOs can be amended; confirm the latest BIS publication before production or certification decisions.</p></div>}"""
s=s[:a]+answer+s[b:]
a=s.index("{asked?<><div className=\"evidence-card\">")
b=s.index("</>:<div className=\"evidence-empty\">",a)
evidence="""{asked&&answer.evidence.length?answer.evidence.map((item,i)=><div className="evidence-card" key={item.standard}><div className="evidence-tag"><ShieldCheck size={13}/> BIS SOURCE</div><h4>{item.standard}</h4><p>{item.title}</p><div className="clause">SOURCE LOCATION <b>{item.clause}</b></div><div className="relevance"><span>DOCUMENT MATCH</span><b>{i===0?'Primary':'Related'}</b></div><a className="evidence-link" href={item.url} target="_blank" rel="noreferrer">Open source document ↗</a></div>):''}"""
s=s[:a]+evidence+s[b:]
s=s.replace("{asked?'02':'—'}","{asked?String(answer.evidence.length).padStart(2,'0'):'—'}")
s=s.replace("SAMPLE DATASET · 30 RECORDS","BIS SOURCE DATA · 5 PRODUCTS").replace("USER DATASET · 3 CATEGORIES","BIS SOURCE DATA · 5 PRODUCTS")
s=s.replace("Showing {searchStandards.length} of 30 sample standards","Showing {searchStandards.length} BIS source records")
s=s.replace("SAMPLE DIRECTORY · 5 EXAMPLES","SAMPLE DIRECTORY · DEMO RECORDS")
p.write_text(s,encoding='utf-8')
