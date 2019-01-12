#!/usr/bin/env python
# -*- coding: utf-8 -*-
import smtplib
import logging
import time
import io

import matplotlib
# For macOS
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

from settings import *

from email import encoders
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase


class ActionHandler(object):
    """
    An abstract class that is used for handlers that notify an ISP of
    bad performance.
    """

    def perform_action(self, results, config):
        """
        Informs the ISP of bad performance

        Parameters
        ----------
        results: dict
            A dictionary of the results of the speed tests
        config: dict
            A dictionary of the configuration for the speed tests
        """

        raise NotImplementedError('This method is required for an\
            ActionHandler object')


class MailHandler(ActionHandler):
    """
    A mail handler that notifies the ISP of bad performance by sending a mail.
    """

    def __init__(self):
        self.lg = logging.getLogger(__name__)
        self.sender = sender
        self.password = password
        self.server_name = server_name
        self.server_port = server_port
        self.ISP = ISP

    def perform_action(self, results, config):
        """
        Implements the perform action method.
        """
        mail = MIMEMultipart()
        mail['Subject'] = subject
        mail['From'] = self.sender
        mail['To'] = self.ISP
        graph = self.create_graph(results, config)
        body = MIMEText(self.create_msg(results, config), 'plain')
        attachment = MIMEBase('application', 'octet-stream')
        attachment.set_payload(graph.read())
        encoders.encode_base64(attachment)
        attachment.add_header('Content-Disposition',
                              'attachment; filename="%s"' % 'speed_test.png')
        mail.attach(body)
        mail.attach(attachment)
        server = smtplib.SMTP(self.server_name, self.server_port)
        try:
            self.lg.debug('Identifying to server')
            server.ehlo()
            if server.has_extn('STARTTLS'):
                self.lg.debug('Starting TLS')
                server.starttls()
                server.ehlo()  # reidentify ourselves over TLS connection
            else:
                self.lg.debug('no STARTTLS')

            if server.has_extn('AUTH'):
                self.lg.debug('logging in')
                server.login(self.sender, self.password)
            else:
                self.lg.debug('no AUTH required')
            self.lg.debug('Sending mail')
            server.sendmail(self.sender,
                           self.ISP,
                           mail.as_string())
        finally:
            self.lg.debug('Closing server')
            server.quit()

    def create_graph(self, results, config):
        timestamps = results['timestamp']
        results_up = results['upload']
        results_down = results['download']
        up = config['upload']
        down = config['download']

        # list of dates from timestamps
        dates = [time.strftime('%e %b %Y', ts) for ts in timestamps]
        times = [time.strftime('%H:%M', ts) for ts in timestamps]
        # string with date(s) of the time stamps
        from_to = '-'.join(list(sorted(set(dates))))
        fig, ax = plt.subplots()
        ax.plot(times, results_up, label="Upload")
        ax.plot(times, results_down, label="Download")
        ax.axhline(down, c='orange', linestyle=':',
                   label='Advertised Download speed')
        ax.axhline(up, c='blue', linestyle=':',
                   label='Advertised Upload speed')
        ax.set_title('Bandwidth results from {}'.format(from_to))
        ax.set_ylabel('Mbps')
        ax.legend()

        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        return buf

    def create_msg(self, results, config):
        timestamps = results['timestamp']
        results_up = results['upload']
        results_down = results['download']
        up = config['upload']
        down = config['download']
        runs = config['runs']
        avg_up = sum(results_up) / len(results_up)
        avg_down = sum(results_down) / len(results_down)
        start = time.strftime('%e %b %Y, %H:%M:%S', timestamps[0])
        end = time.strftime('%e %b %Y, %H:%M:%S', timestamps[-1])
        msg = body.format(contract_no=contract_no, up=up,
                          down=down, runs=runs, start=start, end=end,
                          avg_up=avg_up, avg_down=avg_down)
        return msg
