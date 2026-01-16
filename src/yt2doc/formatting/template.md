# {{ title }}

{{ video_url }}
{%- if add_table_of_contents %}

### {% if language_code == "zh" %}目錄{% else %}Table of contents{% endif %}
{%- for chapter in chapters %}
- {{ chapter.start_h_m_s }} [{{ chapter.title }}](#{{chapter.custom_id}})
  {%- for paragraph in chapter.toc_paragraphs %}
  - {{ paragraph.start_h_m_s }} [{{ paragraph.text }}](#{{ paragraph.custom_id }})
  {%- endfor %}
{%- endfor %}
{%- endif %}
{%- for chapter in chapters %}

## {{ chapter.title }}{%if add_table_of_contents %}<a name="{{chapter.custom_id}}"></a>{% endif %}{% for paragraph in chapter.paragraphs %}

{% if to_timestamp_paragraphs %}({{ paragraph.start_h_m_s }}) {% endif %}{% if add_table_of_contents %}<a name="{{ paragraph.custom_id }}"></a>{% endif %}{{ paragraph.text }}
{%- endfor %}
{%- endfor %}
