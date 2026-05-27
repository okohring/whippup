from pathlib import Path

ADMIN_CSS = Path('program-agenda/assets/css/admin.css')
text = ADMIN_CSS.read_text()

marker = '/* Stagecard sponsor form UI cleanup */'
css = r'''
/* Stagecard sponsor form UI cleanup */
.pa-sponsor-form{
  max-width:1050px;
  display:grid;
  gap:22px;
  align-items:start;
}
.pa-sponsor-form > .pa-field,
.pa-sponsor-form > label,
.pa-sponsor-form > .pa-editor-field,
.pa-sponsor-form .pa-image-field{
  margin:0!important;
}
.pa-sponsor-form > label.pa-field:first-of-type{
  max-width:none;
}
.pa-sponsor-form > label.pa-field:first-of-type input{
  min-height:38px;
}
.pa-sponsor-logo-website-row{
  display:grid;
  grid-template-columns:minmax(220px,.85fr) minmax(300px,1.15fr);
  gap:22px;
  align-items:end;
  padding:16px;
  border:1px solid #dcdcde;
  border-radius:10px;
  background:#fbfbfc;
}
.pa-sponsor-logo-cell,
.pa-sponsor-website-cell{
  min-width:0;
  margin:0!important;
}
.pa-sponsor-logo-cell .pa-image-field{
  margin:0!important;
}
.pa-sponsor-logo-cell .pa-image-field > label,
.pa-sponsor-website-cell{
  display:block;
  margin:0 0 8px!important;
  font-weight:600;
  line-height:1.35;
}
.pa-sponsor-logo-cell .pa-image-recommendation{
  margin:4px 0 10px!important;
  font-size:12px;
  line-height:1.35;
  color:#646970;
}
.pa-sponsor-logo-cell .pa-image-preview{
  min-height:0!important;
  margin:8px 0!important;
}
.pa-sponsor-logo-cell .button,
.pa-sponsor-logo-cell .button-link{
  margin-top:0!important;
}
.pa-sponsor-program-picker-field{
  padding:16px;
  border:1px solid #dcdcde;
  border-radius:10px;
  background:#fff;
}
.pa-sponsor-program-picker-field .pa-field-heading{
  margin:0 0 6px!important;
  font-size:16px;
  line-height:1.3;
}
.pa-sponsor-program-picker-field > .description{
  margin:0 0 12px!important;
  max-width:760px;
  font-size:13px;
  line-height:1.45;
  color:#646970;
}
.pa-sponsor-program-toolbar{
  display:grid;
  grid-template-columns:minmax(260px,1fr) auto;
  gap:10px;
  align-items:center;
  margin:0 0 10px!important;
}
.pa-sponsor-program-toolbar .pa-sponsor-program-search{
  width:100%;
  min-height:36px;
  margin:0!important;
}
.pa-sponsor-program-toolbar .button{
  white-space:nowrap;
}
.pa-sponsor-program-picker{
  border:1px solid #dcdcde;
  border-radius:8px;
  padding:10px 12px;
  max-height:150px;
  overflow:auto;
  background:#fbfbfc;
}
.pa-sponsor-program-picker label{
  display:flex;
  align-items:center;
  gap:7px;
  margin:0 0 8px!important;
  font-weight:400!important;
  line-height:1.35;
}
.pa-sponsor-program-picker label:last-child{
  margin-bottom:0!important;
}
.pa-selected-sponsor-programs{
  margin:12px 0 0!important;
  padding:0;
  list-style:none;
  display:grid;
  gap:10px;
}
.pa-selected-sponsor-programs:empty::before{
  content:attr(data-empty);
  display:block;
  padding:10px 12px;
  border:1px dashed #c3c4c7;
  border-radius:8px;
  color:#646970;
  background:#fbfbfc;
}
.pa-selected-sponsor-programs li{
  margin:0!important;
  padding:12px;
  border:1px solid #dcdcde;
  border-radius:8px;
  background:#fbfbfc;
}
.pa-sponsor-program-row-head{
  display:flex;
  align-items:center;
  justify-content:space-between;
  gap:12px;
  margin-bottom:10px;
}
.pa-sponsor-program-levels{
  display:flex;
  flex-wrap:wrap;
  gap:8px 10px;
  align-items:center;
}
.pa-sponsor-program-level-heading{
  flex-basis:100%;
  display:block;
  margin-bottom:2px;
  font-size:12px;
  font-weight:600;
  color:#50575e;
}
.pa-sponsor-program-levels label{
  display:inline-flex!important;
  align-items:center;
  gap:6px;
  margin:0!important;
  padding:6px 10px;
  border:1px solid #dcdcde;
  border-radius:999px;
  background:#fff;
  font-weight:400!important;
  line-height:1.2;
}
.pa-sponsor-form .pa-editor-field{
  padding:16px;
  border:1px solid #dcdcde;
  border-radius:10px;
  background:#fff;
}
.pa-sponsor-form .pa-editor-field > label{
  margin:0 0 6px!important;
  font-size:16px;
  font-weight:600;
  line-height:1.3;
}
.pa-sponsor-form .pa-editor-field > .description{
  margin:0 0 12px!important;
  color:#646970;
}
.pa-sponsor-form .wp-editor-wrap{
  margin-top:0;
}
.pa-sponsor-form .pa-form-actions{
  margin:4px 0 0!important;
}
@media(max-width:900px){
  .pa-sponsor-logo-website-row,
  .pa-sponsor-program-toolbar{
    grid-template-columns:1fr;
  }
  .pa-sponsor-program-toolbar .button{
    justify-self:start;
  }
}
'''

if marker not in text:
    text = text.rstrip() + '\n\n' + css.strip() + '\n'

ADMIN_CSS.write_text(text)
print('Applied sponsor form UI cleanup CSS.')
