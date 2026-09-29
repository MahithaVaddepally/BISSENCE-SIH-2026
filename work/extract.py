from pathlib import Path
from pypdf import PdfReader
root=Path(r'C:\Users\USER\OneDrive\Desktop\pressure cookers')
out=Path('work/pdf_extracts.txt')
with out.open('w',encoding='utf8') as f:
 for p in sorted(root.rglob('*.pdf')):
  f.write('\n\n'+'='*100+'\n'+str(p)+'\n'+'='*100+'\n')
  try:
   reader=PdfReader(str(p))
   for i,page in enumerate(reader.pages):
    f.write(f'\n--- PAGE {i+1} ---\n')
    f.write(page.extract_text() or '')
  except Exception as e:f.write('ERROR '+str(e))
print(out, out.stat().st_size)
