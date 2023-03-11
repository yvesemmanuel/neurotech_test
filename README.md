# Machine Learning Model Monitoring API

This API is designed to monitor machine learning models. It uses FastAPI as the web framework, pytest for unit tests, and autopep8 and pylint for code formatting and quality checks.

## Performance Endpoint
The Performance Endpoint is used to read the model AUC-ROC performance using the request body as input. The request body should be a JSON object containing the necessary data to perform the performance calculation.

#### Request
```bash
POST /performance
Content-Type: application/json
```

#### The request body should have the format of a list of records.
A record should have the following format:
```json
{
    "VAR2": "M",
    "IDADE": 43.893,
    "VAR5": "PR",
    "VAR6": -25.4955709,
    "VAR7": -49.2454987,
    "VAR8": "D",
    "VAR9": "E",
    "VAR10": "MEDIA",
    "VAR11": 1.0,
    "VAR12": 0.182,
    "VAR14": 0.597,
    "VAR15": 0.618,
    "VAR16": 0.25,
    "VAR18": 1.076712,
    "VAR19": 5.057534,
    "VAR22": 0.125,
    "VAR24": 0.069,
    "VAR25": 0.0969999999999999,
    "VAR32": "SALDO INEXISTENTE",
    "VAR39": 0.661039,
    "VAR40": 0.573539,
    "VAR41": 0.4793699999999999,
    "VAR42": 0.4440489999999999,
    "VAR47": 0.006,
    "VAR49": "S",
    "VAR50": "N",
    "VAR51": "N",
    "VAR52": "N",
    "VAR53": "N",
    "VAR54": "N",
    "VAR55": "N",
    "VAR56": "S",
    "VAR57": "S",
    "VAR58": "N",
    "VAR59": "N",
    "VAR60": "N",
    "VAR61": "N",
    "VAR62": "N",
    "VAR63": "N",
    "VAR64": "N",
    "VAR65": "N",
    "VAR66": "ALTISSIMA",
    "VAR67": "ALTA",
    "VAR68": "ALTISSIMA",
    "VAR69": "ALTISSIMA",
    "VAR70": "ALTISSIMA",
    "VAR71": "ALTA",
    "VAR72": "ALTISSIMA",
    "VAR73": "ALTISSIMA",
    "VAR74": "ALTISSIMA",
    "VAR75": "ALTISSIMA",
    "VAR76": "ALTA",
    "VAR77": "ALTISSIMA",
    "VAR78": "ALTISSIMA",
    "VAR79": "ALTISSIMA",
    "VAR80": "ALTA",
    "VAR81": "ALTA",
    "VAR82": "ALTISSIMA",
    "VAR83": "ALTISSIMA",
    "VAR84": "ALTA",
    "VAR85": "ALTA",
    "VAR86": "ALTA",
    "VAR87": "ALTISSIMA",
    "VAR88": "ALTA",
    "VAR89": "ALTISSIMA",
    "VAR90": "BAIXISSIMA",
    "VAR91": "ALTA",
    "VAR92": "ALTISSIMA",
    "VAR93": "ALTISSIMA",
    "VAR94": "ALTISSIMA",
    "VAR95": "ALTA",
    "VAR96": "ALTISSIMA",
    "VAR97": "ALTA",
    "VAR98": "ALTISSIMA",
    "VAR99": "ALTISSIMA",
    "VAR100": "BAIXISSIMA",
    "VAR101": "ALTA",
    "VAR102": "MEDIO",
    "VAR103": "MEDIO",
    "VAR104": "PROXIMO",
    "VAR105": "LONGE",
    "VAR106": "MEDIO",
    "VAR107": "MEDIO",
    "VAR108": "MEDIO",
    "VAR109": "MEDIO",
    "VAR110": "PROXIMO",
    "VAR111": "MEDIO",
    "VAR112": "MEDIO",
    "VAR113": "PROXIMO",
    "VAR114": "PROXIMO",
    "VAR115": "MEDIO",
    "VAR116": "LONGE",
    "VAR117": "MEDIO",
    "VAR118": "MEDIO",
    "VAR119": "LONGE",
    "VAR120": "MUITO LONGE",
    "VAR121": "MEDIO",
    "VAR122": "MEDIO",
    "VAR123": "MEDIO",
    "VAR124": "MEDIO",
    "VAR125": "PROXIMO",
    "VAR126": "MEDIO",
    "VAR127": "PROXIMO",
    "VAR128": "LONGE",
    "VAR129": "MEDIO",
    "VAR130": "MEDIO",
    "VAR131": "MEDIO",
    "VAR132": "PROXIMO",
    "VAR133": "MEDIO",
    "VAR134": "PROXIMO",
    "VAR135": "MEDIO",
    "VAR136": "MEDIO",
    "VAR137": "MEDIO",
    "VAR138": "MEDIO",
    "VAR139": "MEDIO",
    "VAR140": "MUITO PROXIMO",
    "VAR141": 3970.113648,
    "VAR142": "C",
    "REF_DATE": "2017-03-25 00:00:00+00:00",
    "TARGET": 1
}
```

#### Response
If the request is successful, the API will return a JSON response object containing the volumetry by month and the AUC-ROC value:

```json
{
  "volumetry": {
    "2022-02": 1000,
    "2022-03": 2000,
    "2022-04": 1500
  },
  "auc_roc": 0.8
}
```

#### Erros handling
If the request body is not a valid JSON object or the body doesn't match the body schema, the API will return a 400 Bad Request response with the following error message:

```json
// response on bad request
{
  "detail": "Invalid request body. Must be a valid JSON object."
}

// response on invalid schema
{
  "detail": "Body schema is invalid: ERROR"
}
```


If an internal server error occurs, the API will return a 500 Internal Server Error response with the following error message:

```json
{
  "detail": "Internal server error."
}
```

## Aderencia Endpoint
This endpoint calculates the Kolmogorov-Smirnov (KS) test statistic and the Jensen-Shannon (JS) divergence for a given dataset path.

#### Request
```bash
POST /aderencia
Content-Type: application/json
```

#### The request body must follow the following schema:
A record should have the following format:
```json
{
  "type": "object",
  "properties": {
    "path": {
      "type": "string"
    }
  },
  "required": [
    "path"
  ]
}
```

#### Response
If the request is successful, the API will return a JSON response object containing the KS test statistics and the JS divergence:

```json
{
  "ks_test": {
    "ks_statistic": 0.101,
    "p_value": 0.439
  },
  "js_divergence": 0.102
}
```

#### Erros handling
If the request body is not a valid JSON object or the body doesn't match the body schema, the API will return a 400 Bad Request response with the following error message:

```json
// response on bad request
{
  "detail": "Invalid request body. Must be a valid JSON object."
}

// response on invalid schema
{
  "detail": "Body schema is invalid: ERROR"
}
```

If the request path or file doesn't exists, the API will return 404 Not Found Request response with the following error message:

// response on invalid schema
{
  "detail": "No such file or directory in the provide path."
}
```

If an internal server error occurs, the API will return a 500 Internal Server Error response with the following error message:

```json
{
  "detail": "Internal server error."
}
```
