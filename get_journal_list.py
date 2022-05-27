import requests
from pprint import pprint

search_url = 'http://www.ebi.ac.uk/pdbe/search/pdb/select?q='
search_variables = '&wt=json&rows=200000'
release_year = 2017


def url_response(url):
    #print(url)
    r = requests.get(url=url)
    if r.status_code == 200:
        json_result = r.json()
        return json_result
    else:
        print(r.status_code, r.reason)
        return None


def run_search(pdbe_search_term):
    full_query = search_url + pdbe_search_term + search_variables

    response = url_response(full_query)
    journal_list = []
    if 'grouped' in response:
        if 'pdb_id' in response['grouped']:
            if 'groups' in response['grouped']['pdb_id']:
                for entry in response['grouped']['pdb_id']['groups']:
                    if 'doclist' in entry:
                        if 'docs' in entry['doclist']:
                            for param in entry['doclist']['docs']:
                                if 'journal' in param:
                                    journal = param['journal']
                                    if journal not in journal_list:
                                        journal_list.append(journal)
    else:
        return 'No response'
    return journal_list

f = open('journal_list.csv', 'w')

search_terms = 'release_year:%s&group=true&group.field=pdb_id&group.ngroups=true&fq_status:REL' % release_year
journal_search = sorted(run_search(search_terms))
#pprint(journal_search)
for journal in journal_search:
    f.write('%s,\n' % journal)

f.close()
