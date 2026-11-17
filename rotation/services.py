from statistics import mean
from .allocation import assignment_at


def save_service(store, row):
    if row['status'] not in ['completed', 'interrupted', 'cancelled']:
        raise ValueError('服务状态不合法')
    if row['score'] is not None and not 1 <= row['score'] <= 5:
        raise ValueError('感受评分超出范围')
    if row['minutes'] < 0:
        raise ValueError('时长不能为负')
    return store.put('services', row)


def descriptive_periods(store):
    groups = {}
    unassigned = []
    for row in store.all('services'):
        allocation = assignment_at(store, row['team'], row['date'])
        if allocation is None:
            unassigned.append(row['id'])
            continue
        key = allocation['id']
        group = groups.setdefault(key, {'assignment': key, 'arm': allocation['arm'], 'services': 0, 'completed': 0, 'scores': [], 'minutes': 0})
        group['services'] += 1
        group['completed'] += row['status'] == 'completed'
        group['minutes'] += row['minutes']
        if row['score'] is not None:
            group['scores'].append(row['score'])
    for group in groups.values():
        scores = group.pop('scores')
        group['score_count'] = len(scores)
        group['score_mean'] = mean(scores) if scores else None
    return {'periods': list(groups.values()), 'unassigned': unassigned, 'interpretation': '仅描述当期记录，不表示培训效果'}
