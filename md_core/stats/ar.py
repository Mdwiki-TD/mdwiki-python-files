"""

from stats.ar import get_ar_results

"""

from api_sql import wiki_sql


def get_ar_results():
    qua = """
    SELECT actor_name, count(*) as count from revision
        join actor on rev_actor = actor_id
        join page on rev_page = page_id
        WHERE lower(cast(actor_name as CHAR)) NOT LIKE '%bot%' AND page_namespace = 0 AND rev_timestamp like '2023%'
        and page_id in (
        select DISTINCT pa_page_id
        from page_assessments, page_assessments_projects
        where pa_project_id = pap_project_id
        and pap_project_title = "طب"
        )
        group by actor_id
        order by count(*) desc
    limit 100;
    """
    # ---
    editors = {}
    # ---
    result = wiki_sql.sql_new(qua, "arwiki")
    # ---
    for x in result:
        # ---
        actor_name = x["actor_name"]
        # ---
        if actor_name not in editors:
            editors[actor_name] = 0
        # ---
        editors[actor_name] += x["count"]
        # ---
    # ---
    return editors
