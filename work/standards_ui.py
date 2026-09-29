from pathlib import Path
p=Path('frontend/src/App.tsx');s=p.read_text(encoding='utf-8')
s=s.replace('IS 302 (Part 1):2024','IS 2347:2023 · IS 4151:2015 · IS 9873')
s=s.replace("onClick={()=>alert(`${s[0]}\\n\\n${s[1]}\\n\\nSample data for demonstration. Refer to BIS for official scope and clauses.`)}", "onClick={()=>{setQuery(`${s[1]} ${s[2]}`);setAsked(true);setPage('AI Assistant')}}")
p.write_text(s,encoding='utf-8')
