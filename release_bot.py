import requests
import random
import csv
import os
import bot_script
from pprint import pprint

pub_api_url = 'http://www.ebi.ac.uk/pdbe/api/pdb/entry/publications/'
search_url = 'http://www.ebi.ac.uk/pdbe/search/latest/select?q='
pdb_group = '&group=true&group.field=pdb_id&group.ngroups=true'
search_variables = '&wt=json&rows=999'
jrnl_csv = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'journal_twitter.csv')


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
    #print(full_query)
    response = url_response(full_query)
    #pprint(response)
    if 'grouped' in response:
        if 'pdb_id' in response['grouped']:
            #pprint(response['grouped'])
            if 'groups' in response['grouped']['pdb_id']:
                #pprint(response['grouped']['pdb_id']['groups'])
                result_list = []
                for group in response['grouped']['pdb_id']['groups']:
                    if 'doclist' in group:
                        #pprint(group['doclist'])
                        if 'docs' in group['doclist']:
                            #pprint(group['doclist']['docs'])
                            result_list.append(group['doclist']['docs'])
                results = result_list
                return results
    return None


def get_pdbid(results):
    pdb_list = []
    for result in results:
        for param in result:
            pdbid = param['pdb_id']
            pdb_list.append(pdbid)
    pdbid = random.choice(pdb_list)
    return pdbid


def get_journal(id_search_terms):
    results = run_search(id_search_terms)
    for result in results:
        for param in result:
            if 'journal' in param:
                journal = param['journal']
                if journal.lower() == "to be published":
                    return 'unpublished'
                f = open(jrnl_csv, 'r')
                reader = csv.reader(f)
                rownum = 0
                for line in reader:
                    if line[0] == journal:
                        if line[1]:
                            return line[1]
                f.close()
                if len(journal) > 19:
                    short_jrnl = (journal[:18] + '.')
                    return short_jrnl
                else:
                    return journal


def get_citation_title(id_search_terms):
    results = run_search(id_search_terms)
    for result in results:
        for param in result:
            if 'title' in param:
                title = (param['title'])
                if len(title) > 65:
                    short_title = (title[:63] + '..')
                    return short_title
                else:
                    return title


def get_message(pdbid, journal, title):
    if journal == 'unpublished':
        message = "'%s' Find it at PDBe.org/%s" % (title, pdbid)
    else:
        message = "'%s' published in %s. Find it at PDBe.org/%s" % (title, journal, pdbid)
    return message


def assembly_url_list(pdbid):
    views = ['front', 'side', 'top']
    url_list = []
    for view in views:
        url = "http://www.ebi.ac.uk/pdbe/static/entry/%s_assembly_1_chemically_distinct_molecules_%s_image-800x800.png" % (pdbid, view)
        url_list.append(url)
    return url_list

if '__main__' in __name__:
    search_terms = 'entry_type:new' + pdb_group
    results = run_search(pdbe_search_term=search_terms)
    pdbid = get_pdbid(results)
    id_search_terms = pdbid + pdb_group
    journal = get_journal(id_search_terms)
    title = get_citation_title(id_search_terms)
    message = get_message(pdbid, journal, title)
    url_list = assembly_url_list(pdbid)
    bot_script.twitter_api()
    bot_script.tweet_image(url_list, message)
