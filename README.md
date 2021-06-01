# Vakinha Web Scraping

Python script to obtain campaigns from [Vakinha.com.br](https://www.vakinha.com.br/), and export them to a CSV or JSON file containing their names, collected amounts so far, and campaign goals.

## Parameters

| Name   | Short | Long     | Type   | Default | Supported Values |
| ------ | ----- | -------- | ------ | ------- | ---------------- |
| Output | -o    | --output | string | csv     | 'csv' or 'json'  |
| Pages  | -p    | --pages  | int    | 1       | -                |

## Samples

```bash
python vakinha.py # first page into a CSV file
```

```bash
python vakinha.py -o csv -p 3 # first 3 pages into a CSV file
```

```bash
python vakinha.py -o json -p 15 # first 15 pages into a json file
```
