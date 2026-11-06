[Header / cover block]
{{ project_title }}       Version: {{ version }}

# Schedule Management

## Milestones
[Table — 4 cols]
| Subproject | Milestone | Delivery Date | Status |
|------------|-----------|---------------|--------|
{% for m in milestones %}
| {{ m.subproject }} | {{ m.milestone }} | {{ m.delivery_date }} | {{ m.status }} |
{% endfor %}


## Deliverables
[Table — 5 cols]
| Subproject | Deliverable Name | Due Date | Date Updated | Status |
|------------|-----------------|----------|--------------|--------|
{% for d in deliverables %}
| {{ d.subproject }} | {{ d.deliverable_name }} | {{ d.due_date }} | {{ d.date_updated }} | {{ d.status }} |
{% endfor %}
