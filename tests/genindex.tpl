{%- macro kana_entry(kname) -%}
{%- if kname is string -%}
{{ kname|e }}
{%- else %}
{%- for isruby, val in kname -%}
{%- if isruby -%}
|{{ val[0]|e }}《{{ val[1]|e }}》
{%- else -%}
{{ val|e }}
{%- endif -%}
{%- endfor -%}
{%- endif -%}
{%- endmacro -%}

{%- macro indexentries(firstname, links) -%}
{%- if links -%}
{%- if links[0][0] %}!{% endif -%}
{{ kana_entry(firstname) }}/{{ links[0][1] }}
{%- for ismain, link in links[1:] -%}
, {%- if ismain -%}!{%- endif -%}
[{{ loop.index }}]/{{ link }}
{%- endfor -%}
{%- else -%}
{{ kana_entry(firstname) }}
{%- endif -%}
{%- endmacro -%}

{%- block body -%}
{%- for key, dummy in genindex -%}
{{ key }}
{%- if not loop.last %}| {%- endif -%}
{%- endfor -%}
{%- for key, entries in genindexentries -%}
[{{ key }}]
{% for entryname, (links, subitems, _) in entries -%}
term: {{ indexentries(entryname, links) }}
{% if subitems -%}
{% for subentryname, subentrylinks in subitems -%}
sub: {{ indexentries(subentryname, subentrylinks) }}
{% endfor -%}
{%- endif -%}
{% endfor -%}
{% endfor -%}
{%- endblock -%}
