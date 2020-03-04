# encoding: utf8

import ipdb
import sys
import json
from .util import is_ip
# from util import is_ip


class IpLoction:
    ipkey_map = {
        'country_name': "country",
        'region_name': "region",
        'owner_domain': "user_type",
        'isp_domain': "isp",
        'latitude': 'latitude',
        'longitude': 'longitude',
        'country_code3': 'country_code',
        'idc': 'idc',
        'base_station': 'base_station'
    }

    def __init__(self, ipdb_file):
        self.db = ipdb.City(ipdb_file)

    def _remap(self, d):
        ret = {}
        for k, newk in self.ipkey_map.items():
            ret[newk] = d[k]
        return ret

    def db_info(self):
        print(self.db.is_ipv4(), self.db.is_ipv6())
        print(self.db.languages())  # support language
        print(self.db.build_time())  # build database time
        print(self.db.fields())  # support fields

    def test(self):
        print(self.db.find("1.1.1.1", "CN"))  # query ip return array
        # print(db.find(u"1.1.1.1", "CN")) #  Python 2.7
        print(self.db.find_map("8.8.8.8", "CN5"))  # query ip return dict
        print(self.db.find_info("118.28.1.1", "CN").country_name)

    def loc_file(self, ipfile, output_file):
        resfp = open(output_file, 'w', encoding='utf-8')
        with open(ipfile, 'r', encoding='utf-8') as fp:
            for line in fp:
                ip = line.strip()
                if not is_ip(ip):
                    print(ip)
                    continue
                info = self.db.find_map(ip, "CN")
                newinfo = self._remap(info)
                newinfo['ip'] = ip
                resfp.write(json.dumps(newinfo) + '\n')
        resfp.close()

    def loc(self, ip):
        if not is_ip(ip):
            print(ip)
            return None
        info = self.db.find_map(ip, "CN")
        newinfo = self._remap(info)
        return newinfo


if __name__ == "__main__":
    il = IpLoction('./data/ipip/mydata4vipday3_cn.ipdb')
    print(il.loc('1.1.1.1'))
    print(il.loc('110.110.110.110'))
    print(il.loc('123.58.64.130'))