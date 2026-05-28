from pathlib import Path
import re

PUBLIC_CSS = Path('program-agenda/assets/css/public.css')
text = PUBLIC_CSS.read_text()

# Remove prior experimental speaker-card normalization blocks. They were too broad
# and could alter agenda cards instead of only making Event-page cards match them.
markers_to_remove = [
    'Stagecard event page speaker card compact text',
    'Stagecard speaker card consistency and compact spacing',
    'Stagecard universal speaker card component source of truth',
    'Stagecard Event page speaker cards match agenda cards',
    'Stagecard Montserrat event and speaker card font',
]
for marker in markers_to_remove:
    text = re.sub(r'\n?/\* ' + re.escape(marker) + r' \*/.*?(?=\n/\* Stagecard |\Z)', '\n', text, flags=re.S)

# Source of truth: leave agenda cards alone, then make the individual Event-page
# speaker cards use the same sizing/typography as the agenda speaker cards.
css = '''
/* Stagecard Event page speaker cards match agenda cards */
.pa-single-event .pa-single-event-speaker-section .pa-speaker-card,
.pa-single-event .pa-event-single-speakers .pa-speaker-card{
  box-sizing:border-box!important;
  display:flex!important;
  align-items:center!important;
  gap:.75rem!important;
  padding:.72rem!important;
  border-radius:.35rem!important;
  font-size:.7rem!important;
  line-height:1!important;
  min-width:0!important;
  max-width:100%!important;
}
.pa-single-event .pa-single-event-speaker-section .pa-speaker-card-image,
.pa-single-event .pa-event-single-speakers .pa-speaker-card-image{
  width:40px!important;
  height:40px!important;
  min-width:40px!important;
  max-width:40px!important;
  min-height:40px!important;
  max-height:40px!important;
  flex:0 0 40px!important;
}
.pa-single-event .pa-single-event-speaker-section .pa-speaker-card-thumb,
.pa-single-event .pa-single-event-speaker-section .pa-speaker-card-image img,
.pa-single-event .pa-event-single-speakers .pa-speaker-card-thumb,
.pa-single-event .pa-event-single-speakers .pa-speaker-card-image img{
  width:100%!important;
  height:100%!important;
  max-width:100%!important;
  max-height:100%!important;
  object-fit:cover!important;
  display:block!important;
}
.pa-single-event .pa-single-event-speaker-section .pa-speaker-card-text,
.pa-single-event .pa-event-single-speakers .pa-speaker-card-text{
  min-width:0!important;
  max-width:100%!important;
  padding-right:18px!important;
}
.pa-single-event .pa-single-event-speaker-section .pa-speaker-card-text h3,
.pa-single-event .pa-single-event-speaker-section .pa-speaker-card-text h3 a,
.pa-single-event .pa-single-event-speaker-section .pa-speaker-card-text p,
.pa-single-event .pa-event-single-speakers .pa-speaker-card-text h3,
.pa-single-event .pa-event-single-speakers .pa-speaker-card-text h3 a,
.pa-single-event .pa-event-single-speakers .pa-speaker-card-text p{
  font-size:.7rem!important;
  line-height:1!important;
  margin-top:2px!important;
  margin-bottom:2px!important;
}
.pa-single-event .pa-single-event-speaker-section .pa-speaker-card-list,
.pa-single-event .pa-event-single-speakers .pa-speaker-card-list{
  margin-top:0!important;
  gap:.75rem!important;
}
'''

font_css = '''
/* Stagecard Montserrat event and speaker card font */
.pa-event-card,
.pa-event-card :where(h1,h2,h3,h4,h5,h6,p,span,a,button,small,strong,em,li),
.pa-speaker-card,
.pa-speaker-card :where(h1,h2,h3,h4,h5,h6,p,span,a,small,strong,em,li),
.pa-single-event-speaker-sections,
.pa-single-event-speaker-sections :where(h1,h2,h3,h4,h5,h6,p,span,a,small,strong,em,li),
.pa-event-single-speakers,
.pa-event-single-speakers :where(h1,h2,h3,h4,h5,h6,p,span,a,small,strong,em,li){
  font-family:Montserrat, Arial, Helvetica, sans-serif!important;
}
'''

text = text.rstrip() + '\n\n' + css.strip() + '\n\n' + font_css.strip() + '\n'
PUBLIC_CSS.write_text(text)
print('Made individual Event page speaker cards match agenda-card speaker styling and applied Montserrat to event/speaker cards.')
