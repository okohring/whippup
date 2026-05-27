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

/* Stagecard final admin preview system: clean public-card clone, static placeholders */
.pa-combined-preview-section .pa-event-card-preview{
  --pa-event-card-datebar-width:64px!important;
  --pa-event-card-border-color:color-mix(in srgb,currentColor 18%,transparent);
  box-sizing:border-box!important;
  display:grid!important;
  grid-template-columns:64px minmax(0,1fr)!important;
  grid-auto-rows:1fr!important;
  width:100%!important;
  max-width:900px!important;
  min-height:118px!important;
  margin-top:20px!important;
  position:relative!important;
  overflow:hidden!important;
  isolation:isolate!important;
  background:var(--pa-agenda-card-bg,#fff)!important;
  background-color:var(--pa-agenda-card-bg,#fff)!important;
  color:inherit!important;
  border:0!important;
  gap:0!important;
  border-spacing:0!important;
  transform:none!important;
  transition:none!important;
}
.pa-combined-preview-section .pa-event-card-preview:hover,
.pa-combined-preview-section .pa-event-card-preview:focus-within{
  grid-template-columns:64px minmax(0,1fr)!important;
  transform:none!important;
  transition:none!important;
}
.pa-combined-preview-section .pa-event-card-preview::after{
  content:""!important;
  display:block!important;
  position:absolute!important;
  inset:0!important;
  pointer-events:none!important;
  z-index:10!important;
  border:1px solid var(--pa-event-card-border-color)!important;
  border-radius:inherit!important;
  box-sizing:border-box!important;
}
.pa-combined-preview-section .pa-event-card-preview .pa-event-card__datebar{
  box-sizing:border-box!important;
  grid-column:1!important;
  grid-row:1!important;
  position:relative!important;
  z-index:1!important;
  top:-2px!important;
  left:-2px!important;
  width:calc(100% + 4px)!important;
  height:calc(100% + 4px)!important;
  min-height:calc(100% + 4px)!important;
  margin:0!important;
  background:var(--pa-agenda-bar-color,#1d2327)!important;
  background-color:var(--pa-agenda-bar-color,#1d2327)!important;
  color:#fff!important;
  display:flex!important;
  flex-direction:column!important;
  align-items:center!important;
  justify-content:center!important;
  gap:4px!important;
  padding:14px 12px!important;
  text-align:center!important;
  overflow:hidden!important;
  box-shadow:1px 0 0 var(--pa-agenda-bar-color,#1d2327)!important;
  transform:none!important;
  transition:none!important;
}
.pa-combined-preview-section .pa-event-card-preview:hover .pa-event-card__datebar,
.pa-combined-preview-section .pa-event-card-preview:focus-within .pa-event-card__datebar{
  clip-path:none!important;
  transform:none!important;
  transition:none!important;
}
.pa-combined-preview-section .pa-event-card-preview .pa-event-card__datebar::before,
.pa-combined-preview-section .pa-event-card-preview .pa-event-card__datebar::after{
  content:none!important;
  display:none!important;
}
.pa-combined-preview-section .pa-event-card-preview .pa-event-card__date,
.pa-combined-preview-section .pa-event-card-preview .pa-event-card__time{
  display:block!important;
  margin:0!important;
  padding:0!important;
  font-size:.78rem!important;
  line-height:1.1!important;
  text-transform:uppercase!important;
  white-space:nowrap!important;
}
.pa-combined-preview-section .pa-event-card-preview .pa-event-card__body{
  box-sizing:border-box!important;
  grid-column:2!important;
  grid-row:1!important;
  position:relative!important;
  z-index:2!important;
  top:-2px!important;
  right:-2px!important;
  width:calc(100% + 4px)!important;
  height:calc(100% + 4px)!important;
  min-height:calc(100% + 4px)!important;
  margin:0!important;
  min-width:0!important;
  max-width:100%!important;
  padding:20px 28px!important;
  display:flex!important;
  flex-direction:column!important;
  justify-content:center!important;
  align-items:flex-start!important;
  text-align:left!important;
  overflow:hidden!important;
  background:var(--pa-agenda-card-bg,#fff)!important;
  background-color:var(--pa-agenda-card-bg,#fff)!important;
  transform:translateZ(0)!important;
}
.pa-combined-preview-section .pa-event-card-preview .pa-event-card__summary{
  box-sizing:border-box!important;
  display:block!important;
  width:100%!important;
  min-width:0!important;
  max-width:100%!important;
  margin:0!important;
  padding:0!important;
  text-align:left!important;
}
.pa-combined-preview-section .pa-event-card-preview .pa-event-card__title,
.pa-combined-preview-section .pa-event-card-preview .pa-event-card__title a{
  display:block!important;
  margin:0!important;
  padding:0!important;
  line-height:1.15!important;
  color:var(--pa-agenda-title-color,inherit)!important;
  text-align:left!important;
  white-space:normal!important;
  overflow-wrap:break-word!important;
}
.pa-combined-preview-section .pa-event-card-preview .pa-event-card__meta{
  display:flex!important;
  align-items:center!important;
  flex-wrap:wrap!important;
  gap:.45rem!important;
  margin:.5rem 0 0!important;
  padding:0!important;
  line-height:1.25!important;
  color:var(--pa-agenda-location-color,inherit)!important;
  text-align:left!important;
}
.pa-combined-preview-section .pa-event-card-preview .pa-event-card__category{
  display:inline-flex!important;
  align-items:center!important;
  gap:.45rem!important;
  min-width:0!important;
}
.pa-combined-preview-section .pa-event-card-preview .pa-event-card__category-icon{
  display:inline-flex!important;
  align-items:center!important;
  justify-content:center!important;
  color:currentColor!important;
  background:transparent!important;
  border:0!important;
  border-radius:0!important;
  font-style:normal!important;
  line-height:1!important;
}
.pa-combined-preview-section .pa-event-card-preview .pa-event-card__meta-dot,
.pa-combined-preview-section .pa-event-card-preview .pa-event-card__description{
  color:var(--pa-agenda-location-color,inherit)!important;
}
.pa-combined-preview-section .pa-event-card-preview .pa-event-card__description{
  margin:.75rem 0 0!important;
}
.pa-combined-preview-section .pa-event-card-preview .pa-event-card__speakers{
  box-sizing:border-box!important;
  width:100%!important;
  max-width:100%!important;
  margin-top:.85rem!important;
  padding:0!important;
  overflow-x:auto!important;
  overflow-y:visible!important;
}
.pa-combined-preview-section .pa-event-card-preview .pa-speaker-card-list,
.pa-combined-preview-section .pa-event-card-preview .pa-speaker-card-list-agenda{
  margin:0!important;
  display:flex!important;
  flex-wrap:nowrap!important;
  align-items:flex-start!important;
  gap:.75rem!important;
  overflow-x:auto!important;
  padding-bottom:10px!important;
}
.pa-combined-preview-section .pa-event-card-preview .pa-speaker-card{
  box-sizing:border-box!important;
  display:flex!important;
  align-items:center!important;
  gap:.8rem!important;
  min-height:56px!important;
  padding:10px 14px!important;
  border-radius:.75rem!important;
  flex:0 0 auto!important;
}
.pa-combined-preview-section .pa-event-card-preview .pa-speaker-card-image{
  width:44px!important;
  height:44px!important;
  min-width:44px!important;
  max-width:44px!important;
  min-height:44px!important;
  max-height:44px!important;
  flex:none!important;
}
.pa-combined-preview-section .pa-event-card-preview .pa-speaker-card-thumb{
  display:block!important;
  width:44px!important;
  height:44px!important;
  object-fit:cover!important;
  background:#ddd!important;
  border-radius:.5rem;
}
.pa-combined-preview-section .pa-event-card-preview.pa-event-card--size-full,
.pa-combined-preview-section .pa-event-card-preview.pa-event-card--size-full:hover,
.pa-combined-preview-section .pa-event-card-preview.pa-event-card--size-full:focus-within{
  --pa-event-card-datebar-width:64px!important;
  grid-template-columns:64px minmax(0,1fr)!important;
  min-height:118px!important;
}
.pa-combined-preview-section .pa-event-card-preview.pa-event-card--size-thin,
.pa-combined-preview-section .pa-event-card-preview.pa-event-card--size-thin:hover,
.pa-combined-preview-section .pa-event-card-preview.pa-event-card--size-thin:focus-within{
  --pa-event-card-datebar-width:56px!important;
  grid-template-columns:56px minmax(0,1fr)!important;
  min-height:54px!important;
}
.pa-combined-preview-section .pa-event-card-preview.pa-event-card--size-thin .pa-event-card__datebar{gap:1px!important;padding:6px 8px!important;}
.pa-combined-preview-section .pa-event-card-preview.pa-event-card--size-thin .pa-event-card__date,
.pa-combined-preview-section .pa-event-card-preview.pa-event-card--size-thin .pa-event-card__time{font-size:.67rem!important;line-height:1.05!important;}
.pa-combined-preview-section .pa-event-card-preview.pa-event-card--size-thin .pa-event-card__body{padding:10px 18px!important;}
.pa-combined-preview-section .pa-event-card-preview.pa-event-card--size-thin .pa-event-card__speakers,
.pa-combined-preview-section .pa-event-card-preview.pa-event-card--size-thin .pa-event-card__description{display:none!important;}

.pa-preview-line{
  display:block;
  height:8px;
  border-radius:999px;
  background:currentColor;
  opacity:.9;
}
.pa-preview-line + .pa-preview-line{margin-top:10px;}
.pa-preview-line-title{width:120px;height:8px;color:var(--pa-agenda-title-color,inherit);}
.pa-preview-line-short{width:65px;height:6px;color:var(--pa-agenda-location-color,inherit);}
.pa-preview-line-medium{width:130px;height:6px;color:var(--pa-agenda-location-color,inherit);}
.pa-preview-line-heading{width:180px;height:10px;}
.pa-preview-line-subheading{width:130px;height:7px;}
.pa-preview-line-content{width:min(360px,100%);height:7px;}
.pa-preview-line-speaker-name{width:95px;height:7px;}
.pa-preview-line-speaker-role{width:75px;height:5px;opacity:.75;}
.pa-preview-line-speaker-company{width:88px;height:5px;opacity:.75;}
.pa-preview-content{display:grid;gap:12px;}
.pa-program-page-preview-card .pa-single-content .pa-preview-line-content{width:min(360px,100%);}
.pa-preview-header .pa-preview-line,
.pa-preview-content .pa-preview-line{background:currentColor;}
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

# Replace Event Page / Speaker Page preview text at the source with placeholder lines.
php = re.sub(
    r"    private function program_page_preview\(\$type, \$s\) \{[\s\S]*?\n    \}\n\n    private function program_page_settings_controls",
    r'''    private function program_page_preview($type, $s) {
        if (!is_array($s)) { $s = []; }
        $is_speaker = $type === 'speaker';
        echo '<section class="pa-preview-card pa-program-page-preview-card"><div class="pa-preview-title"><h3>Preview</h3></div>';
        echo '<div class="pa-live-preview" data-program-page-preview="' . esc_attr($type) . '">';
        if ($is_speaker) {
            echo '<div class="pa-preview-header pa-preview-speaker-header" style="' . esc_attr($this->inline_header_style($s)) . '"><span class="pa-preview-image" style="' . esc_attr($this->preview_image_style($s)) . '"></span><div class="pa-preview-speaker-text"><span class="pa-preview-line pa-preview-line-heading"></span><span class="pa-preview-line pa-preview-line-subheading"></span><span class="pa-preview-line pa-preview-line-subheading"></span></div><nav class="pa-preview-speaker-icons" aria-label="Preview speaker links"><span class="pa-preview-icon" aria-hidden="true">↗</span><span class="pa-preview-icon" aria-hidden="true">◎</span></nav></div>';
        } else {
            echo '<div class="pa-preview-header" style="' . esc_attr($this->inline_header_style($s)) . '"><span class="pa-preview-line pa-preview-line-heading"></span><span class="pa-preview-line pa-preview-line-subheading"></span></div>';
        }
        echo '<div class="pa-preview-content" style="' . esc_attr($this->inline_content_style($s)) . '"><span class="pa-preview-line pa-preview-line-content"></span><span class="pa-preview-line pa-preview-line-content"></span><span class="pa-preview-line pa-preview-line-content"></span></div></div></section>';
    }

    private function program_page_settings_controls''',
    php,
    count=1
)
PHP.write_text(php)

print('Admin preview CSS cleanup complete.')
