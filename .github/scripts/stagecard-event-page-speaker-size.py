from pathlib import Path

PUBLIC_CSS = Path('program-agenda/assets/css/public.css')
text = PUBLIC_CSS.read_text()

css = '''
/* Stagecard event page speaker card compact text */
.pa-single-event-speaker-section .pa-speaker-card,
.pa-event-single-speakers .pa-speaker-card{
  font-size:.72rem!important;
  line-height:1.12!important;
}
.pa-single-event-speaker-section .pa-speaker-card-text h3,
.pa-single-event-speaker-section .pa-speaker-card-text h3 a,
.pa-event-single-speakers .pa-speaker-card-text h3,
.pa-event-single-speakers .pa-speaker-card-text h3 a{
  font-size:.76rem!important;
  line-height:1.08!important;
  margin:0 0 1px!important;
}
.pa-single-event-speaker-section .pa-speaker-card-role,
.pa-single-event-speaker-section .pa-speaker-card-company,
.pa-event-single-speakers .pa-speaker-card-role,
.pa-event-single-speakers .pa-speaker-card-company{
  font-size:.68rem!important;
  line-height:1.12!important;
  margin:0!important;
}
'''

if '/* Stagecard event page speaker card compact text */' not in text:
    text += '\n' + css

PUBLIC_CSS.write_text(text)
print('Applied compact text sizing for Event page speaker cards.')
