from pathlib import Path
import re

PUBLIC = Path('program-agenda/assets/css/public.css')
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


def remove_selector_blocks_containing(text, needle):
    """Remove simple CSS blocks whose selector contains needle."""
    pattern = re.compile(r'(^|\n)([^{}]*' + re.escape(needle) + r'[^{}]*\{[^{}]*\})', re.M)
    old = None
    while old != text:
        old = text
        text = pattern.sub('\n', text)
    return text


public = PUBLIC.read_text()

# 1) Remove legacy agenda-item accent expansion at the top of the file. The current
# public cards use .pa-event-card, not this older flex card path.
public = public.replace('  transition:width .18s ease;\n', '')
public = re.sub(
    r'\n\.pa-agenda-item:hover \.pa-agenda-category-bar,\n\.pa-agenda-item:focus-within \.pa-agenda-category-bar\{\n\s*width:145px;\n\}\n',
    '\n',
    public,
)
public = public.replace('  .pa-agenda-category-bar,\n  .pa-agenda-item:hover .pa-agenda-category-bar,\n  .pa-agenda-item:focus-within .pa-agenda-category-bar{', '  .pa-agenda-category-bar{')

# 2) Remove old sponsor showcase/page blocks and later patch layers. These were
# iterative fixes; the final clean sponsor rules are appended once below.
public = remove_block(public, '/* v1.15.102: Sponsor Showcase + Individual Sponsor Pages */', '/* Stagecard layout and URL polish */')

# 3) Remove all late stacked patch sections and replace them with one consolidated
# final section.
public = remove_block(public, '/* Stagecard layout and URL polish */')

# 4) Remove lingering slant/hover-animation selector blocks and hover-width variables.
public = remove_selector_blocks_containing(public, 'pa-event-card--hover')
public = public.replace('  --pa-event-card-datebar-hover-width:58px;\n', '')
public = public.replace('  --pa-event-card-datebar-hover-width:58px!important;\n', '')
public = public.replace('  --pa-event-card-datebar-hover-width:64px!important;\n', '')
public = public.replace('  --pa-event-card-datebar-hover-width:84px!important;\n', '')
public = public.replace('  --pa-event-card-datebar-hover-width:98px!important;\n', '')
public = public.replace('  --pa-event-card-datebar-hover-width:145px;\n', '')
public = re.sub(r'\n\.pa-event-card:hover,\n\.pa-event-card:focus-within\{\n\s*grid-template-columns:var\(--pa-event-card-datebar-hover-width\) minmax\(0,1fr\)!important;\n\}\n', '\n', public)

# 5) Remove obsolete sponsor-page wrapper rules. Current sponsor pages output
# .pa-single.pa-single-sponsor, not .pa-theme-sponsor-page.
public = remove_selector_blocks_containing(public, 'pa-theme-sponsor-page')

final_public = r'''

/* Stagecard final public layout cleanup: event cards, sponsor showcase, sponsor pages */
.pa-event-card{
  --pa-event-card-datebar-width:64px;
  box-sizing:border-box!important;
  display:grid!important;
  grid-template-columns:var(--pa-event-card-datebar-width) minmax(0,1fr)!important;
  width:100%!important;
  max-width:100%!important;
  min-height:118px!important;
  overflow:hidden!important;
  position:relative!important;
  isolation:isolate!important;
  background:var(--pa-agenda-card-bg,#fff)!important;
  background-color:var(--pa-agenda-card-bg,#fff)!important;
  color:inherit!important;
  border:0!important;
  gap:0!important;
  border-spacing:0!important;
  grid-auto-rows:1fr!important;
  transition:transform .16s ease,box-shadow .16s ease!important;
  transform-origin:center center!important;
}
.pa-event-card:hover,
.pa-event-card:focus-within{
  grid-template-columns:var(--pa-event-card-datebar-width) minmax(0,1fr)!important;
  transform:scale(1.015)!important;
}
.pa-event-card::after{
  content:""!important;
  display:block!important;
  position:absolute!important;
  inset:0!important;
  pointer-events:none!important;
  z-index:10!important;
  border:1px solid var(--pa-event-card-border-color, transparent)!important;
  border-radius:inherit!important;
  box-sizing:border-box!important;
}
.pa-event-card__datebar{
  box-sizing:border-box!important;
  grid-column:1!important;
  grid-row:1!important;
  width:auto!important;
  min-width:0!important;
  max-width:none!important;
  height:calc(100% + 4px)!important;
  min-height:calc(100% + 4px)!important;
  top:-2px!important;
  left:-2px!important;
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
  position:relative!important;
  z-index:1!important;
  transform:none!important;
  transition:none!important;
  box-shadow:1px 0 0 var(--pa-agenda-bar-color,#1d2327)!important;
}
.pa-event-card:hover .pa-event-card__datebar,
.pa-event-card:focus-within .pa-event-card__datebar{
  clip-path:none!important;
  transform:none!important;
  transition:none!important;
}
.pa-event-card__datebar::before,
.pa-event-card__datebar::after{
  content:none!important;
  display:none!important;
}
.pa-event-card__date,
.pa-event-card__time{
  display:block!important;
  margin:0!important;
  padding:0!important;
  font-size:.78rem!important;
  line-height:1.1!important;
  text-transform:uppercase!important;
  white-space:nowrap!important;
}
.pa-event-card__icon{
  display:grid!important;
  place-items:center!important;
  margin-top:8px!important;
  font-size:1rem!important;
  line-height:1!important;
  text-align:center!important;
}
.pa-event-card__body{
  box-sizing:border-box!important;
  grid-column:2!important;
  grid-row:1!important;
  min-width:0!important;
  width:calc(100% + 4px)!important;
  max-width:calc(100% + 4px)!important;
  height:calc(100% + 4px)!important;
  min-height:calc(100% + 4px)!important;
  top:-2px!important;
  right:-2px!important;
  padding:20px 28px!important;
  display:flex!important;
  flex-direction:column!important;
  justify-content:center!important;
  align-items:flex-start!important;
  text-align:left!important;
  overflow:hidden!important;
  position:relative!important;
  z-index:2!important;
  background:var(--pa-agenda-card-bg,#fff)!important;
  background-color:var(--pa-agenda-card-bg,#fff)!important;
  transform:translateZ(0)!important;
}
.pa-event-card__summary{
  box-sizing:border-box!important;
  display:block!important;
  width:100%!important;
  min-width:0!important;
  max-width:100%!important;
  margin:0!important;
  padding:0!important;
  text-align:left!important;
}
.pa-event-card .pa-event-card__title,
.pa-event-card .pa-event-card__title a{
  display:block!important;
  margin:0!important;
  padding:0!important;
  font-size:1rem!important;
  line-height:1.15!important;
  font-weight:600!important;
  letter-spacing:normal!important;
  text-transform:none!important;
  color:var(--pa-agenda-title-color,inherit)!important;
  text-align:left!important;
  white-space:normal!important;
  overflow-wrap:break-word!important;
}
.pa-event-card__meta{
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
.pa-event-card__category{
  display:inline-flex!important;
  align-items:center!important;
  gap:.45rem!important;
  min-width:0!important;
}
.pa-event-card__category-text{
  color:var(--pa-agenda-category-color,var(--pa-agenda-location-color,var(--pa-agenda-title-color,inherit)))!important;
}
.pa-event-card__category-icon{
  display:inline-flex!important;
  align-items:center!important;
  justify-content:center!important;
  color:currentColor;
  background:transparent!important;
  border:0!important;
  border-radius:0!important;
  font-style:normal!important;
  line-height:1!important;
}
.pa-event-card__location,
.pa-event-card__location a,
.pa-event-card__meta-dot{
  color:var(--pa-agenda-location-color,inherit)!important;
}
.pa-event-card__invite-icon{
  display:inline-flex!important;
  width:1em!important;
  height:1em!important;
  color:var(--pa-agenda-location-color,inherit)!important;
  vertical-align:-.12em!important;
}
.pa-event-card__invite-icon svg{display:block!important;width:100%!important;height:100%!important;}
.pa-event-card__description{
  margin:.75rem 0 0!important;
  color:var(--pa-agenda-location-color,inherit)!important;
}
.pa-event-card__speakers{
  box-sizing:border-box!important;
  width:100%!important;
  max-width:100%!important;
  margin-top:.85rem!important;
  padding:0!important;
  overflow-x:auto!important;
  overflow-y:visible!important;
}
.pa-event-card__speakers .pa-speaker-card-list,
.pa-event-card__speakers .pa-speaker-card-list-agenda{
  margin:0!important;
  display:flex!important;
  flex-wrap:wrap!important;
  align-items:flex-start!important;
  gap:.75rem!important;
}
.pa-event-card--speakers-inline .pa-event-card__speakers .pa-speaker-card-list-agenda{
  flex-wrap:nowrap!important;
  overflow-x:auto!important;
  padding-bottom:10px!important;
}
.pa-event-card--speakers-inline .pa-event-card__speakers .pa-speaker-card{flex:0 0 auto!important;}
.pa-event-card.pa-event-card--size-full{
  --pa-event-card-datebar-width:64px!important;
  min-height:118px!important;
  grid-template-columns:64px minmax(0,1fr)!important;
}
.pa-event-card.pa-event-card--size-full:hover,
.pa-event-card.pa-event-card--size-full:focus-within{grid-template-columns:64px minmax(0,1fr)!important;}
.pa-event-card.pa-event-card--size-full .pa-event-card__speakers .pa-speaker-card{
  grid-template-columns:44px max-content!important;
  column-gap:10px!important;
}
.pa-event-card.pa-event-card--size-full .pa-event-card__speakers .pa-speaker-card-image{
  width:44px!important;height:44px!important;min-width:44px!important;max-width:44px!important;min-height:44px!important;max-height:44px!important;flex-basis:44px!important;
}
.pa-event-card.pa-event-card--size-full .pa-event-card__speakers .pa-speaker-card-text{padding-right:18px!important;}
.pa-event-card.pa-event-card--size-full .pa-event-card__speakers .pa-speaker-card-text h3,
.pa-event-card.pa-event-card--size-full .pa-event-card__speakers .pa-speaker-card-text h3 a,
.pa-event-card.pa-event-card--size-full .pa-event-card__speakers .pa-speaker-card-text p{
  font-size:.86rem!important;
  line-height:1.12!important;
  margin-bottom:1px!important;
}
.pa-event-card.pa-event-card--size-thin{
  --pa-event-card-datebar-width:56px!important;
  min-height:54px!important;
  grid-template-columns:56px minmax(0,1fr)!important;
}
.pa-event-card.pa-event-card--size-thin:hover,
.pa-event-card.pa-event-card--size-thin:focus-within{grid-template-columns:56px minmax(0,1fr)!important;}
.pa-event-card.pa-event-card--size-thin .pa-event-card__datebar{gap:1px!important;padding:6px 8px!important;}
.pa-event-card.pa-event-card--size-thin .pa-event-card__date,
.pa-event-card.pa-event-card--size-thin .pa-event-card__time{font-size:.67rem!important;line-height:1.05!important;}
.pa-event-card.pa-event-card--size-thin .pa-event-card__icon{display:none!important;}
.pa-event-card.pa-event-card--size-thin .pa-event-card__body{padding:10px 18px!important;}
.pa-event-card.pa-event-card--size-thin .pa-event-card__title,
.pa-event-card.pa-event-card--size-thin .pa-event-card__title a{font-size:1rem!important;line-height:1.12!important;}
.pa-event-card.pa-event-card--size-thin .pa-event-card__meta{margin:.22rem 0 0!important;gap:.35rem!important;font-size:.82rem!important;line-height:1.15!important;}
.pa-event-card.pa-event-card--size-thin .pa-event-card__speakers,
.pa-event-card.pa-event-card--size-thin .pa-event-card__description{display:none!important;}
.pa-speaker-upcoming-events .pa-event-list,
.pa-schedule .pa-event-list{display:grid!important;gap:1rem!important;}
@media(max-width:700px){
  .pa-event-card:hover,.pa-event-card:focus-within{transform:none!important;}
  .pa-event-card,
  .pa-event-card.pa-event-card--size-full,
  .pa-event-card.pa-event-card--size-thin{
    --pa-event-card-datebar-width:58px!important;
    grid-template-columns:58px minmax(0,1fr)!important;
  }
  .pa-event-card:hover,
  .pa-event-card:focus-within,
  .pa-event-card.pa-event-card--size-full:hover,
  .pa-event-card.pa-event-card--size-full:focus-within,
  .pa-event-card.pa-event-card--size-thin:hover,
  .pa-event-card.pa-event-card--size-thin:focus-within{grid-template-columns:58px minmax(0,1fr)!important;}
  .pa-event-card.pa-event-card--size-full{min-height:112px!important;}
  .pa-event-card.pa-event-card--size-full .pa-event-card__body{padding:18px!important;}
  .pa-event-card.pa-event-card--size-thin{min-height:54px!important;}
  .pa-event-card.pa-event-card--size-thin .pa-event-card__body{padding:10px 14px!important;}
}

.pa-sponsor-showcase{width:100%;box-sizing:border-box;}
.pa-sponsor-level-group{margin:0;padding:0;}
.pa-sponsor-level-group h1,
.pa-sponsor-level-group h2{margin:0 0 24px!important;}
.pa-sponsor-level-group + .pa-sponsor-level-group{margin-top:60px!important;}
.pa-sponsor-showcase-separator{display:none!important;margin:0!important;border:0!important;}
.pa-sponsor-logo-grid{
  display:grid!important;
  grid-template-columns:repeat(3,250px)!important;
  gap:40px 38px!important;
  justify-content:start!important;
  align-items:center!important;
  max-width:826px!important;
  overflow:visible!important;
}
.pa-sponsor-showcase-logo{
  box-sizing:border-box!important;
  display:flex!important;
  align-items:center!important;
  justify-content:center!important;
  width:250px!important;
  height:150px!important;
  min-height:150px!important;
  padding:0!important;
  overflow:visible!important;
  text-decoration:none!important;
  transform:scale(1)!important;
  transform-origin:center center!important;
  transition:transform 160ms ease!important;
  will-change:transform!important;
}
.pa-sponsor-showcase-logo:hover,
.pa-sponsor-showcase-logo:focus-visible,
.pa-event-sponsor-logo:hover,
.pa-event-sponsor-logo:focus-visible,
.pa-single-sponsor .pa-sponsor-logo a:hover,
.pa-single-sponsor .pa-sponsor-logo a:focus-visible{transform:scale(1.035)!important;}
.pa-sponsor-showcase-logo-img,
.pa-event-sponsor-logo-img{
  display:block!important;
  max-width:250px!important;
  max-height:150px!important;
  width:auto!important;
  height:auto!important;
  object-fit:contain!important;
}
.pa-sponsor-showcase-name{display:flex;align-items:center;justify-content:center;width:250px!important;min-height:150px!important;text-align:center;line-height:1.2;font-weight:700;}
@media(max-width:900px){.pa-sponsor-logo-grid{grid-template-columns:repeat(2,250px)!important;max-width:538px!important;}}
@media(max-width:640px){.pa-sponsor-logo-grid{grid-template-columns:repeat(auto-fit,minmax(150px,250px))!important;justify-content:center!important;max-width:none!important;}.pa-sponsor-showcase-logo,.pa-sponsor-showcase-name{width:min(250px,100%)!important;}.pa-sponsor-showcase-logo-img{max-width:100%!important;}}

.pa-single-sponsor{width:min(100%,1120px);max-width:1120px;margin-left:auto;margin-right:auto;box-sizing:border-box;}
.pa-single-sponsor *{box-sizing:border-box;}
.pa-single-sponsor .pa-sponsor-hero{display:flex;align-items:center;gap:28px;padding:32px;}
.pa-sponsor-hero-logo{background:#fff!important;border-radius:0!important;padding:30px!important;display:flex!important;align-items:center!important;justify-content:center!important;overflow:hidden!important;line-height:0!important;}
.pa-sponsor-hero-logo-wide{width:250px!important;height:150px!important;flex:0 0 250px!important;}
.pa-sponsor-hero-logo-square{width:150px!important;height:150px!important;flex:0 0 150px!important;}
.pa-sponsor-hero-logo a{display:flex!important;align-items:center!important;justify-content:center!important;width:100%!important;height:100%!important;}
.pa-sponsor-hero-logo-img{display:block!important;max-width:100%!important;max-height:100%!important;width:auto!important;height:auto!important;object-fit:contain!important;border-radius:0!important;margin:0!important;}
.pa-single-sponsor .pa-sponsor-page-label{margin:0 0 .35rem!important;padding:0!important;font-size:inherit!important;line-height:1.2!important;font-weight:700!important;text-transform:none!important;letter-spacing:normal!important;color:inherit!important;opacity:1!important;}
.pa-single-sponsor .pa-sponsor-name{margin:0 0 .25rem!important;padding:0!important;line-height:1.12!important;text-transform:none!important;letter-spacing:normal!important;}
.pa-single-sponsor .pa-sponsor-website{margin:.12rem 0!important;padding:0!important;font-size:.875rem!important;line-height:1.25!important;font-weight:inherit!important;text-transform:none!important;letter-spacing:normal!important;}
.pa-single-sponsor .pa-sponsor-website a{color:inherit!important;text-decoration:underline!important;text-underline-offset:.18em!important;}
.pa-single-sponsor .pa-sponsor-hero-text,
.pa-single-sponsor .pa-sponsor-hero-text :where(h1,h2,h3,h4,h5,h6,p,span,a,a:visited,a:hover,a:focus){color:inherit!important;}
.pa-single-sponsor .pa-sponsor-content{padding:32px;}
@media(max-width:1180px){.pa-single-sponsor{width:calc(100% - 32px);}}
@media(max-width:700px){.pa-single-sponsor{width:100%;}.pa-single-sponsor .pa-sponsor-hero{align-items:flex-start;gap:20px;}.pa-sponsor-hero-logo{width:100%;min-width:0;margin-bottom:20px;}}
'''

if '/* Stagecard final public layout cleanup: event cards, sponsor showcase, sponsor pages */' not in public:
    public = public.rstrip() + final_public
else:
    public = re.sub(r'\n/\* Stagecard final public layout cleanup: event cards, sponsor showcase, sponsor pages \*/[\s\S]*$', final_public.strip(), public)

# Trim excessive blank lines created by removal.
public = re.sub(r'\n{3,}', '\n\n', public).rstrip() + '\n'
PUBLIC.write_text(public)

# Admin CSS: remove stacked preview patches and append one final preview system.
admin = ADMIN.read_text()
admin = remove_block(admin, '/* v1.15.161: admin preview line placeholders and static event-card preview */')
admin = remove_block(admin, '/* v1.15.162: preview event cards are static after legacy hover cleanup */')
admin = remove_block(admin, '/* Simple preview placeholder lines */')

final_admin = r'''

/* Stagecard final admin preview system */
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
.pa-event-card-preview,
.pa-event-card-preview:hover,
.pa-event-card-preview:focus-within{
  transform:none!important;
  transition:none!important;
  --pa-event-card-datebar-width:64px!important;
  grid-template-columns:64px minmax(0,1fr)!important;
}
.pa-event-card-preview.pa-event-card--size-thin,
.pa-event-card-preview.pa-event-card--size-thin:hover,
.pa-event-card-preview.pa-event-card--size-thin:focus-within{
  --pa-event-card-datebar-width:56px!important;
  grid-template-columns:56px minmax(0,1fr)!important;
}
.pa-event-card-preview:hover .pa-event-card__datebar,
.pa-event-card-preview:focus-within .pa-event-card__datebar{
  clip-path:none!important;
  transform:none!important;
  transition:none!important;
}
.pa-event-card-preview .pa-event-card__datebar::before,
.pa-event-card-preview .pa-event-card__datebar::after{content:none!important;display:none!important;}
'''
if '/* Stagecard final admin preview system */' not in admin:
    admin = admin.rstrip() + final_admin
admin = re.sub(r'\n{3,}', '\n\n', admin).rstrip() + '\n'
ADMIN.write_text(admin)

# Admin JS: previews should never re-add old hover animation classes.
js = JS.read_text()
js = js.replace("    var hoverAnim=$('[name=\"agenda[hover_animation]\"]').val() || 'default'; if(hoverAnim !== 'slant') hoverAnim = 'default';\n    $p.removeClass('pa-event-card--hover-default pa-event-card--hover-slant').addClass('pa-event-card--hover-'+hoverAnim);\n", "    $p.removeClass('pa-event-card--hover-default pa-event-card--hover-slant');\n")
js = js.replace("$('[name=\"agenda[hover_animation]\"]').val('default');", "")
js = js.replace("$('[name=\"agenda[hover_animation]\"]').val(ag.hover_animation || 'default');", "")
JS.write_text(js)

# PHP: remove old hover classes from preview markup if any remain.
php = PHP.read_text()
php = php.replace(' pa-event-card--hover-default', '')
php = php.replace(' pa-event-card--hover-slant', '')
PHP.write_text(php)

print('Stagecard CSS cleanup complete.')
