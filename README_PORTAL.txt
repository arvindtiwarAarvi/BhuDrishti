BhuDrishti Portal — How to run
================================

1) Copy this whole BhuDrishti_Portal folder content into:
   C:\Users\HP\BhuDrishti\

   Important: app.py and pages/ should sit NEXT TO your existing modules:
   extract.py, geo_utils.py, map_overlay.py, fertility_water.py,
   ai_report.py, blockchain_module.py

2) Folder should look like:
   BhuDrishti\
     app.py
     aasia.py
     extract.py
     geo_utils.py
     ...
     pages\
       1_Lekhpal.py
       2_Farmers.py
       ...

3) Run:
   cd C:\Users\HP\BhuDrishti
   venv\Scripts\activate
   streamlit run app.py

4) Open browser: http://localhost:8501

Pages:
- Home (app.py)
- Lekhpal, Farmers, Real Estate, Citizen
- Gov Officer, Feedback, Related Portals
- About Team, Database, Dashboard

AASIA button on each page summarizes that page.
