import json
import os
from datetime import date

MAX_SCORES=5
SCORES_PATH=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),"highscores.json")

def load_scores(path=SCORES_PATH):
    """Return the saved top scores (highest first). Missing or corrupt file -> empty list."""
    try:
        with open(path) as f:
            data=json.load(f)
    except (OSError,ValueError):
        return []
    scores=[]
    for entry in data if isinstance(data,list) else []:
        if isinstance(entry,dict) and isinstance(entry.get("score"),int):
            scores.append({"score":entry["score"],"date":str(entry.get("date",""))})
    scores.sort(key=lambda e:e["score"],reverse=True)
    return scores[:MAX_SCORES]

def add_score(score, path=SCORES_PATH):
    """Insert a score, keep the top 5, save. Returns (scores, rank) where rank is the
    0-based position of the new score in the table, or None if it didn't make it."""
    new={"score":int(score),"date":date.today().isoformat()}
    scores=load_scores(path)+[new]
    scores.sort(key=lambda e:e["score"],reverse=True)  # stable: older ties stay ahead
    scores=scores[:MAX_SCORES]
    rank=next((i for i,e in enumerate(scores) if e is new),None)
    tmp=path+".tmp"
    try:
        with open(tmp,"w") as f:
            json.dump(scores,f,indent=2)
        os.replace(tmp,path)
    except OSError:
        pass  # can't save (read-only dir etc.) -> still show the table for this session
    return scores,rank
