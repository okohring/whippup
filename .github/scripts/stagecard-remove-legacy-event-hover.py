from pathlib import Path
import re

public_path = Path('program-agenda/assets/css/public.css')
admin_path = Path('program-agenda/assets/css/admin.css')
js_path = Path('program-agenda/assets/js/admin.js')

public = public_path.read_text()

# Remove the old standalone event-card hover animation block. This is the main source
# of the accent/datebar sliding because it changes grid-template-columns on hover.
public = re.sub(
    r"\n/\* v1\.15\.95: Event Card hover animations[\s\S]*?(?=\n/\* v1\.15\.96: Event Card size options\.)",
    "\n",
    public,
    count=1,
)

# Neutralize the earlier v1.15.94 grid-column hover behavior without removing the
# full component block.
public = public.replace('  --pa-event-card-datebar-hover-width:145px;\n', '')
public = public.replace('  transition:grid-template-columns .18s ease!important;\n', '')
public = public.replace(".pa-event-card:hover,\n.pa-event-card:focus-within{\n  grid-template-columns:var(--pa-event-card-datebar-hover-width) minmax(0,1fr)!important;\n}\n", "")

# Thin cards should not define a separate hover width anymore.
public = public.replace('  --pa-event-card-datebar-hover-width:84px!important;\n', '')

# Remove old slant-specific thin-card hover clip-path.
public = re.sub(
    r"\n\.pa-event-card\.pa-event-card--size-thin\.pa-event-card--hover-slant:hover \.pa-event-card__datebar,[\s\S]*?\n}\n(?=\.pa-speaker-upcoming-events|@media|/\*)",
    "\n",
    public,
    count=1,
)

# Add a concise final public event-card hover rule: the card may gently scale, but
# the accent/datebar grid column never changes size.
marker = '/* v1.15.162: remove legacy event-card accent hover movement */'
addition = """

/* v1.15.162: remove legacy event-card accent hover movement */
.pa-event-card,
.pa-event-card:hover,
.pa-event-card:focus-within{
  --pa-event-card-datebar-hover-width:var(--pa-event-card-datebar-width)!important;
  grid-template-columns:var(--pa-event-card-datebar-width) minmax(0,1fr)!important;
}
.pa-event-card.pa-event-card--size-full,
.pa-event-card.pa-event-card--size-full:hover,
.pa-event-card.pa-event-card--size-full:focus-within{
  --pa-event-card-datebar-width:64px!important;
  grid-template-columns:64px minmax(0,1fr)!important;
}
.pa-event-card.pa-event-card--size-thin,
.pa-event-card.pa-event-card--size-thin:hover,
.pa-event-card.pa-event-card--size-thin:focus-within{
  --pa-event-card-datebar-width:56px!important;
  grid-template-columns:56px minmax(0,1fr)!important;
}
.pa-event-card:hover .pa-event-card__datebar,
.pa-event-card:focus-within .pa-event-card__datebar{
  clip-path:none!important;
  transform:none!important;
  transition:none!important;
}
"""
if marker not in public:
    public = public.rstrip() + addition
public_path.write_text(public)

# Also make admin preview static at the source, because preview should not inherit
# public hover behavior at all.
admin = admin_path.read_text()
admin_marker = '/* v1.15.162: preview event cards are static after legacy hover cleanup */'
admin_addition = """

/* v1.15.162: preview event cards are static after legacy hover cleanup */
.pa-event-card-preview,
.pa-event-card-preview:hover,
.pa-event-card-preview:focus-within{
  transform:none!important;
  transition:none!important;
  --pa-event-card-datebar-hover-width:var(--pa-event-card-datebar-width)!important;
  grid-template-columns:var(--pa-event-card-datebar-width) minmax(0,1fr)!important;
}
.pa-event-card-preview.pa-event-card--size-full,
.pa-event-card-preview.pa-event-card--size-full:hover,
.pa-event-card-preview.pa-event-card--size-full:focus-within{
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
"""
if admin_marker not in admin:
    admin = admin.rstrip() + admin_addition
admin_path.write_text(admin)

# Remove any preview JS that re-adds the old hover classes.
js = js_path.read_text()
js = js.replace("    var hoverAnim=$('[name=\"agenda[hover_animation]\"]').val() || 'default'; if(hoverAnim !== 'slant') hoverAnim = 'default';\n    $p.removeClass('pa-event-card--hover-default pa-event-card--hover-slant').addClass('pa-event-card--hover-'+hoverAnim);\n", "    $p.removeClass('pa-event-card--hover-default pa-event-card--hover-slant');\n")
js_path.write_text(js)
