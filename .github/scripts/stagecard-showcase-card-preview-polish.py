from pathlib import Path
import re

php_path = Path('program-agenda/program-agenda.php')
public_css_path = Path('program-agenda/assets/css/public.css')
admin_css_path = Path('program-agenda/assets/css/admin.css')
js_path = Path('program-agenda/assets/js/admin.js')

php = php_path.read_text()
php = php.replace("            if ($printed > 0) { echo '<div class=\"pa-sponsor-showcase-separator\" aria-hidden=\"true\"></div>'; }\n", "")
php = php.replace("<section class=\"pa-sponsor-level-group\"><h1>' . esc_html($level) . '</h1><div class=\"pa-sponsor-logo-grid\">", "<section class=\"pa-sponsor-level-group\"><h2>' . esc_html($level) . '</h2><div class=\"pa-sponsor-logo-grid\">")
php_path.write_text(php)

public_css = public_css_path.read_text()
public_marker = '/* v1.15.161: sponsor showcase spacing and borderless event cards */'
public_addition = """

/* v1.15.161: sponsor showcase spacing and borderless event cards */
.pa-sponsor-level-group h1,
.pa-sponsor-level-group h2{
  margin:0 0 24px!important;
}
.pa-sponsor-level-group + .pa-sponsor-level-group{
  margin-top:60px!important;
}
.pa-sponsor-showcase-separator{
  display:none!important;
  margin:0!important;
  border:0!important;
}
.pa-event-card{
  border-color:var(--pa-event-card-border-color, transparent)!important;
}
.pa-event-card::after{
  border-color:var(--pa-event-card-border-color, transparent)!important;
}
"""
if public_marker not in public_css:
    public_css_path.write_text(public_css.rstrip() + public_addition)

js = js_path.read_text()
# Ensure preview no longer reads/uses hover animation.
js = js.replace("    var hoverAnim=$('[name=\"agenda[hover_animation]\"]').val() || 'default'; if(hoverAnim !== 'slant') hoverAnim = 'default';\n    $p.removeClass('pa-event-card--hover-default pa-event-card--hover-slant').addClass('pa-event-card--hover-'+hoverAnim);\n", "    $p.removeClass('pa-event-card--hover-default pa-event-card--hover-slant');\n")
js = js.replace("    $('[name=\"agenda[hover_animation]\"]').val('default');\n", "")
js = js.replace("      $('[name=\"agenda[hover_animation]\"]').val(ag.hover_animation || 'default');\n", "")
# Strengthen agenda preview border rendering.
old = "    applyProgramBorder($p,'agenda'); if(bc){ $p.css({'borderColor':bc,'--pa-event-card-border-color':bc}); }\n    $p.css('overflow','hidden');"
new = """    applyProgramBorder($p,'agenda'); if(bc){ $p.css({'borderColor':bc,'--pa-event-card-border-color':bc}); }
    var borderMap={tl:'top-left',tr:'top-right',br:'bottom-right',bl:'bottom-left'};
    ['tl','tr','br','bl'].forEach(function(k){
      var v=$('[name=\"agenda[radius_'+k+']\"]').val();
      if(v !== undefined && v !== ''){ $p[0].style.setProperty('border-'+borderMap[k]+'-radius', v+'px', 'important'); }
    });
    ['top','right','bottom','left'].forEach(function(k){
      var v=$('[name=\"agenda[width_'+k+']\"]').val();
      if(v !== undefined && v !== ''){ $p[0].style.setProperty('border-'+k+'-width', v+'px', 'important'); $p[0].style.setProperty('border-style', 'solid', 'important'); }
    });
    if(bc){ $p[0].style.setProperty('border-color', bc, 'important'); }
    $p[0].style.setProperty('overflow','hidden','important');"""
if old in js:
    js = js.replace(old, new)
js_path.write_text(js)

admin_css = admin_css_path.read_text()
admin_marker = '/* v1.15.161: static simple previews with color lines */'
admin_addition = """

/* v1.15.161: static simple previews with color lines */
.pa-event-card-preview,
.pa-event-card-preview:hover,
.pa-event-card-preview:focus-within{
  transform:none!important;
  transition:none!important;
}
.pa-event-card-preview,
.pa-event-card-preview:hover,
.pa-event-card-preview:focus-within{
  --pa-event-card-datebar-hover-width:var(--pa-event-card-datebar-width)!important;
  grid-template-columns:var(--pa-event-card-datebar-width) minmax(0,1fr)!important;
}
.pa-event-card-preview .pa-event-card__datebar,
.pa-event-card-preview:hover .pa-event-card__datebar,
.pa-event-card-preview:focus-within .pa-event-card__datebar{
  clip-path:none!important;
  transform:none!important;
  transition:none!important;
}
.pa-event-card-preview .pa-event-card__datebar::before,
.pa-event-card-preview .pa-event-card__datebar::after{
  display:none!important;
  content:none!important;
}
.pa-preview-line-source,
.pa-event-card-preview .pa-event-card__title a,
.pa-event-card-preview .pa-event-card__category-text,
.pa-event-card-preview .pa-event-card__location,
.pa-event-card-preview .pa-event-card__description,
.pa-event-card-preview .pa-speaker-card-preview-text h3 a,
.pa-event-card-preview .pa-speaker-card-preview-text p,
.pa-speaker-card-preview .pa-speaker-card-preview-text h3 a,
.pa-speaker-card-preview .pa-speaker-card-preview-text p,
.pa-live-preview .pa-preview-header strong,
.pa-live-preview .pa-preview-header small,
.pa-live-preview .pa-preview-content strong,
.pa-live-preview .pa-preview-content p{
  display:block!important;
  font-size:0!important;
  line-height:0!important;
  text-indent:-9999px!important;
  overflow:hidden!important;
  text-decoration:none!important;
  color:inherit!important;
}
.pa-event-card-preview .pa-event-card__title a::before,
.pa-event-card-preview .pa-event-card__category-text::before,
.pa-event-card-preview .pa-event-card__location::before,
.pa-event-card-preview .pa-event-card__description::before,
.pa-event-card-preview .pa-speaker-card-preview-text h3 a::before,
.pa-event-card-preview .pa-speaker-card-preview-text p::before,
.pa-speaker-card-preview .pa-speaker-card-preview-text h3 a::before,
.pa-speaker-card-preview .pa-speaker-card-preview-text p::before,
.pa-live-preview .pa-preview-header strong::before,
.pa-live-preview .pa-preview-header small::before,
.pa-live-preview .pa-preview-content strong::before,
.pa-live-preview .pa-preview-content p::before{
  content:""!important;
  display:block!important;
  height:8px!important;
  border-radius:999px!important;
  background:currentColor!important;
  opacity:.9!important;
  text-indent:0!important;
}
.pa-event-card-preview .pa-event-card__title a::before{width:120px!important;height:7px!important;}
.pa-event-card-preview .pa-event-card__category-text::before{width:62px!important;height:6px!important;}
.pa-event-card-preview .pa-event-card__location::before{width:110px!important;height:6px!important;}
.pa-event-card-preview .pa-event-card__description::before{width:min(260px,100%)!important;height:6px!important;box-shadow:0 12px 0 currentColor!important;}
.pa-event-card-preview .pa-speaker-card-preview-text h3 a::before,
.pa-speaker-card-preview .pa-speaker-card-preview-text h3 a::before{width:95px!important;height:7px!important;}
.pa-event-card-preview .pa-speaker-card-preview-text p::before,
.pa-speaker-card-preview .pa-speaker-card-preview-text p::before{width:70px!important;height:5px!important;opacity:.7!important;}
.pa-live-preview .pa-preview-header strong::before{width:180px!important;height:10px!important;}
.pa-live-preview .pa-preview-header small::before{width:130px!important;height:6px!important;opacity:.8!important;}
.pa-live-preview .pa-preview-content strong::before{width:160px!important;height:8px!important;}
.pa-live-preview .pa-preview-content p::before{width:min(360px,100%)!important;height:6px!important;box-shadow:0 13px 0 currentColor,0 26px 0 currentColor!important;opacity:.75!important;}
.pa-preview-speaker-role::before{width:95px!important;}
.pa-preview-speaker-company::before{width:120px!important;}
"""
if admin_marker not in admin_css:
    admin_css_path.write_text(admin_css.rstrip() + admin_addition)
