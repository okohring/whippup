from pathlib import Path
import re

PUBLIC_CSS = Path('program-agenda/assets/css/public.css')
text = PUBLIC_CSS.read_text()

# Remove older one-off speaker-card fixes that made Event page cards differ from
# agenda cards. This script runs late in the cleanup workflow, so the block below
# becomes the source of truth for speaker cards everywhere they are rendered.
markers_to_remove = [
    'Stagecard event page speaker card compact text',
    'Stagecard speaker card consistency and compact spacing',
]
for marker in markers_to_remove:
    text = re.sub(r'\n?/\* ' + re.escape(marker) + r' \*/.*?(?=\n/\* Stagecard |\Z)', '\n', text, flags=re.S)

css = '''
/* Stagecard universal speaker card component source of truth */
:where(.pa-event-card,.pa-single-event,.pa-speaker-upcoming-events) .pa-speaker-card-list,
:where(.pa-event-card,.pa-single-event,.pa-speaker-upcoming-events) .pa-speaker-card-list-agenda{
  gap:.75rem!important;
  margin-top:0!important;
}
:where(.pa-event-card,.pa-single-event,.pa-speaker-upcoming-events) .pa-speaker-card,
:where(.pa-event-card,.pa-single-event,.pa-speaker-upcoming-events) .pa-speaker-card.pa-speaker-card--categorized{
  box-sizing:border-box!important;
  display:flex!important;
  align-items:center!important;
  gap:.75rem!important;
  padding:.72rem!important;
  border-radius:.35rem!important;
  font-size:.7rem!important;
  line-height:1.12!important;
  min-width:0!important;
  max-width:100%!important;
}
:where(.pa-event-card,.pa-single-event,.pa-speaker-upcoming-events) .pa-speaker-card-image{
  width:40px!important;
  height:40px!important;
  min-width:40px!important;
  max-width:40px!important;
  min-height:40px!important;
  max-height:40px!important;
  flex:0 0 40px!important;
}
:where(.pa-event-card,.pa-single-event,.pa-speaker-upcoming-events) .pa-speaker-card-thumb,
:where(.pa-event-card,.pa-single-event,.pa-speaker-upcoming-events) .pa-speaker-card-image img{
  width:100%!important;
  height:100%!important;
  max-width:100%!important;
  max-height:100%!important;
  object-fit:cover!important;
  display:block!important;
}
:where(.pa-event-card,.pa-single-event,.pa-speaker-upcoming-events) .pa-speaker-card-text{
  min-width:0!important;
  max-width:100%!important;
  padding-right:0!important;
}
:where(.pa-event-card,.pa-single-event,.pa-speaker-upcoming-events) .pa-speaker-card-text h3,
:where(.pa-event-card,.pa-single-event,.pa-speaker-upcoming-events) .pa-speaker-card-text h3 a{
  font-size:.7rem!important;
  line-height:1.08!important;
  margin:0 0 2px!important;
  padding:0!important;
}
:where(.pa-event-card,.pa-single-event,.pa-speaker-upcoming-events) .pa-speaker-card-role,
:where(.pa-event-card,.pa-single-event,.pa-speaker-upcoming-events) .pa-speaker-card-company{
  font-size:.7rem!important;
  line-height:1.08!important;
  margin:0!important;
  padding:0!important;
}
.pa-event-card .pa-event-card__speakers{
  margin-top:0!important;
}
.pa-event-card .pa-speaker-card-unit{
  padding-top:0!important;
  gap:3px!important;
}
.pa-event-card .pa-speaker-card-category-label{
  margin:0 0 3px!important;
  line-height:1.05!important;
}
@media (max-width:768px){
  .pa-event-card .pa-event-card__speakers{margin-top:0!important;}
  .pa-event-card .pa-speaker-card-unit{padding-top:0!important;}
}
'''

if '/* Stagecard universal speaker card component source of truth */' not in text:
    text = text.rstrip() + '\n\n' + css.strip() + '\n'
else:
    text = re.sub(r'/\* Stagecard universal speaker card component source of truth \*/.*?\Z', css.strip() + '\n', text, flags=re.S)

PUBLIC_CSS.write_text(text)
print('Enforced universal speaker card component styling across agenda, Event pages, and speaker upcoming-event cards.')
