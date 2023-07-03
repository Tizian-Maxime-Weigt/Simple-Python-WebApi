# duckduckgo-api

## Self host
#Docker

```
docker run -p 8000:8000 tizi-development\duckduckgo-api
```
#Host self or Deploy by Github
```bash
git clone https://github.com/binjie09/duckduckgo-api.git
cd duckduckgo-api
python3 -m venv myenv && source myenv/bin/activate && pip install -r requirements.txt
gunicorn -b 0.0.0.0:8000 app:app
```
