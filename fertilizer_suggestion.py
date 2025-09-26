import json
from pathlib import Path
#loading ideal values(actual requirement of nutrients to get a proper yeild for a given crop) from json dataset.
DATA_FILE = Path("data/fertilizer_dataset.json")
with open(DATA_FILE,'r') as f:
    IDEAL_NPK = json.load(f)

#logic to suggest fertilizer
def suggest_fertilizer(crop,N,P,K):
    crop = crop.lower()
    if not crop in IDEAL_NPK:
        return f"No fertilizer data available for '{crop}'"
    ideal= IDEAL_NPK[crop]
    diff ={
        "N": N-ideal["N"],
        "P": N-ideal["P"],
        "K": N-ideal["K"]
    }

    key , value = max(diff.items(),key=lambda x: abs(x[1]))
    if value == 0:
        return f"Nutrient levels look good for {crop}"
    status = "high" if value> 0 else "low"

    if key=='N':
        nutrint = "Nitrogen"
        recommendation = "Apply Urea" if  status =='low' else "Reduce Urea"
    if key=='P':
        nutrint = "Phosphorous"
        recommendation = "Apply DAP" if  status =='low' else "Reduce DAP"
    else:
        nutrint = "Pottasium"
        recommendation = "Apply MOP" if  status =='low' else "Reduce MOP"
    
    return f"{nutrint} is {status} for {crop}. {recommendation}"




