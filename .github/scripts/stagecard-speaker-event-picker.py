from pathlib import Path

PHP = Path('program-agenda/program-agenda.php')
JS = Path('program-agenda/assets/js/admin.js')
ADMIN_CSS = Path('program-agenda/assets/css/admin.css')
PUBLIC_CSS = Path('program-agenda/assets/css/public.css')

php = PHP.read_text()

# Agenda cards are rendered from $event. Single event pages are rendered from $post.
php = php.replace(
    "if ($card_size !== 'thin' && $speaker_ids) { echo '<div class=\"pa-event-card__speakers\">' . $this->speaker_cards($speaker_ids, $program_id, 'agenda', $post->ID) . '</div>'; }",
    "if ($card_size !== 'thin' && $speaker_ids) { echo '<div class=\"pa-event-card__speakers\">' . $this->speaker_cards($speaker_ids, $program_id, 'agenda', $event->ID) . '</div>'; }",
)
php = php.replace(
    "echo '<div class=\"pa-event-single-speakers\"><h4>Speakers</h4>' . $this->speaker_cards($speaker_ids, $program_id, 'agenda', $event->ID) . '</div>';",
    "echo '<div class=\"pa-event-single-speakers\"><h4>Speakers</h4>' . $this->speaker_cards($speaker_ids, $program_id, 'event-page', $post->ID) . '</div>';",
)
php = php.replace(
    "echo '<div class=\"pa-event-single-speakers\"><h4>Speakers</h4>' . $this->speaker_cards($speaker_ids, $program_id, 'agenda', $post->ID) . '</div>';",
    "echo '<div class=\"pa-event-single-speakers\"><h4>Speakers</h4>' . $this->speaker_cards($speaker_ids, $program_id, 'event-page', $post->ID) . '</div>';",
)

old_split = """        if ($categorized_cards && $default_cards) {
            echo '<div class=\"pa-speaker-card-column pa-speaker-card-column--default\">' . implode('', $default_cards) . '</div>';
            echo '<div class=\"pa-speaker-card-column pa-speaker-card-column--categorized\">' . implode('', $categorized_cards) . '</div>';
        } else {
            echo implode('', array_merge($default_cards, $categorized_cards));
        }
"""
new_split = """        if ($categorized_cards && $default_cards) {
            if ($context === 'event-page') {
                echo '<div class=\"pa-speaker-card-column pa-speaker-card-column--categorized\"><h5 class=\"pa-speaker-card-column-heading pa-speaker-card-column-heading--category\">Speaker Category</h5>' . implode('', $categorized_cards) . '</div>';
                echo '<div class=\"pa-speaker-card-column pa-speaker-card-column--default\"><h5 class=\"pa-speaker-card-column-heading pa-speaker-card-column-heading--speakers\">Speakers</h5>' . implode('', $default_cards) . '</div>';
            } else {
                echo '<div class=\"pa-speaker-card-column pa-speaker-card-column--categorized\">' . implode('', $categorized_cards) . '</div>';
                echo '<div class=\"pa-speaker-card-column pa-speaker-card-column--default\">' . implode('', $default_cards) . '</div>';
            }
        } else {
            echo implode('', array_merge($categorized_cards, $default_cards));
        }
"""
if old_split in php:
    php = php.replace(old_split, new_split, 1)

old_existing_split = """        if ($categorized_cards && $default_cards) {
            if ($context === 'event-page') {
                echo '<div class=\"pa-speaker-card-column pa-speaker-card-column--categorized\"><h5 class=\"pa-speaker-card-column-heading pa-speaker-card-column-heading--category\">Speaker Category</h5>' . implode('', $categorized_cards) . '</div>';
                echo '<div class=\"pa-speaker-card-column pa-speaker-card-column--default\"><h5 class=\"pa-speaker-card-column-heading pa-speaker-card-column-heading--speakers\">Speakers</h5>' . implode('', $default_cards) . '</div>';
            } else {
                echo '<div class=\"pa-speaker-card-column pa-speaker-card-column--default\">' . implode('', $default_cards) . '</div>';
                echo '<div class=\"pa-speaker-card-column pa-speaker-card-column--categorized\">' . implode('', $categorized_cards) . '</div>';
            }
        } else {
            echo implode('', array_merge($default_cards, $categorized_cards));
        }
"""
if old_existing_split in php:
    php = php.replace(old_existing_split, new_split, 1)

php = php.replace('class=\"pa-speaker-card-column-heading\">Speaker Category</h5>', 'class=\"pa-speaker-card-column-heading pa-speaker-card-column-heading--category\">Speaker Category</h5>')
php = php.replace('class=\"pa-speaker-card-column-heading\">Speakers</h5>', 'class=\"pa-speaker-card-column-heading pa-speaker-card-column-heading--speakers\">Speakers</h5>')

PHP.write_text(php)

js = JS.read_text()
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
.pa-program-category-columns{display:block!important;margin:20px 0 26px!important;}
.pa-program-category-column{box-sizing:border-box!important;width:100%!important;max-width:none!important;margin:0 0 24px!important;}
.pa-speaker-categories-column{max-width:760px!important;}
.pa-speaker-category-row{max-width:620px!important;}
'''
if '/* Stagecard speaker category stacked admin layout */' not in admin_css:
    admin_css += '\n' + stacked_admin
ADMIN_CSS.write_text(admin_css)

public_css = PUBLIC_CSS.read_text()
public_guard = '''
/* Stagecard speaker category alignment and visibility guard */
.pa-event-card .pa-event-card__speakers,
.pa-event-card .pa-speaker-card-list,
.pa-event-card .pa-speaker-card-column,
.pa-event-card .pa-speaker-card-unit,
.pa-single-event .pa-speaker-card-list,
.pa-single-event .pa-speaker-card-column,
.pa-single-event .pa-speaker-card-unit{overflow:visible!important;}
.pa-event-card .pa-speaker-card-list-has-categories{align-items:end!important;}
.pa-event-card .pa-speaker-card-column{align-items:end!important;}
.pa-event-card .pa-speaker-card-unit{justify-content:flex-end!important;align-self:end!important;padding-top:14px!important;}
.pa-event-card .pa-speaker-card-category-label{display:block!important;visibility:visible!important;min-height:1em!important;line-height:1.15!important;margin:0 0 5px!important;overflow:visible!important;white-space:nowrap!important;}
.pa-event-card .pa-speaker-card--categorized,
.pa-single-event .pa-speaker-card--categorized{border:1px solid var(--pa-agenda-bar-color,var(--pa-agenda-accent-color,currentColor))!important;}
.pa-single-event .pa-speaker-card-list--categorized-split{display:grid!important;grid-template-columns:minmax(0,1fr) minmax(0,1fr)!important;gap:28px!important;align-items:start!important;}
.pa-single-event .pa-speaker-card-column{display:grid!important;grid-template-columns:repeat(2,minmax(0,max-content))!important;gap:12px!important;align-items:start!important;align-content:start!important;}
.pa-single-event .pa-speaker-card-unit{padding-top:0!important;align-self:start!important;justify-content:flex-start!important;}
.pa-single-event .pa-speaker-card-column-heading{margin:0 0 10px!important;font-size:.8rem!important;line-height:1.2!important;text-transform:uppercase!important;letter-spacing:.04em!important;grid-column:1/-1!important;}
.pa-single-event .pa-speaker-card-column-heading--category{display:none!important;}
.pa-single-event .pa-speaker-card-category-label{display:block!important;visibility:visible!important;margin:0 0 10px!important;font-size:.8rem!important;line-height:1.2!important;text-transform:uppercase!important;letter-spacing:.04em!important;white-space:nowrap!important;overflow:visible!important;}
@media (max-width:900px){.pa-single-event .pa-speaker-card-list--categorized-split{grid-template-columns:1fr!important;}.pa-single-event .pa-speaker-card-column{grid-template-columns:1fr!important;}}
'''
if '/* Stagecard speaker category alignment and visibility guard */' not in public_css:
    public_css += '\n' + public_guard

cleanup = '''
/* Stagecard single event speaker category cleanup */
.pa-single-event .pa-speaker-card-column-heading--category{display:none!important;}
.pa-single-event .pa-speaker-card-list--categorized-split{align-items:start!important;}
.pa-single-event .pa-speaker-card-column{align-items:start!important;align-content:start!important;}
.pa-single-event .pa-speaker-card-unit{padding-top:0!important;align-self:start!important;justify-content:flex-start!important;}
.pa-single-event .pa-speaker-card-category-label{margin:0 0 10px!important;font-size:.8rem!important;line-height:1.2!important;text-transform:uppercase!important;letter-spacing:.04em!important;}
'''
if '/* Stagecard single event speaker category cleanup */' not in public_css:
    public_css += '\n' + cleanup
PUBLIC_CSS.write_text(public_css)

print('Shows categorized speakers first on event cards and keeps single event layout clean.')
