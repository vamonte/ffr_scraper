# ffr_scraper
Python3 scraper to extract the french rugby clubs from the official FFR website.


### How to:

```shell
#To install depedencies
pip3 -r requirements.txt

#To run the scraper
python3 main.py
```

### Data structure:
```json
{
    "<id_committee>": {
        "tel.": "<string>",
        "email": "<string>",
        "fax.": "<string>",
        "adresse": "<string>",
        "name":   "<string>",
        "site web":  "<string>",
        "code postal":  "<string>",
        "ville":  "<string>",
        "clubs": {
            "<id_club>": {
              "fax.": "",
              "site web": "<string>",
              "tel.": "<string>",
              "couleur": "<string>",
              "nom": "<string>",
              "email": "<string>",
              "code postal": "<string>",
              "ville": "<string>",
              "president": "<string>",
              "adresse": "<string>",
              }
         }
    }
}


```
