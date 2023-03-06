from django.shortcuts import render
from django.template import  loader
from django.http import HttpResponse

from .extra.MQAccountRequest import MQAccountRequest
from .models import BankAccount
import json
import pika
import uuid

def index(request):
    bank_account = BankAccount.objects.all()
    context = {
        'bank_account': bank_account
    }

    for acc in bank_account :
        print(acc)

    template = loader.get_template('bank_account.html')
    return HttpResponse(template.render(context, request))


def get_accounts(request):
    bank_account = BankAccount.objects.all()
    all_accounts = [{"account_no":acc.account_no} for acc in bank_account]
    return HttpResponse(json.dumps(all_accounts), content_type='application/json')


def deduct_account_balance(request, norek=None, amount=None):
    print("norek ", norek)
    print("amount ", amount)

    result = ""

    if norek and amount:

        the_account = BankAccount.objects.get(account_no=norek)
        print(the_account)

        mqReq = MQAccountRequest()
        mqReq.norek = norek
        mqReq.amount = str(amount)
        mqReq.action = "deduct"

        q_body = json.dumps(mqReq.__dict__)

        ngonarbank = NgonarBankRpcClient()
        result = ngonarbank.call(q_body)
    print(result)
    return HttpResponse(result, content_type='application/json')


def topup_account_balance(request, norek=None, amount=None):
    print("norek ", norek)
    print("amount ", amount)

    result = ""

    if norek and amount:
        the_account = BankAccount.objects.get(account_no=norek)
        print(the_account)

        mqReq = MQAccountRequest()
        mqReq.norek = norek
        mqReq.amount = str(amount)
        mqReq.action = "topup"

        q_body = json.dumps(mqReq.__dict__)

        ngonarbank = NgonarBankRpcClient()
        result = ngonarbank.call(q_body)

    print(result)
    return HttpResponse(result, content_type='application/json')

def send_to_mq(q_body=None):
    if q_body:
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host='localhost',
                credentials=pika.PlainCredentials(username='rabbit', password='admin')))
        channel = connection.channel()

        channel.queue_declare(queue='balance')

        channel.basic_publish(
            exchange='',
            routing_key='balance',
            body=q_body)

        print("[x] sent ", q_body)

        connection.close()


class NgonarBankRpcClient(object):

    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost', credentials=pika.PlainCredentials(username='rabbit', password='admin')))

        self.channel = self.connection.channel()

        result = self.channel.queue_declare(queue='', exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True)

        self.response = None
        self.corr_id = None

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def call(self, n):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='',
            routing_key='rpc_queue',
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=str(n))
        self.connection.process_data_events(time_limit=None)
        return str(self.response.decode())