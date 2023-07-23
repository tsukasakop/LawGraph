# purpose
- Making legal texts more easily understandable through visualization
- Utilizing graph data representation for processing legal texts

# get starting
1. download raw law data
  - zip
    download from below
    ```
    https://elaws.e-gov.go.jp/download
    ```
  - or api
    
    get law-id
    ```sh
    curl https://elaws.e-gov.go.jp/api/1/lawlists/2
    ```
    
    get law text by law-id
    ```sh
    curl https://elaws.e-gov.go.jp/api/1/lawdata/{lawId}
    ```
    e.g. 日本国憲法 `lawId: 321CONSTITUTION`
    ```sh
    curl https://elaws.e-gov.go.jp/api/1/lawdata/321CONSTITUTION
    ```
 
2. import to neo4j
```
python main.py
```
