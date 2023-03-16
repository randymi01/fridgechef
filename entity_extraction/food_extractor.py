from transformers import AutoTokenizer, AutoModelForTokenClassification
from transformers import pipeline
import json
import os
from pathlib import Path

tokenizer = AutoTokenizer.from_pretrained("harr/distilbert-base-uncased-finetuned-ingredients")

model = AutoModelForTokenClassification.from_pretrained("harr/distilbert-base-uncased-finetuned-ingredients")

classifier = pipeline('token-classification', model=model, tokenizer=tokenizer, aggregation_strategy = "simple")

# return list of food items
# turn debug to false to stop recording extractions
def food_extractor(text: str, debug = True):
    output = classifier(text)
    if debug:

        # need to do some funky pathing stuff since module is being imported by main, but
        # we use relative paths here
        current_directory = os.getcwd()
        os.chdir(Path(__file__).parent)
        record_num = len([name for name in os.listdir('records') if os.path.isfile(name)])
        file_name = f'records/food_extraction_log_{str(record_num)}.json'
        with open(file_name, 'w') as f:
            f.write(str(output))
        
        os.chdir(current_directory)
    return [i["word"] for i in output]
        



