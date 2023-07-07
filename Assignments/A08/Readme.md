##  A08 practicing fast api using covid data. We are to build an api and test the endpoints.

|   #   | Folder Link | Assignment Description |
| :---: | ----------- | ---------------------- |
|   1   |     [Main](Main.py)     | Python program to create the API                       |
|   2   |     [Data](Data.csv)     | Covid data we will call with the API                                     |


Requirement:
fastapi
uvicorn
csv
datetime

Report:
Implementation was a bit weird. Initially port 8080 was in the code but for some reason it was being a pain so I changed it to 8000 and it works for some reason.

It took me hours to realize that I did not have to constantly keep putting in my user variables every time I tested and reloaded my API. I could just copy the url call and use that to automatically put in my user inputs which made testing so much easier.

Been a while since I did user error checking and I think I managed to pull off a decent sequence, albeit beyond the naive approach asked for in the requirements.

I prefer the query route with optional variables I think it makes the urls visually pleasing.