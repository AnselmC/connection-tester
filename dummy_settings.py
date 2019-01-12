#!/usr/bin/env python
# -*- coding: utf-8 -*-
sender = 'your.adress@host.com'  # Your address
password = '#s0oPerSTr0nGpä$$\\/\\/ord'  # Your password
server_name = 'mail.host.com'  # Your mail server address
server_port = 587  # Your mail server port
ISP = 'customer_service@isp.com'  # Your ISP customer service address
contract_no = '1234'  # The ID of your contract
subject = 'Notification concerning low bandwidth'
body = 'Dear customer support,\n' + \
    'This is an automated message informing you about ' + \
    'underperforming bandwidth.\n My advertised up- and ' + \
    'download speeds for contract {contract_no} are {up} Mbps and ' +\
    '{down} Mbps, respectively.\n' + \
    'However, {runs} speed tests conducted between {start} and {end} ' + \
    'showed average speeds of {avg_up} Mbps and {avg_down} Mbps, ' + \
    'respectively. Attached you can find a time sequence.\n' + \
    'Please resolve this issue in a timely matter.'