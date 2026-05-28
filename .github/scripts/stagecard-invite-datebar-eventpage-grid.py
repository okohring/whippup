from pathlib import Path
import re

PHP = Path('program-agenda/program-agenda.php')
PUBLIC_CSS = Path('program-agenda/assets/css/public.css')

php = PHP.read_text()

# Move the invite-only envelope out of the event-card meta row and into the
# accent/date bar, directly below the time.
old_datebar = """        ob_start();
        echo '<article class="' . esc_attr(implode(' ', $card_classes)) . '" style="' . esc_attr($item_style) . '">';
        echo '<div class="pa-event-card__datebar"><span class="pa-event-card__date">' . esc_html($date_text ?: 'Date') . '</span><span class="pa-event-card__time">' . esc_html($time_text ?: 'Time') . '</span></div>';
"""
old_datebar_with_icon_above_time = """        $invite_icon_html = $invite_only ? '<span class="pa-event-card__invite-wrap pa-event-card__datebar-invite-wrap"><span class="pa-event-card__invite-icon" aria-label="Invite only" tabindex="0"><svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M3.75 6.75h16.5v10.5H3.75V6.75Zm1.5 1.4v7.7h13.5v-7.7L12 12.9 5.25 8.15Zm12.38.1H6.37L12 12.1l5.63-3.85Z" fill="currentColor"/></svg></span><span class="pa-invite-tooltip" role="tooltip"><span class="pa-invite-tooltip-inner"><span>Invite only</span></span></span></span>' : '';

        ob_start();
        echo '<article class="' . esc_attr(implode(' ', $card_classes)) . '" style="' . esc_attr($item_style) . '">';
        echo '<div class="pa-event-card__datebar"><span class="pa-event-card__date">' . esc_html($date_text ?: 'Date') . '</span>' . $invite_icon_html . '<span class="pa-event-card__time">' . esc_html($time_text ?: 'Time') . '</span></div>';
"""
new_datebar = """        $invite_icon_html = $invite_only ? '<span class="pa-event-card__invite-wrap pa-event-card__datebar-invite-wrap"><span class="pa-event-card__invite-icon" aria-label="Invite only" tabindex="0"><svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M3.75 6.75h16.5v10.5H3.75V6.75Zm1.5 1.4v7.7h13.5v-7.7L12 12.9 5.25 8.15Zm12.38.1H6.37L12 12.1l5.63-3.85Z" fill="currentColor"/></svg></span><span class="pa-invite-tooltip" role="tooltip"><span class="pa-invite-tooltip-inner"><span>Invite only</span></span></span></span>' : '';

        ob_start();
        echo '<article class="' . esc_attr(implode(' ', $card_classes)) . '" style="' . esc_attr($item_style) . '">';
        echo '<div class="pa-event-card__datebar"><span class="pa-event-card__date">' . esc_html($date_text ?: 'Date') . '</span><span class="pa-event-card__time">' . esc_html($time_text ?: 'Time') . '</span>' . $invite_icon_html . '</div>';
"""
if old_datebar_with_icon_above_time in php:
    php = php.replace(old_datebar_with_icon_above_time, new_datebar, 1)
elif old_datebar in php:
    php = php.replace(old_datebar, new_datebar, 1)
elif '$invite_icon_html = $invite_only ?' not in php:
    raise SystemExit('Could not find agenda_event_card datebar output block.')

php = php.replace("        if ($cat || $loc || $invite_only) {\n", "        if ($cat || $loc) {\n")
php = php.replace("            if (($cat || $loc) && $invite_only) { echo '<span class=\"pa-event-card__meta-dot\" aria-hidden=\"true\">•</span>'; }\n            if ($invite_only) { echo '<span class=\"pa-event-card__invite-wrap\"><span class=\"pa-event-card__invite-icon\" aria-label=\"Invite only\" tabindex=\"0\"><svg viewBox=\"0 0 24 24\" aria-hidden=\"true\" focusable=\"false\"><path d=\"M3.75 6.75h16.5v10.5H3.75V6.75Zm1.5 1.4v7.7h13.5v-7.7L12 12.9 5.25 8.15Zm12.38.1H6.37L12 12.1l5.63-3.85Z\" fill=\"currentColor\"/></svg></span><span class=\"pa-invite-tooltip\" role=\"tooltip\"><span class=\"pa-invite-tooltip-inner\"><span>Invite only</span></span></span></span>'; }\n", "")

PHP.write_text(php)

css = PUBLIC_CSS.read_text()

# Remove earlier versions of this block so the cleanup remains idempotent.
css = re.sub(r'\n?/\* Stagecard invite icon datebar and Event page speaker grid \*/.*?(?=\n/\* Stagecard |\Z)', '\n', css, flags=re.S)

block = '''
/* Stagecard invite icon datebar and Event page speaker grid */
.pa-event-card__datebar .pa-event-card__datebar-invite-wrap{
  display:inline-flex!important;
  align-items:center!important;
  justify-content:center!important;
  margin:2px 0 0!important;
  padding:0!important;
  line-height:1!important;
  position:relative!important;
}
.pa-event-card__datebar .pa-event-card__invite-icon{
  display:inline-flex!important;
  align-items:center!important;
  justify-content:center!important;
  width:1em!important;
  height:1em!important;
  color:inherit!important;
  line-height:1!important;
}
.pa-event-card__datebar .pa-event-card__invite-icon svg{
  display:block!important;
  width:100%!important;
  height:100%!important;
}
.pa-single-event-speaker-sections{
  display:grid!important;
  grid-template-columns:1fr!important;
  gap:28px!important;
}
.pa-single-event-speaker-section-list--categorized,
.pa-single-event-speaker-section--default{
  order:initial!important;
  border:0!important;
  border-left:0!important;
  border-top:0!important;
  padding:0!important;
  margin:0!important;
}
.pa-single-event-speaker-section-list--categorized{
  order:1!important;
}
.pa-single-event-speaker-section--default{
  order:2!important;
}
.pa-single-event-speaker-sections .pa-single-event-speaker-section .pa-speaker-card-list{
  display:grid!important;
  grid-template-columns:1fr!important;
  gap:12px!important;
  align-items:start!important;
  justify-items:start!important;
}
.pa-single-event-speaker-sections .pa-single-event-speaker-section .pa-speaker-card{
  width:min(230px,100%)!important;
  max-width:230px!important;
  min-width:0!important;
  grid-template-columns:40px minmax(0,1fr)!important;
}
@media (max-width:900px){
  .pa-single-event-speaker-sections{
    grid-template-columns:1fr!important;
  }
  .pa-single-event-speaker-sections .pa-single-event-speaker-section .pa-speaker-card{
    width:min(230px,100%)!important;
    max-width:100%!important;
  }
}
'''
css = css.rstrip() + '\n\n' + block.strip() + '\n'
PUBLIC_CSS.write_text(css)

print('Moved invite icon below time and stacked Event page moderator section above speakers section.')
