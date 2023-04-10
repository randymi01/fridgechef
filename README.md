# fridgechef

A conversational text bot that finds recipes for you based on the ingredients in your fridge.
Filters its recipes based on your dietary restrictions and your cuisine preferences.
Capstone project for EECS 449 Conversational AI Winter 2023 at the University of Michigan.
Created by aashil@umich.edu, alexzvk@umich.edu, cohenga@umich.edu, jayhass@umich.edu, kylewilk@umich.edu, liamt@umich.edu, randymi@umich.edu, and zhukevin@umich.edu


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