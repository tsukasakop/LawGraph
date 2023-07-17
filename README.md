# purpose
- Making legal texts more easily understandable through visualization
- Utilizing graph data representation for processing legal texts
# get starting
1. download raw law data
  - get law name list info
    ```sh
    curl https://elaws.e-gov.go.jp/api/1/lawlists/2
    ```
 - get raw law text info by law-id
    ```sh
    curl https://elaws.e-gov.go.jp/api/1/lawdata/{lawId}
    ```

    case: 日本国憲法 `lawId: 321CONSTITUTION`
    ```sh
    curl https://elaws.e-gov.go.jp/api/1/lawdata/321CONSTITUTION
    ```
 
2. convert to neo4j
```
python main.py
```
