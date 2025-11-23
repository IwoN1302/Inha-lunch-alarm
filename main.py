import requests
from inha_tc import get_inhatc_lunch_menu
from inha_univ import get_inha_uni_lunch_final

webhook_url="https://discord.com/api/webhooks/1442171364424552532/fkzijIbbTTEuXcCsDodEDV90NqSjTNaTy3oJXXSWjgnsOkTs8I6641fVpBjyEdq1N2_b"

inha_univ_menu=get_inha_uni_lunch_final()
inha_tc_menu=get_inhatc_lunch_menu()

inha_menu=inha_univ_menu + "\n"*2 + inha_tc_menu

data={
    "content":inha_menu
}

requests.post(webhook_url, json=data)