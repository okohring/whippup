from pathlib import Path

PHP = Path('program-agenda/program-agenda.php')
JS = Path('program-agenda/assets/js/admin.js')
ADMIN_CSS = Path('program-agenda/assets/css/admin.css')
PUBLIC_CSS = Path('program-agenda/assets/css/public.css')

php = PHP.read_text()

# The agenda event card renderer receives $event, not $post. If $post->ID is used
# here, the event-specific speaker category meta is never found on public cards.
php = php.replace(
    "$this->speaker_cards($speaker_ids, $program_id, 'agenda', $post->ID)",
    "$this->speaker_cards($speaker_ids, $program_id, 'agenda', $event->ID)",
)

PHP.write_text(php)

js = JS.read_text()

# Make sure newly selected speakers receive the category dropdown. A previous
# guard could skip this replacement after only the helper function existed.
old_handler = """  $(document).on('change','.pa-speaker-check',function(){
    var id=$(this).val(), name=$(this).closest('label').text().trim(), $list=$('.pa-selected-speakers');
    if(this.checked){ if(!$list.find('li[data-id="'+id+'"]').length){$list.append('<li data-id="'+id+'"><span class="pa-selected-speaker-name">'+name+'</span><span class="pa-selected-speaker-actions"><button type="button" class="button-link pa-move-speaker-up" aria-label="Move up" title="Move up"><span aria-hidden="true">▲</span><span class="screen-reader-text">Move up</span></button> <button type="button" class="button-link pa-move-speaker-down" aria-label="Move down" title="Move down"><span aria-hidden="true">▼</span><span class="screen-reader-text">Move down</span></button> <button type="button" class="button-link pa-remove-speaker">Remove</button></span></li>');} }
    else {$list.find('li[data-id="'+id+'"]').remove();}
    updateSpeakerOrder();
  });
"""
new_handler = """  $(document).on('change','.pa-speaker-check',function(){
    var id=$(this).val(), name=$(this).closest('label').text().trim(), $list=$('.pa-selected-speakers');
    if(this.checked){
      if(!$list.find('li[data-id="'+id+'"]').length){
        $list.append('<li data-id="'+id+'"><span class="pa-selected-speaker-name">'+name+'</span>'+speakerCategorySelectHtml(id)+'<span class="pa-selected-speaker-actions"><button type="button" class="button-link pa-move-speaker-up" aria-label="Move up" title="Move up"><span aria-hidden="true">▲</span><span class="screen-reader-text">Move up</span></button> <button type="button" class="button-link pa-move-speaker-down" aria-label="Move down" title="Move down"><span aria-hidden="true">▼</span><span class="screen-reader-text">Move down</span></button> <button type="button" class="button-link pa-remove-speaker">Remove</button></span></li>');
      }
    }
    else {$list.find('li[data-id="'+id+'"]').remove();}
    updateSpeakerOrder();
  });
"""
if old_handler in js:
    js = js.replace(old_handler, new_handler, 1)

JS.write_text(js)

admin_css = ADMIN_CSS.read_text()
stacked_admin = '''
/* Stagecard speaker category stacked admin layout */
.pa-program-category-columns{
  display:block!important;
  margin:20px 0 26px!important;
}
.pa-program-category-column{
  box-sizing:border-box!important;
  width:100%!important;
  max-width:none!important;
  margin:0 0 24px!important;
}
.pa-speaker-categories-column{
  max-width:760px!important;
}
.pa-speaker-category-row{
  max-width:620px!important;
}
'''
if '/* Stagecard speaker category stacked admin layout */' not in admin_css:
    admin_css += '\n' + stacked_admin
ADMIN_CSS.write_text(admin_css)

public_css = PUBLIC_CSS.read_text()
public_guard = '''
/* Stagecard speaker category public visibility guard */
.pa-event-card .pa-speaker-card-category-label,
.pa-single-event .pa-speaker-card-category-label{
  display:block!important;
  visibility:visible!important;
}
.pa-event-card .pa-speaker-card--categorized,
.pa-single-event .pa-speaker-card--categorized{
  border:1px solid var(--pa-agenda-bar-color,var(--pa-agenda-accent-color,currentColor))!important;
}
'''
if '/* Stagecard speaker category public visibility guard */' not in public_css:
    public_css += '\n' + public_guard
PUBLIC_CSS.write_text(public_css)

print('Fixed speaker category public rendering and stacked admin category layout.')
