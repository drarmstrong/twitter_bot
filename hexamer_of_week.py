import os
from release_bot import get_pdbid, get_journal, get_citation_title, run_search
from bot_script import twitter_api, tweet_image

pub_api_url = 'http://www.ebi.ac.uk/pdbe/api/pdb/entry/publications/'
search_url = 'http://www.ebi.ac.uk/pdbe/search/latest/select?q='
pdb_group = '&group=true&group.field=pdb_id&group.ngroups=true'
search_variables = '&wt=json&rows=999'
jrnl_csv = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'journal_twitter.csv')


def get_assembly_id(search_results, pdbid):
    for result in search_results:
        for param in result:
            if param['pdb_id'] == pdbid:
                type_list = param['assembly_type']
                id_list = param['assembly_id']
                type_and_list = zip(type_list, id_list)
                for type, id in type_and_list:
                    if type == 'hexamer':
                        return id


def get_message(pdbid, journal, title):
    if journal == 'unpublished':
        message = "#HexamerOfTheWeek '%s' Find it at PDBe.org/%s" % (title, pdbid)
    else:
        if len(title) > 47:
            short_title = (title[:45] + "..")
            message = "#HexamerOfTheWeek '%s' published in %s. Find it at PDBe.org/%s" % (short_title, journal, pdbid)
        else:
            message = "#HexamerOfTheWeek '%s' published in %s. Find it at PDBe.org/%s" % (title, journal, pdbid)
    return message


def assembly_url(pdbid, assembly_id):
    views = ['front', 'side', 'top']
    url_list = []
    for view in views:
        url = "http://www.ebi.ac.uk/pdbe/static/entry/%s_assembly_%s_chemically_distinct_molecules_%s_image-800x800.png" % (pdbid, assembly_id, view)
        url_list.append(url)
    return url_list


search_terms = 'assembly_type:"hexamer" AND assembly_form:"homo"' + pdb_group
results = run_search(pdbe_search_term=search_terms)
pdbid = get_pdbid(results)
id_search_terms = pdbid + pdb_group
journal = get_journal(id_search_terms)
title = get_citation_title(id_search_terms)
message = get_message(pdbid, journal, title)
assembly_id = get_assembly_id(results, pdbid)
url_list = assembly_url(pdbid, assembly_id)
twitter_api()
tweet_image(url_list, message)
