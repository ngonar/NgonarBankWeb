# Ngonar Bank Web

Contains the API and User Interface

Run the web :
```commandline
python manage.py runserver
```

### The flow 
1. Receive the API request 
```commandline
http://127.0.0.1:8000/account/api/debalacc/0354888999/100
```

2. Put the request onto MQ protocol
```python
q_body = 'deduct.' + norek + '.' + str(amount)
ngonarbank = NgonarBankRpcClient()
result = ngonarbank.call(q_body)
```
3. Get the response from MQ
```python
result = ngonarbank.call(q_body)
```
4. Send the response as HTTP Response
```python
return HttpResponse(result, content_type='application/json')
```


### Reference 
https://www.rabbitmq.com







