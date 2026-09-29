from pathlib import Path
p=Path('frontend/src/App.tsx');s=p.read_text(encoding='utf-8')
s=s.replace("import React,{useState}from'react';", "import React,{useEffect,useState}from'react';")
s=s.replace("[turns,setTurns]=useState<Array<{question:string;guidance:ReturnType<typeof getGuidance>;createdAt:number}>>([])", "[turns,setTurns]=useState<Array<{question:string;guidance:ReturnType<typeof getGuidance>;createdAt:number}>>(()=>{try{return JSON.parse(localStorage.getItem('bissence-recent-questions')||'[]')}catch{return []}})")
s=s.replace("const complianceAnswer=getGuidance(Object.values(productForm).filter(Boolean).join(' '));return <div", "const complianceAnswer=getGuidance(Object.values(productForm).filter(Boolean).join(' '));useEffect(()=>{try{localStorage.setItem('bissence-recent-questions',JSON.stringify(turns))}catch{}},[turns]);return <div")
p.write_text(s,encoding='utf-8')
