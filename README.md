# fridgechef

make a python env and download packages from requirements.txt using

> pip install -r requirements.txt

ToDo (soft deadline this Sunday):
1. Twilio Front End Integration - Aashil, and anyone else as needed
2. Dietary Restriction Entity Extraction - DONE
3. Cuisine Preference Entity Extraction - Kevin - DONE
4. Query Recipies - Alex & Kyle - DONE
5. Put entity extraction in chatbot - Alex - DONE
6. Spacy import error for Food Extractor (OSError: [E050] Can't find model 'en_core_web_sm'. It doesn't seem to be a Python package or 7 valid path to a data directory.) - SOLVED: Update spacy and run command "python -m spacy download en_core_web_sm"
8. ZeroDivisionError when receipes_to_get is empty. Should throw custom error - SOLVED: Commented out for debugging but will be reenabled for final build. Also, recommender should now always return at least one recipe
9. Remove print statements


Reach goals
1. Parameter for if you can run to grocery store
2. Integrate all different allergies questions, query includes all parameters - Kevin, Alex
3. MongoDB save dietary restrictions
4. Improve food entity extractor - Randy, Liam
5. Improve recommender - Kyle, Jacob, Liam, Randy