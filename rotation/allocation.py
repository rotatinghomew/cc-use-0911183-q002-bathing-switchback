from datetime import date


def save_assignment(store, row):
    date.fromisoformat(row['start'])
    date.fromisoformat(row['end'])
    if row['start'] >= row['end'] or row['arm'] not in ['trained', 'usual']:
        raise ValueError('班组安排不合法')
    for old in store.all('assignments'):
        if old['id'] != row['id'] and old['team'] == row['team'] and row['start'] < old['end'] and old['start'] < row['end']:
            raise ValueError('班组时段重叠')
    return store.put('assignments', row)


def assignment_at(store, team, day):
    date.fromisoformat(day)
    rows = [row for row in store.all('assignments') if row['team'] == team and row['start'] <= day < row['end']]
    return rows[0] if rows else None


def attendance(store, course):
    return sorted({row['person'] for row in store.all('attendance') if row['course'] == course and row['attended']})
