from pathlib import Path
import re

PHP = Path('program-agenda/program-agenda.php')
PUBLIC_CSS = Path('program-agenda/assets/css/public.css')

php = PHP.read_text()
old = "        wp_enqueue_style('pa-public', plugin_dir_url(__FILE__) . 'assets/css/public.css', [], self::VERSION);\n"
new = "        wp_enqueue_style('pa-montserrat', 'https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;500;600;700&display=swap', [], null);\n" + old
if "wp_enqueue_style('pa-montserrat'" not in php:
    if old not in php:
        raise SystemExit('Could not find public stylesheet enqueue marker.')
    php = php.replace(old, new, 1)
PHP.write_text(php)

css = PUBLIC_CSS.read_text()
# Remove older font-only blocks so the final one is the source of truth.
for marker in [
    'Stagecard Montserrat event and speaker card font',
    'Stagecard force lighter Montserrat weights',
    'Stagecard reduce event/speaker card boldness',
    'Stagecard event and speaker card font weights',
]:
    css = re.sub(r'\n?/\* ' + re.escape(marker) + r' \*/.*?(?=\n/\* Stagecard |\Z)', '\n', css, flags=re.S)

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
  font-synthesis-weight:none!important;
}
.pa-event-card .pa-event-card__title,
.pa-event-card .pa-event-card__title a,
.pa-speaker-card .pa-speaker-card-text h3,
.pa-speaker-card .pa-speaker-card-text h3 a{
  font-weight:500!important;
  font-variation-settings:"wght" 500!important;
}
.pa-event-card .pa-event-card__meta,
.pa-event-card .pa-event-card__meta *,
.pa-speaker-card .pa-speaker-card-role,
.pa-speaker-card .pa-speaker-card-company{
  font-weight:400!important;
  font-variation-settings:"wght" 400!important;
}
.pa-event-card .pa-event-card__date,
.pa-event-card .pa-event-card__time,
.pa-event-card .pa-speaker-card-category-label,
.pa-single-event-speaker-section-heading{
  font-weight:500!important;
  font-variation-settings:"wght" 500!important;
}
'''
css = css.rstrip() + '\n\n' + font_css.strip() + '\n'
PUBLIC_CSS.write_text(css)
print('Enqueued Montserrat weights and applied Montserrat font/weight rules to event and speaker cards.')
