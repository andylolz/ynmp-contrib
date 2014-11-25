from os import system
import json

import requests


tmpl = 'https://candidates.democracyclub.org.uk/api/v0.9/' + \
       'logged_actions/?format=json&page={}&page_size=200'
page = 1
data = []
while True:
    print('Page {} - {} found. Latest: {}'.format(
        page,
        len(data),
        data[-1]['created'][:7] if len(data) > 0 else '-'
        ))
    j = requests.get(tmpl.format(page)).json()
    if 'results' not in j:
        break
    data += [r for r in j['results']]
    page += 1

with open('../data.json', 'w') as f:
    json.dump(data, f)

for idx, x in enumerate(data):
    if x['user'] == 'andylolz':
        author = ''
    else:
        author = '{0} <{0}@users.noreply.github.com>'.format(x['user'])
        author = '--author="{}"'.format(author)
    with open('commit.log', 'w') as f:
        if idx % 2 == 0:
            f.write('.')
        else:
            f.write('-')
    if idx == 0:
        _ = system('git add .')
    commit_tmpl = 'git commit -a --allow-empty-message ' + \
                  '--message="{}" --date="{}" {}'
    cmd = commit_tmpl.format(
        x['source'].replace('"', '\\"').replace('`', '\''),
        x['created'],
        author,
    )
    output = system(cmd)
    if output != 0:
        print('argh')
        break
