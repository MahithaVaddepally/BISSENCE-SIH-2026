# BISSENCE prototype

## Run locally

Frontend: open a terminal in `frontend`, run `npm install`, then `npm run dev`.

Backend: from the project root run `python -m pip install -r backend/requirements.txt`, then `python -m uvicorn backend.main:app --reload`. If the terminal is already inside `backend`, use `python -m pip install -r requirements.txt` and `python -m uvicorn main:app --reload`.

The FastAPI API reads `data/standards.json`, `data/labs.json`, and `data/hallmark.json`. Routes: `/standards`, `/standards/{id}`, `/chat`, `/recommend`, `/verify-huid`, `/labs`, `/stats`.

## Product knowledge dataset

`data/standards.json` contains structured product guidance and source references for pressure cookers, two-wheeler helmets and toys from the supplied PDFs, plus stainless steel utensils and metallic potable water bottles from BIS product manuals. The assistant's matching/answer rules live in `frontend/src/knowledge.ts`; answers and evidence cards vary by the query and say when no source matches.

Supplied source PDFs remain in `C:\Users\USER\OneDrive\Desktop\pressure cookers`. The app does not copy them. It includes file references and official BIS links. Exact material and test references are included only where confirmed in a product manual or BIS amendment. Helmet shell-material details are deliberately not guessed because the supplied manual points to Clause 4 of IS 4151 rather than reproducing its full requirements. Toy-material guidance is limited to what the supplied manual confirms. The BIS standards can change; verify the current publication and QCO before manufacturing or certification decisions.

The labs, HUID lookup, and analytics remain clearly labelled demonstration data, not live BIS services.
