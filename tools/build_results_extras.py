# -*- coding: utf-8 -*-
"""Add double-dummy analysis and the player index to the results archive.

1. Double dummy: tools/dd/dds_results.jsonl.gz holds, for every distinct deal
   (hands + dealer + vulnerability), the output of the DDS solver
   (https://github.com/dds-bridge/dds, Apache-2.0) run through
   tools/dd/driver.cpp: tricks for each strain/declarer, dealer par and the
   tricks the declarer takes after every possible opening lead.
   Each board in public/data/results/events/*.json gets a "dds" block.
   Where Bridgewebs itself published makeable contracts for a board, they are
   checked against the solver and any mismatch is reported (there should be none).

2. Player index: public/data/results/players.json lists every player name found
   in the rankings with the events, positions and scores, for the search box.

Run after tools/bridgewebs_import.py.
"""
import gzip, json, os, re, glob, collections

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EVDIR = os.path.join(BASE, 'public', 'data', 'results', 'events')
DDFILE = os.path.join(BASE, 'tools', 'dd', 'dds_results.jsonl.gz')
STRAINS = ['NT', 'S', 'H', 'D', 'C']
SEATS = 'NESW'


def deal_key(b):
    return ' '.join('.'.join(b['hands'][p]) for p in SEATS) + '|' + (b.get('dealer') or 'N') + '|' + (b.get('vul') or 'None')


def load_dd():
    if not os.path.exists(DDFILE):
        print('no DD file, skipping double dummy')
        return {}
    idx = {}
    with gzip.open(DDFILE, 'rt', encoding='utf-8') as f:
        for line in f:
            o = json.loads(line)
            idx[o['key']] = o
    return idx


def check_against_bridgewebs(b, dd):
    """Bridgewebs makeable data: 'dd' = tricks, 'ddl' = levels (tricks - 6, '-' when < 7)."""
    bad = 0
    for p in 'NSEW':
        si = SEATS.index(p)
        for k, st in enumerate(STRAINS):
            t = dd[k][si]
            if b.get('dd') and b['dd'].get(p, {}).get(st, '') not in ('', None):
                if int(b['dd'][p][st]) != t:
                    bad += 1
            if b.get('ddl') and b['ddl'].get(p, {}).get(st, '') not in ('', None):
                lv = b['ddl'][p][st]
                exp = str(t - 6) if t > 6 else '-'
                if lv != exp:
                    bad += 1
    return bad


def split_names(txt):
    out = []
    for part in re.split(r'[\n&,/]', txt or ''):
        n = re.sub(r'\s+', ' ', part).strip()
        if n and n.upper() != 'N/A' and len(n) > 1:
            out.append(n)
    return out


def norm(n):
    return re.sub(r'[^a-z0-9؀-ۿ]+', ' ', n.lower()).strip()


def main():
    dd = load_dd()
    players = collections.defaultdict(lambda: {'names': collections.Counter(), 'e': []})
    checked = mism = withdd = 0
    for fp in sorted(glob.glob(os.path.join(EVDIR, '*.json'))):
        ev = json.load(open(fp, encoding='utf-8'))
        changed = False
        for si, sec in enumerate(ev['sections']):
            for b in sec.get('boards', []):
                if not b.get('hands'):
                    continue
                o = dd.get(deal_key(b))
                if not o:
                    continue
                b['dds'] = {'t': o['dd'], 'par': o['par'], 'parc': o['parc'], 'leads': o['leads']}
                withdd += 1
                changed = True
                if b.get('dd') or b.get('ddl'):
                    checked += 1
                    if check_against_bridgewebs(b, o['dd']):
                        mism += 1
                        print('DD mismatch', ev['id'], si, b['bd'])
            # players from ranking tables
            for t in sec['ranking']['tables']:
                if not t:
                    continue
                head = [c['t'].replace('\n', ' ') for c in t[0]]
                try:
                    pc = head.index('Players')
                except ValueError:
                    continue
                teams = 'Team' in head
                direction = ''
                for r in t[1:]:
                    if len(r) == 1 and r[0].get('h'):
                        txt = r[0]['t'].lower()
                        direction = 'NS' if 'north' in txt else ('EW' if 'east' in txt else '')
                        continue
                    if any(c.get('h') for c in r) or len(r) <= pc:
                        continue
                    pos = r[0]['t']
                    no = r[1]['t'] if len(r) > 1 else ''
                    names = split_names(r[pc]['t'])
                    score = ''
                    label = head[pc + 1] if len(head) > pc + 1 else ''
                    tot = [h for h in head if h.startswith('Total')]
                    if tot:
                        # team events: the total is counted from the end of the row, past e.g. Wins/Draws, Master Points
                        k = len(head) - 1 - head.index(tot[0])
                        if len(r) - 1 - k > pc:
                            score = r[len(r) - 1 - k]['t']
                        label = tot[0]
                    else:
                        for c in r[pc + 1:]:
                            if re.match(r'^[+-]?\d+(\.\d+)?$', c['t'] or ''):
                                score = c['t']
                                break
                    team = r[2]['t'] if teams and len(r) > 3 else ''
                    if teams:
                        pair_key = 'NS:' + no
                    elif direction:
                        pair_key = direction + ':' + no
                    else:
                        pair_key = ':' + no
                    for n in names:
                        k = norm(n)
                        if not k:
                            continue
                        partners = [x for x in names if x != n]
                        players[k]['names'][n] += 1
                        players[k]['e'].append([ev['id'], si, pos, score, label, pair_key, team, ' & '.join(partners[:5])])
        if changed:
            json.dump(ev, open(fp, 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
    # winners for the event list (position 1 of the first ranking table, as published)
    ip = os.path.join(BASE, 'public', 'data', 'results', 'index.json')
    index = json.load(open(ip, encoding='utf-8'))
    for e in index['events']:
        ev = json.load(open(os.path.join(EVDIR, e['id'] + '.json'), encoding='utf-8'))
        e.pop('winner', None)
        tabs = ev['sections'][0]['ranking']['tables']
        if not tabs:
            continue
        head = [c['t'].replace('\n', ' ') for c in tabs[0][0]]
        if 'Players' not in head:
            continue
        pc = head.index('Players')
        for r in tabs[0][1:]:
            if r and not r[0].get('h') and re.match(r'^1=?$', r[0]['t'] or '') and len(r) > pc:
                team = r[2]['t'] if 'Team' in head and len(r) > 2 else ''
                names = [n for n in split_names(r[pc]['t'])]
                e['winner'] = team if team and team.upper() not in ('N/A',) else ' & '.join(names)
                break
        e['dd'] = any(b.get('dds') for s in ev['sections'] for b in s.get('boards', []))
    json.dump(index, open(ip, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

    out = []
    for k, v in players.items():
        out.append({'k': k, 'n': v['names'].most_common(1)[0][0], 'e': v['e']})
    out.sort(key=lambda x: x['n'].lower())
    json.dump({'players': out}, open(os.path.join(BASE, 'public', 'data', 'results', 'players.json'), 'w', encoding='utf-8'),
              ensure_ascii=False, separators=(',', ':'))
    print(f'boards with DD: {withdd}; checked against Bridgewebs: {checked}; mismatches: {mism}; players: {len(out)}')


if __name__ == '__main__':
    main()
