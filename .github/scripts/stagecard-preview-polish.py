from pathlib import Path
import re

js_path = Path('program-agenda/assets/js/admin.js')
admin_css_path = Path('program-agenda/assets/css/admin.css')

js = js_path.read_text()

# Remove preview hover animation class logic and any reset/copy references to removed option.
js = js.replace("    var hoverAnim=$('[name=\"agenda[hover_animation]\"]').val() || 'default'; if(hoverAnim !== 'slant') hoverAnim = 'default';\n    $p.removeClass('pa-event-card--hover-default pa-event-card--hover-slant').addClass('pa-event-card--hover-'+hoverAnim);\n", "    $p.removeClass('pa-event-card--hover-default pa-event-card--hover-slant');\n")
js = js.replace("    $('[name=\"agenda[hover_animation]\"]').val('default');\n", "")
js = js.replace("      $('[name=\"agenda[hover_animation]\"]').val(ag.hover_animation || 'default');\n", "")

# Strengthen agenda preview border rendering so border widths/radii are visible despite !important CSS.
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
marker = '/* v1.15.160: admin event-card preview matches stable public hover and border behavior */'
addition = """

/* v1.15.160: admin event-card preview matches stable public hover and border behavior */
.pa-event-card-preview,
.pa-event-card-preview:hover,
.pa-event-card-preview:focus-within{
  --pa-event-card-datebar-width:64px!important;
  --pa-event-card-datebar-hover-width:64px!important;
  grid-template-columns:64px minmax(0,1fr)!important;
  transition:transform .16s ease, box-shadow .16s ease!important;
}
.pa-event-card-preview:hover,
.pa-event-card-preview:focus-within{
  transform:scale(1.015)!important;
}
.pa-event-card-preview .pa-event-card__datebar,
.pa-event-card-preview:hover .pa-event-card__datebar,
.pa-event-card-preview:focus-within .pa-event-card__datebar{
  clip-path:none!important;
  transform:none!important;
  width:auto!important;
  min-width:0!important;
  max-width:none!important;
  transition:none!important;
}
.pa-event-card-preview .pa-event-card__datebar::before,
.pa-event-card-preview .pa-event-card__datebar::after{
  content:none!important;
  display:none!important;
  transform:none!important;
  transition:none!important;
}
.pa-event-card-preview.pa-event-card--size-thin,
.pa-event-card-preview.pa-event-card--size-thin:hover,
.pa-event-card-preview.pa-event-card--size-thin:focus-within{
  --pa-event-card-datebar-width:56px!important;
  --pa-event-card-datebar-hover-width:56px!important;
  grid-template-columns:56px minmax(0,1fr)!important;
}
"""
if marker not in admin_css:
    admin_css_path.write_text(admin_css.rstrip() + addition)
