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

### The result

#### Insufficient Balance 
```commandline
http://127.0.0.1:8000/account/api/debalacc/0354888999/1000000000
```
```json
{
  "rc": "0046",
  "last_balance": "996000",
  "current_balance": "996000",
  "description": "Insufficient Balance "
}
```

#### Topup Balance
```commandline
http://127.0.0.1:8000/account/api/addbalacc/0354888999/100
```
```json
{
  "rc": "0000",
  "last_balance": "995900",
  "current_balance": "996000",
  "description": "Topup Success to account 0354888999 for $100"
}
```

#### Deduct Balance
```commandline
http://127.0.0.1:8000/account/api/debalacc/0354888999/100
```
```json
{
  "rc": "0000",
  "last_balance": "996000",
  "current_balance": "995900",
  "description": "Deduct Success to account 0354888999 for $100"
}
```

## Processing Module
https://github.com/ngonar/NgonarBankCore

### Article
The article for this code is on [Medium](https://medium.com/@ngonar/one-concurrency-recipe-with-mq-flavored-line-81259a1c25e2)

### Reference 
https://www.rabbitmq.com






