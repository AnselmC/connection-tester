# connection-tester
Python script to automatically inform your ISP if your bandwidth is not as advertised.

*Disclaimer:* This project is still in early development. If you'd like to contribute, feel free to make a pull request.

This project uses `speedtest-cli` (https://github.com/sivel/speedtest-cli) to test bandwidth via speedtest.net and notifies your ISP (or anyone else if you like) if average performance is below a certain threshold. 
Currently, only email notification is possible.

## Installation
```
git clone https://github.com/AnselmC/connection-tester.git
pip install -r connectiontester/requirements.txt
```
To go ahead and update the `settings.py` file with your SMTP mail connection, the address(es) you want to send the notification to, and possibly a different message.
To write your own message, include the following formatting keys and consider their meaning:
 - `up`: The upload speed of your contract
 - `down`: The download speed of your contract
 - `contract_no`: Your contract number/ID
 - `avg_up`: The average upload speed of the conducted tests
 - `avg_down`: The average download speed of the conducted tests
 - `start`: The timestamp of the first test
 - `end`: The timestamp of the final test
 - `runs`: The total amount of runs

Finally, run:
``
python connectiontester/setup.py install
```

## Usage
```
$ connectiontester --help
usage: connectiontester [-h] [-i INTERVAL] [-u UP] [-d DOWN] [-r RUNS]
                        [-t {0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,90,91,92,93,94,95,96,97,98,99}]

Automatically inform your ISP if your bandwidth is not as advertised

optional arguments:
  -h, --help            show this help message and exit
  -i INTERVAL, --interval INTERVAL
                        The interval in minutes in between speed tests
                        (default is 10)
  -u UP, --up UP        The upload speed your ISP claims to provide (default
                        is 20)
  -d DOWN, --down DOWN  The download speed your ISP claims to provide (default
                        is 100)
  -r RUNS, --runs RUNS  The number of tests that should be averaged (default
                        is 5)
  -t {0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,90,91,92,93,94,95,96,97,98,99}
                        The minimum percentage of performance to tolerate
                        (default is 50)
```

