from pathlib import Path
import re

PUBLIC_CSS = Path('program-agenda/assets/css/public.css')
text = PUBLIC_CSS.read_text()

# Repair a malformed date-tab declaration that can happen during manual CSS
# edits. The stray `};` closes the .pa-agenda-day-tab rule early and makes the
# brace-balance check fail. Also normalize the date-tab/datebar override to
# Montserrat instead of Arial.
text = text.replace(
    '  font-family: Arial, Helvetica, sans-serif;};\n  line-height:1.1;',
    '  font-family: Montserrat, Arial, Helvetica, sans-serif;\n  line-height:1.1;',
)
text = text.replace(
    '  font-family:Arial, Helvetica, sans-serif;};\n  line-height:1.1;',
    '  font-family:Montserrat, Arial, Helvetica, sans-serif;\n  line-height:1.1;',
)
text = text.replace('font-family: Arial, Helvetica, sans-serif;', 'font-family: Montserrat, Arial, Helvetica, sans-serif;')
text = text.replace('font-family:Arial, Helvetica, sans-serif;', 'font-family:Montserrat, Arial, Helvetica, sans-serif;')

# The custom event-card hover media query was missing its closing brace, which
# caused the rest of the event-card rules to be scoped to mobile widths and
# could also knock sponsor logo sizing out of place. Replace that media block
# with a complete, closed block.
fixed_mobile_block = '''@media (max-width: 768px) {
  .pa-event-card .pa-event-card__datebar::before {
    width: 100% !important;
    transition: none !important;
  }

  .pa-event-card:hover .pa-event-card__datebar::before,
  .pa-event-card:focus-within .pa-event-card__datebar::before {
    width: 100% !important;
  }

  .pa-event-card .pa-event-card__body {
    transition: none !important;
  }

  .pa-event-card:hover .pa-event-card__body,
  .pa-event-card:focus-within .pa-event-card__body {
    padding-left: 28px !important;
  }
}

'''

pattern = re.compile(
    r'@media \(max-width: 768px\) \{\n'
    r'  \.pa-event-card \.pa-event-card__datebar::before \{\n'
    r'    width: 100% !important;\n'
    r'    transition: none !important;\n'
    r'  \}\n\n'
    r'  \.pa-event-card:hover \.pa-event-card__datebar::before,\n'
    r'  \.pa-event-card:focus-within \.pa-event-card__datebar::before \{\n'
    r'    width: 100% !important;\n'
    r'  \}\n\n'
    r'  \.pa-event-card \.pa-event-card__body \{\n'
    r'    transition: none !important;\n'
    r'  \}\n\n'
    r'  \.pa-event-card:hover \.pa-event-card__body,\n'
    r'  \.pa-event-card:focus-within \.pa-event-card__body \{\n'
    r'    padding-left: 28px !important;\n'
    r'  \}\n\n'
    r'(?=\.pa-event-card::after\{)'
)
text, count = pattern.subn(fixed_mobile_block, text, count=1)

# Keep the event hover effect off on smaller screens, including after the later
# consolidated mobile card rules. This prevents overlap on phones/tablets.
mobile_safety = '''
@media (max-width:768px){
  .pa-event-card .pa-event-card__datebar::before,
  .pa-event-card:hover .pa-event-card__datebar::before,
  .pa-event-card:focus-within .pa-event-card__datebar::before{
    width:100%!important;
    transition:none!important;
  }
  .pa-event-card .pa-event-card__body,
  .pa-event-card:hover .pa-event-card__body,
  .pa-event-card:focus-within .pa-event-card__body{
    transition:none!important;
  }
  .pa-event-card:hover .pa-event-card__body,
  .pa-event-card:focus-within .pa-event-card__body{
    padding-left:18px!important;
  }
  .pa-event-card.pa-event-card--size-thin:hover .pa-event-card__body,
  .pa-event-card.pa-event-card--size-thin:focus-within .pa-event-card__body{
    padding-left:14px!important;
  }
}
'''
if '/* Stagecard responsive hover safety */' not in text:
    text += '\n/* Stagecard responsive hover safety */' + mobile_safety

# Safari can repeatedly recalculate percentage-based grid child heights on
# hover. Keep the children stretched by grid instead of using calc(100% + 4px).
safari_height_guard = '''
/* Stagecard Safari event card height guard */
.pa-event-card .pa-event-card__datebar,
.pa-event-card .pa-event-card__body{
  height:auto!important;
  min-height:0!important;
  top:auto!important;
  bottom:auto!important;
  align-self:stretch!important;
}
.pa-event-card .pa-event-card__datebar{
  left:0!important;
  right:auto!important;
  width:calc(100% + 4px)!important;
}
.pa-event-card .pa-event-card__body{
  right:auto!important;
  width:100%!important;
  max-width:100%!important;
}
'''
if '/* Stagecard Safari event card height guard */' not in text:
    text += '\n' + safari_height_guard

# Hard cap sponsor logos in case a theme or malformed earlier CSS tries to make
# images render at their source dimensions.
sponsor_guard = '''
/* Stagecard sponsor logo sizing guard */
.pa-sponsor-showcase-logo-img,
.pa-event-sponsor-logo-img{
  display:block!important;
  max-width:250px!important;
  max-height:150px!important;
  width:auto!important;
  height:auto!important;
  object-fit:contain!important;
}
.pa-sponsor-showcase-logo,
.pa-sponsor-showcase-name{
  width:250px!important;
  height:150px!important;
  min-height:150px!important;
}
.pa-sponsor-hero-logo-img{
  display:block!important;
  max-width:100%!important;
  max-height:100%!important;
  width:auto!important;
  height:auto!important;
  object-fit:contain!important;
}
'''
if '/* Stagecard sponsor logo sizing guard */' not in text:
    text += '\n' + sponsor_guard

# Basic sanity check: public.css should not have an obvious unbalanced brace
# after this script runs.
balance = 0
for i, char in enumerate(text):
    if char == '{':
        balance += 1
    elif char == '}':
        balance -= 1
    if balance < 0:
        raise SystemExit(f'CSS brace balance went negative near character {i}.')
if balance != 0:
    raise SystemExit(f'CSS brace balance is {balance}, expected 0.')

PUBLIC_CSS.write_text(text)
print('Fixed malformed agenda tab CSS, normalized date fonts to Montserrat, event-card mobile media query, Safari height guard, and sponsor logo sizing guard.')
