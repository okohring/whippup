from pathlib import Path

css_path = Path('program-agenda/assets/css/public.css')
css = css_path.read_text()
marker = '/* v1.15.159: hard-lock event card accent column and sponsor label color */'
addition = """

/* v1.15.159: hard-lock event card accent column and sponsor label color */
.pa-event-card,
.pa-event-card:hover,
.pa-event-card:focus-within{
  --pa-event-card-datebar-hover-width:var(--pa-event-card-datebar-width)!important;
  grid-template-columns:var(--pa-event-card-datebar-width) minmax(0,1fr)!important;
  transition:transform .16s ease, box-shadow .16s ease!important;
}
.pa-event-card.pa-event-card--size-full,
.pa-event-card.pa-event-card--size-full:hover,
.pa-event-card.pa-event-card--size-full:focus-within{
  --pa-event-card-datebar-width:64px!important;
  --pa-event-card-datebar-hover-width:64px!important;
  grid-template-columns:64px minmax(0,1fr)!important;
}
.pa-event-card.pa-event-card--size-thin,
.pa-event-card.pa-event-card--size-thin:hover,
.pa-event-card.pa-event-card--size-thin:focus-within{
  --pa-event-card-datebar-width:56px!important;
  --pa-event-card-datebar-hover-width:56px!important;
  grid-template-columns:56px minmax(0,1fr)!important;
}
.pa-event-card:hover .pa-event-card__datebar,
.pa-event-card:focus-within .pa-event-card__datebar,
.pa-event-card.pa-event-card--hover-slant:hover .pa-event-card__datebar,
.pa-event-card.pa-event-card--hover-slant:focus-within .pa-event-card__datebar,
.pa-event-card.pa-event-card--size-thin.pa-event-card--hover-slant:hover .pa-event-card__datebar,
.pa-event-card.pa-event-card--size-thin.pa-event-card--hover-slant:focus-within .pa-event-card__datebar{
  clip-path:none!important;
  transform:none!important;
  width:auto!important;
  min-width:0!important;
  max-width:none!important;
}
.pa-event-card__datebar::before,
.pa-event-card__datebar::after,
.pa-agenda-category-bar::before,
.pa-agenda-category-bar::after{
  content:none!important;
  display:none!important;
  transform:none!important;
  transition:none!important;
}
.pa-single-sponsor .pa-sponsor-page-label,
.pa-single-sponsor .pa-sponsor-page-label:visited,
.pa-single-sponsor .pa-sponsor-page-label:hover,
.pa-single-sponsor .pa-sponsor-page-label:focus{
  color:inherit!important;
  opacity:1!important;
}
.pa-single-sponsor .pa-sponsor-hero-text,
.pa-single-sponsor .pa-sponsor-hero-text :where(h1,h2,h3,h4,h5,h6,p,span,a,a:visited,a:hover,a:focus){
  color:inherit!important;
}
@media(max-width:700px){
  .pa-event-card,
  .pa-event-card:hover,
  .pa-event-card:focus-within,
  .pa-event-card.pa-event-card--size-full,
  .pa-event-card.pa-event-card--size-full:hover,
  .pa-event-card.pa-event-card--size-full:focus-within,
  .pa-event-card.pa-event-card--size-thin,
  .pa-event-card.pa-event-card--size-thin:hover,
  .pa-event-card.pa-event-card--size-thin:focus-within{
    --pa-event-card-datebar-width:58px!important;
    --pa-event-card-datebar-hover-width:58px!important;
    grid-template-columns:58px minmax(0,1fr)!important;
  }
}
"""
if marker not in css:
    css_path.write_text(css.rstrip() + addition)
