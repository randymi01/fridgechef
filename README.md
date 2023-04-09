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

## Local build setup guide
1. Pull repo, make and activate a python env, run the following commands in your terminal
> pip install -r requirements.txt
>
> python -m spacy download en_core_web_sm
2. Get a [Spoonacular](https://spoonacular.com/food-api) authentication key, and a [Twilio](https://www.twilio.com/) SID, authentication key, and number. Make a secret.py file in the working directory and put the following in:
> TWILIO_SID = "YOUR SID HERE"
>
> TWILIO_AUTH = "YOUR AUTH KEY HERE"
>
> SPOON_AUTH = "YOUR AUTH KEY HERE"
>
> 
> twilio_number = 'YOUR TWILIO PHONE NUMBER HERE' (need a twilio account)
>
> my_phone_number = 'YOUR PERSONAL PHONE NUMBER HERE'
3. Run main.py in the virtual env with "python main.py". At this point, you should receive a text message to your phone number from the twilio number.
4. In a new terminal, install [ngrok](https://ngrok.com/) and run the following command to your computer (I use wsl, might be different for different os)
> ngrok http 8000
5. Running the command should generate a url which is a tunnel to your computer. Copy this url, then go to the Twilio website, log in, and edit the twilio number you used. Replace the webhook "HTTP POST" url with the ngrok url generated, followed by "/sms". You should now be able to text back the Twilio number and interact with the program.