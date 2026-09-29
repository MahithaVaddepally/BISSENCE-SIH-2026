from pathlib import Path
p=Path('frontend/src/App.tsx');s=p.read_text(encoding='utf-8')
s=s.replace('IS 302 (Part 1)','IS 2347:2023')
s=s.replace("Standards for steel bottles","Standards for pressure cookers")
s=s.replace("BIS certification for LED bulbs","BIS standards for toy safety")
s=s.replace("Understanding IS 302","Helmet requirements for two-wheeler riders")
s=s.replace("'Explain IS 302 in simple English'","'Explain IS 9873 for a non-electric toy'")
s=s.replace("['Standards for LED bulbs','How does BIS certification work?','Find a testing lab']","['Which standard applies to a pressure cooker?','What steel is allowed for a water bottle?','How do toy standards differ?']")
p.write_text(s,encoding='utf-8')
