#!/usr/bin/env python
# -*- coding: utf-8 -*-


from __future__ import print_function
from __future__ import division

import speedtest
import argparse
import actionhandler
import logging
import time

from time import sleep


__author__ = 'Anselm Coogan'
__program__ = 'ConnectionTester'
__description__ = 'Automatically inform your ISP if your bandwidth \
                    is not as advertised'
__version__ = 0.1


class ConnectionTester(object):
    """
    A class that performs speed tests and notifies an ISP if performance is bad
    """

    def __init__(self, min_runs, interval,
                 tolerance, up, down):
        """
        ConnectionTester constructor.

        Parameters
        ----------
        mail_info: list of info needed for sending mail to ISP
            The list consists of the sender address, sender password, and ISP
            address
        min_runs: int
            The minimum amount of times a speed test should be done before
            performance is evaluated
        interval: int
            The time to wait in between speed tests in minutes
        up: int
            The maximum upload speeds the ISP claims to provide (in Mbps)
        down: int
            The maximum download speeds the ISP claims to provide (in Mbps)
        tolerance: int
            If the performance of up- and download falls below this threshold
            the ISP is notified (in %)
        """

        self.min_runs = min_runs
        self.interval = interval
        self.up = up
        self.down = down
        self.tolerance = tolerance
        self.config = self.get_config_dict()
        self.st = speedtest.Speedtest()
        self.runs = 1
        self.action_handlers = []
        self.action_handlers.append(actionhandler.MailHandler())
        # results are treated as FIFO queues
        self.results_up = []
        self.results_down = []
        self.results_timestamp = []
        self.bad_performance = False
        self.lg = logging.getLogger(__program__)
        self.lg.info('Started ConnectionTester...')
        self.lg.debug(('Runs: {0}\nInterval: {1}\nUpload: {2}\nDownload: {3}\nTolerance: {4}').format(
            min_runs, interval, up, down, tolerance))

    def test_connection(self):
        """
        Perform a speed test, check performance, and notify ISP if necessary.
        """

        self.speed_test()
        if self.runs >= self.min_runs:
            self.lg.debug('Minimum number of speed tests performed.')
            self.check_performance()
        if self.bad_performance:
            self.lg.debug('Performance is below tolerance level.')
            self.notify_ISP()
            self.results_up.pop(0)
            self.results_down.pop(0)
            self.results_timestamp.pop(0)
        self.runs += 1

    def speed_test(self):
        """
        Perform the speed test and add result dict to `results` list object.
        """
        self.lg.debug('Performing speed test no. {}'.format(self.runs))
        self.st.get_best_server()
        self.st.upload()
        self.st.download()
        up = self.st.results.upload // 1e6
        down = self.st.results.download // 1e6
        timestamp = time.localtime(time.time())
        self.lg.debug('Timestamp: {}'.format(
            time.strftime('%H:%M:%S', timestamp)))
        self.lg.debug(
            'Upload is {} Mbps'.format(up))
        self.lg.debug(
            'Download is {} Mbps'.format(down))
        self.results_up.append(up)
        self.results_down.append(down)
        self.results_timestamp.append(timestamp)

    def get_results_dict(self):
        results = {}
        results['upload'] = self.results_up
        results['download'] = self.results_down
        results['timestamp'] = self.results_timestamp
        return results

    def get_config_dict(self):
        config = {}
        config['upload'] = self.up
        config['download'] = self.down
        config['runs'] = self.min_runs
        config['interval'] = self.interval
        config['tolerance'] = self.tolerance
        return config

    def check_performance(self):
        """
        Checks whether average performance falls below determined threshold.
        """
        self.lg.debug('Checking performance.')
        avg_up = (sum(self.results_up)) / len(self.results_up)
        avg_down = (sum(self.results_down)) / len(self.results_down)
        if (
            avg_up < self.tolerance * self.up or
            avg_down < self.tolerance * self.down
        ):
            self.bad_performance = True
        else:
            self.bad_performance = False

    def notify_ISP(self):
        """
        Notify an ISP by means specified through the action handlers.
        """
        self.lg.debug('Notifying the ISP about bad performance.')
        for handler in self.action_handlers:
            handler.perform_action(
                results=self.get_results_dict(),
                config=self.config
            )


def parse_args(args):
    parser = argparse.ArgumentParser(description=__description__)

    parser.add_argument(
        '-i', '--interval',
        type=int,
        help='The interval in minutes in between speed tests \
            (default is 10)',
        default=10
    )
    parser.add_argument(
        '-u', '--up',
        type=float,
        help='The upload speed your ISP claims to provide \
            (default is 20)',
        default=20.
    )
    parser.add_argument(
        '-d', '--down',
        type=float,
        help='The download speed your ISP claims to provide \
            (default is 100)',
        default=100.
    )
    parser.add_argument(
        '-r', '--runs',
        type=int,
        help='The number of tests that should be averaged (default is 5)',
        default=5
    )
    parser.add_argument(
        '-t',
        type=int,
        choices=range(0, 100,),
        help='The minimum percentage of performance to tolerate \
            (default is 50)',
        default=50
    )
    return parser.parse_args(args)


def main(args=None):
    # Set up logging
    logging.basicConfig(
        filename='app.log',
        filemode='a',
        format='%(name)s - %(levelname)s - %(message)s')
    logging.getLogger(__program__).setLevel(logging.DEBUG)
    logging.getLogger(__program__).addHandler(logging.StreamHandler())
    options = parse_args(args)
    tester = ConnectionTester(
        options.runs,
        options.interval,
        options.t,
        options.up,
        options.down
    )

    while(True):
        tester.test_connection()
        sleep(options.interval * 60)


if __name__ == '__main__':
    main()
