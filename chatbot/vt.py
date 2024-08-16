##from splunklib.searchcommands import dispatch, GeneratingCommand, Option, Configuration
import virustotal3.core
import json

from config import conf

VT_KEY = conf['virustotal']

def virustotal(query_item, query_type):
    """ virustotal api """
    result = {}
    if query_type == 'ip':
        virus_total = virustotal3.core.IP(VT_KEY)
        result = virus_total.info_ip(query_item)
    
    elif query_type == 'domain':
        virus_total = virustotal3.core.Domains(VT_KEY)
        result = virus_total.info_domain(query_item)

    elif query_type == 'url':
        virus_total = virustotal3.core.URL(VT_KEY)
        result = virus_total.info_url(query_item)

    elif query_type == 'hash':
        virus_total = virustotal3.core.Files(VT_KEY)
        result = virus_total.info_file(query_item)
    if 'data' in result and 'attributes' in result['data']:
        return result['data']['attributes']['last_analysis_stats']
    return result    


#result = virustotal('https://www.naver.com','url')
#print(result['data']['attribute']['last_analysis_stats'])
#print(result)
