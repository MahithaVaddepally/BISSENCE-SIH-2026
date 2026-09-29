from pathlib import Path
s=Path('frontend/src/App.tsx').read_text(encoding='utf-8')
for term in ['IS 302','steel bottles','Pressure Cooker QCO']:
 print('\nTERM',term)
 start=0
 while True:
  i=s.find(term,start)
  if i<0: break
  print(s[max(0,i-90):i+140])
  start=i+1

