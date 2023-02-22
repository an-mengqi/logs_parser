import argparse
import json
import pathlib
import re


class LogInfo:

    def __init__(self, method, url, ip, duration, date_time):
        self.method = method
        self.url = url
        self.ip = ip
        self.duration = duration
        self.date_time = date_time


def find_info(path):
    info_list = []
    with open(path, 'r') as f:
        for line in f:
            method = re.search(r"\] \"(POST|GET|PUT|DELETE|HEAD|CONNECT|OPTIONS|TRACE)", line)
            founded_method = method.group(1)
            ip_match = re.search(r"(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})", line)
            founded_ip = ip_match.group(1)
            duration = re.search(r"\" (\d{1,5})$", line)
            founded_duration = duration.group(1)
            try:
                url = re.search(r"\"(http.+)\" \"", line)
                founded_url = url.group(1)
            except:
                founded_url = "-"
            date_time = re.search(r"\[(\S+ \+\d{4})\]", line)
            founded_date_time = date_time.group(1)

            log_info = LogInfo(method=founded_method,
                               url=founded_url,
                               ip=founded_ip,
                               duration=int(founded_duration),
                               date_time=founded_date_time)
            info_list.append(log_info)

    newlist = sorted(info_list, key=lambda x: x.duration, reverse=True)
    data = {'top_longest': [{'method': newlist[0].method,
                             'url': newlist[0].url,
                             'ip': newlist[0].ip,
                             'duration': newlist[0].duration,
                             'date_time':newlist[0].date_time},
                            {'method': newlist[1].method,
                             'url': newlist[1].url,
                             'ip': newlist[1].ip,
                             'duration': newlist[1].duration,
                             'date_time': newlist[1].date_time},
                            {'method': newlist[2].method,
                             'url': newlist[2].url,
                             'ip': newlist[2].ip,
                             'duration': newlist[2].duration,
                             'date_time': newlist[2].date_time},
                            ]}
    return data


def get_requests_number(path):
    with open(path, 'r') as f:
        count = 0
        for line in f:
            if line != "\n":
                count += 1
    data = {'total_requests': count}
    return data


def get_methods_with_numbers(path):
    key_list = ["POST", "GET", "PUT", "DELETE", "HEAD", "CONNECT", "OPTIONS", "TRACE"]
    methods_number = {}
    for x in key_list:
        methods_number[x] = 0
    with open(path, 'r') as f:
        for line in f:
            method = re.search(r"\] \"(POST|GET|PUT|DELETE|HEAD|CONNECT|OPTIONS|TRACE)", line)
            methods_number[method.group(1)] += 1
    data = {'methods': methods_number}
    return data


def get_ip(path):
    all_ip = []
    with open(path, 'r') as f:
        for line in f:
            ip_match = re.search(r"(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})", line)
            all_ip.append(ip_match.group(1))
    unique_ip = set(all_ip)
    ip_number = {}
    for ip in unique_ip:
        ip_number[ip] = 0
    with open(path, 'r') as f:
        for line in f:
            ip_match = re.search(r"(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})", line)
            ip_number[ip_match.group(1)] += 1
    sorted_ip_list = sorted(ip_number.items(), key=lambda x: x[1], reverse=True)
    data = {'top_ip': [{'top_first': sorted_ip_list[0], 'top_second': sorted_ip_list[1], 'top_third': sorted_ip_list[2]}]}
    return data


if __name__ == '__main__':
    parse = argparse.ArgumentParser(description='This script helps to parse log file access.log')
    parse.add_argument('-path',
                       '--path',
                       type=str,
                       help='Input full path to a file with logs',
                       required=True,
                       )
    args = parse.parse_args()

    if ".log" not in args.path:
        desktop = pathlib.Path(args.path)
        files = list(desktop.glob("*.log"))
        json_content = []
        for x in files:
            full_path = str(x)
            requests_number = get_requests_number(full_path)
            methods = get_methods_with_numbers(full_path)
            ip = get_ip(full_path)
            info = find_info(full_path)

            result = requests_number | methods | ip | info
            json_content.append(result)

        json_data = json.dumps(json_content, indent=4)
        with open('result.json', 'w') as f:
            f.write(json_data)
    else:
        requests_number = get_requests_number(args.path)
        methods = get_methods_with_numbers(args.path)
        ip = get_ip(args.path)
        info = find_info(args.path)

        result = requests_number | methods | ip | info

        json_data = json.dumps(result, indent=4)
        with open('result.json', 'w') as f:
            f.write(json_data)
