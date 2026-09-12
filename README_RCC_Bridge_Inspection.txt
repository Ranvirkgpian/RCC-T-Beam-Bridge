RCC T-BEAM BRIDGE — VISUAL INSPECTION APPLICATION
=====================================================

Tutorial-1: Vibe Coding Assignment

WHAT IT DOES
------------
This application records and summarises visual inspection observations
for a conventional RCC T-beam bridge.

Supported hierarchy:
Bridge -> Span -> Component -> Location -> Observation

MAIN FEATURES
-------------
1. Bridge ID, inspector, date and site/weather information
2. Structural component selection
3. Span/chainage and exact location entry
4. Defect selection
5. Condition/severity classification:
   Good -> Minor -> Moderate -> Severe
6. Condition score:
   Good=1, Minor=2, Moderate=3, Severe=4
7. Automatic priority:
   Good=NONE, Minor=ROUTINE, Moderate=HIGH, Severe=URGENT
8. Remarks/observations
9. Optional inspection photograph selection
10. Multiple observations
11. Delete/clear observations
12. CSV export
13. Automatic inspection summary
14. Component prioritisation and recommendation for detailed investigation

HOW TO RUN
-----------
Requirements:
- Python 3.x
- Tkinter (normally included with standard Python)

Run:
    python rcc_bridge_inspection.py

No external Python packages are required.

DEMO OBSERVATIONS
-----------------
Try entering:
1. Span S1 | Deck Slab | Near midspan | Cracking | Minor
2. Span S2 | Longitudinal T-Beam Girder | Bottom flange | Spalling | Moderate
3. Span S3 | Pier Cap | Bearing zone | Corrosion Staining | Moderate
4. Span S2 | Expansion Joint | Joint at roadway | Expansion Joint Damage | Severe
5. Span S1 | Kerb / Parapet | East side | No Significant Defect | Good

SUBMISSION MATERIAL
-------------------
Submit:
- rcc_bridge_inspection.py
- Screenshot of the running application
- Important prompts used during Vibe Coding
- Short note describing the basic idea, improvements and future feature

IMPORTANT ENGINEERING NOTE
--------------------------
The application is intended for visual inspection and condition
documentation. It must not be interpreted as establishing structural
safety solely from visual observations. Severe observations trigger a
recommendation for detailed investigation rather than a safety verdict.
