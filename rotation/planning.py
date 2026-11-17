def course_costs(store):
    rows = []
    for course in store.all('courses'):
        people = [row for row in store.all('attendance') if row['course'] == course['id']]
        rows.append({'course': course['id'], 'cents': course['fixed_cents'] + sum(row['hours'] * course['hour_cents'] for row in people), 'registered': len(people)})
    return rows


def quote_expansion(store, teams):
    if len(set(teams)) != len(teams):
        raise ValueError('班组重复')
    rows = [store.get('candidates', team) for team in teams]
    return {'teams': teams, 'cents': sum(row['training_cents'] for row in rows), 'service_slots': sum(row['service_slots'] for row in rows)}
