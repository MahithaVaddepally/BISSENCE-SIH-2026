from pathlib import Path
s=Path('frontend/src/App.tsx').read_text(encoding='utf8')
for t in ['IS 302','steel bottles','IS 2347:2023']:
 print(t,[repr(s[max(0,i-20):i+80]) for i in [s.find(t)] if i>=0])
print('replacement char',s.count('\ufffd'),'replacement byte-ish',s.count('\ufffd'))
