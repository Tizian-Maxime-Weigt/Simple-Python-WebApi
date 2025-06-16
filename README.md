# Simple-Python-WebApi

Python3 WebAPI for AI and some other use cases.

## Overview

This project provides a simple web API using Flask, offering endpoints for web search functionalities (powered by DuckDuckGo) and designed to be easily extensible for other use cases.

---

## Getting Started

### Prerequisites

- Python 3.8+
- pip

### Installation

```bash
git clone https://github.com/Tizian-Maxime-Weigt/Simple-Python-WebApi.git
cd Simple-Python-WebApi
pip install -r requirements.txt
```

### Running the API

```bash
cd api
python index.py
```

By default, the server will run on `http://0.0.0.0:5000/`.

---

## API Endpoints

### 1. `/suche`

Search the web using DuckDuckGo and return the top results.

- **Endpoint:** `/suche`
- **Method:** `GET`
- **Query Parameters:**
  - `q` (string, required): Search keywords.
  - `max_res` (integer, required): Maximum number of results to return.

#### Example Request

```http
GET /suche?q=Python%20WebAPI&max_res=3 HTTP/1.1
Host: localhost:5000
```

#### Example cURL

```sh
curl "http://localhost:5000/suche?q=Python%20WebAPI&max_res=3"
```

#### Example Response

```json
{
  "Web-API-v1.1": [
    {
      "title": "Python Web API Guide",
      "description": "A guide to building web APIs with Python.",
      "link": "https://example.com/python-web-api"
    },
    {
      "title": "Flask Documentation",
      "description": "Official Flask documentation.",
      "link": "https://flask.palletsprojects.com/"
    },
    {
      "title": "DuckDuckGo Search",
      "description": "Search results from DuckDuckGo.",
      "link": "https://duckduckgo.com/"
    }
  ]
}
```

---

## Error Handling

- If required parameters are missing or invalid, the API will return a 500 error.
- Make sure to always provide both the `q` and `max_res` parameters.

---

## Extending the API

You can easily add more endpoints and functionality by editing `api/index.py` and following the Flask conventions.

---

## License

[MIT](LICENSE)

---

## Author

[Tizian-Maxime-Weigt](https://github.com/Tizian-Maxime-Weigt)

---

**Feel free to modify this template as you add more endpoints or functionality!**
