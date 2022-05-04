**Integration**
=================

# Usage

- Install packages
    - **NOTE:** It is possible you will want to use a virtualenv for this to avoid breaking your native Python install!
```
pip install -U -r requirements.txt
```

# Run tests
   - Where $ENVIRONMENT = env_dev.yaml, env_int.yaml, env_latest.yaml, etc.
```
pytest tests/gateway_integration --env=environments/$ENVIRONMENT.yaml
```

   - To run a specific test case use the file($FILE), class($CLASS), function($FUNC), and parameter($PARAM) if applicable
```
pytest tests/gateway_integration/$FILE.py::$CLASS::$FUNC[$PARAM] --env=environments/$ENVIRONMENT.yaml
```

   - Additionally you can run or not run marked tests.
```
pytest -m smoke tests/gateway_integration --env=environments/$ENVIRONMENT.yaml
pytest -m "not notprodsafe" tests/gateway_integration --env=environments/$ENVIRONMENT.yaml
```
    
   - To generate an allure report add the --alluredir flag
```
pytest tests --env=environments/$ENVIRONMENT.yaml --alluredir results/allure-results
```
