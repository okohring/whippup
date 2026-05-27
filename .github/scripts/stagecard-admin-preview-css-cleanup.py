from pathlib import Path
import re

ADMIN = Path('program-agenda/assets/css/admin.css')
JS = Path('program-agenda/assets/js/admin.js')
PHP = Path('program-agenda/program-agenda.php')


def remove_block(text, start_marker, end_marker=None):
    start = text.find(start_marker)
    if start == -1:
        return text
    if end_marker is None:
        return text[:start].rstrip() + '\n'
    end = text.find(end_marker, start + len(start_marker))
    if end == -1:
        return text[:start].rstrip() + '\n'
    return text[:start].rstrip() + '\n\n' + text[end:].lstrip()

admin = ADMIN.read_text()

# Remove the legacy preview component copy. It contained its own hover-width variable,
# grid-template-columns hover transition, and old slant animation selectors.
admin = remove_block(
    admin,
    '/* v1.15.117: admin Event Card preview now uses the same dummy component/classes as public cards. */',
    '/* v1.15.118: reorderable sponsor levels */'
)

# Remove later preview patch layers so there is one final preview system only.
admin = remove_block(admin, '/* v1.15.160: admin event-card preview matches stable public hover and border behavior */', '/* v1.15.161: static simple previews with color lines */')
admin = remove_block(admin, '/* v1.15.161: static simple previews with color lines */', '/* Stagecard final admin preview system */')
admin = remove_block(admin, '/* Stagecard final admin preview system */')

final_admin = r'''

/* Stagecard final admin preview system */
.pa-combined-preview-section .pa-event-card-preview,
.pa-combined-preview-section .pa-event-card-preview:hover,
.pa-combined-preview-section .pa-event-card-preview:focus-within,
.pa-event-card-preview,
.pa-event-card-preview:hover,
.pa-event-card-preview:focus-within{
  transform:none!important;
  transition:none!important;
  --pa-event-card-datebar-width:64px!important;
  grid-template-columns:64px minmax(0,1fr)!important;
}
.pa-combined-preview-section .pa-event-card-preview.pa-event-card--size-full,
.pa-combined-preview-section .pa-event-card-preview.pa-event-card--size-full:hover,
.pa-combined-preview-section .pa-event-card-preview.pa-event-card--size-full:focus-within,
.pa-event-card-preview.pa-event-card--size-full,
.pa-event-card-preview.pa-event-card--size-full:hover,
.pa-event-card-preview.pa-event-card--size-full:focus-within{
  --pa-event-card-datebar-width:64px!important;
  grid-template-columns:64px minmax(0,1fr)!important;
}
.pa-combined-preview-section .pa-event-card-preview.pa-event-card--size-thin,
.pa-combined-preview-section .pa-event-card-preview.pa-event-card--size-thin:hover,
.pa-combined-preview-section .pa-event-card-preview.pa-event-card--size-thin:focus-within,
.pa-event-card-preview.pa-event-card--size-thin,
.pa-event-card-preview.pa-event-card--size-thin:hover,
.pa-event-card-preview.pa-event-card--size-thin:focus-within{
  --pa-event-card-datebar-width:56px!important;
  grid-template-columns:56px minmax(0,1fr)!important;
}
.pa-combined-preview-section .pa-event-card-preview .pa-event-card__datebar,
.pa-combined-preview-section .pa-event-card-preview:hover .pa-event-card__datebar,
.pa-combined-preview-section .pa-event-card-preview:focus-within .pa-event-card__datebar,
.pa-event-card-preview .pa-event-card__datebar,
.pa-event-card-preview:hover .pa-event-card__datebar,
.pa-event-card-preview:focus-within .pa-event-card__datebar{
  clip-path:none!important;
  transform:none!important;
  transition:none!important;
}
.pa-combined-preview-section .pa-event-card-preview .pa-event-card__datebar::before,
.pa-combined-preview-section .pa-event-card-preview .pa-event-card__datebar::after,
.pa-event-card-preview .pa-event-card__datebar::before,
.pa-event-card-preview .pa-event-card__datebar::after{
  content:none!important;
  display:none!important;
}
.pa-preview-line{
  display:block;
  height:8px;
  border-radius:999px;
  background:currentColor;
  opacity:.9;
}
.pa-preview-line + .pa-preview-line{margin-top:10px;}
.pa-preview-line-title{width:120px;height:8px;}
.pa-preview-line-short{width:65px;height:6px;}
.pa-preview-line-medium{width:130px;height:6px;}
.pa-preview-line-heading{width:180px;height:10px;}
.pa-preview-line-subheading{width:130px;height:7px;}
.pa-preview-line-content{width:min(360px,100%);height:7px;}
.pa-preview-line-speaker-name{width:95px;height:7px;}
.pa-preview-line-speaker-role{width:75px;height:5px;opacity:.75;}
.pa-preview-line-speaker-company{width:88px;height:5px;opacity:.75;}
.pa-preview-content{display:grid;gap:12px;}
.pa-program-page-preview-card .pa-single-content .pa-preview-line-content{width:min(360px,100%);}
'''

admin = admin.rstrip() + final_admin
admin = re.sub(r'\n{3,}', '\n\n', admin).rstrip() + '\n'
ADMIN.write_text(admin)

# Make sure JS cannot restore removed hover classes.
js = JS.read_text()
js = js.replace("    var hoverAnim=$('[name=\"agenda[hover_animation]\"]').val() || 'default'; if(hoverAnim !== 'slant') hoverAnim = 'default';\n    $p.removeClass('pa-event-card--hover-default pa-event-card--hover-slant').addClass('pa-event-card--hover-'+hoverAnim);\n", "    $p.removeClass('pa-event-card--hover-default pa-event-card--hover-slant');\n")
js = js.replace("$('[name=\"agenda[hover_animation]\"]').val('default');", "")
js = js.replace("$('[name=\"agenda[hover_animation]\"]').val(ag.hover_animation || 'default');", "")
JS.write_text(js)

php = PHP.read_text()
php = php.replace(' pa-event-card--hover-default', '')
php = php.replace(' pa-event-card--hover-slant', '')
PHP.write_text(php)

print('Admin preview CSS cleanup complete.')
