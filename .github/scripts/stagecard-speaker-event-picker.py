from pathlib import Path

PHP = Path('program-agenda/program-agenda.php')
JS = Path('program-agenda/assets/js/admin.js')
ADMIN_CSS = Path('program-agenda/assets/css/admin.css')
PUBLIC_CSS = Path('program-agenda/assets/css/public.css')

php = PHP.read_text()

# Agenda cards use $event. Single event pages use $post.
php = php.replace(
    "if ($card_size !== 'thin' && $speaker_ids) { echo '<div class=\"pa-event-card__speakers\">' . $this->speaker_cards($speaker_ids, $program_id, 'agenda', $post->ID) . '</div>'; }",
    "if ($card_size !== 'thin' && $speaker_ids) { echo '<div class=\"pa-event-card__speakers\">' . $this->speaker_cards($speaker_ids, $program_id, 'agenda', $event->ID) . '</div>'; }",
)
php = php.replace(
    "echo '<div class=\"pa-event-single-speakers\"><h4>Speakers</h4>' . $this->speaker_cards($speaker_ids, $program_id, 'agenda', $event->ID) . '</div>';",
    "echo '<div class=\"pa-event-single-speakers\"><h4>Speakers</h4>' . $this->speaker_cards($speaker_ids, $program_id, 'event-page', $post->ID) . '</div>';",
)

old_single = """        $speaker_ids = get_post_meta($post->ID, '_pa_speaker_ids', true);
        if (is_array($speaker_ids) && $speaker_ids) {
            $event_speaker_categories = get_post_meta($post->ID, '_pa_event_speaker_categories', true);
            if (!is_array($event_speaker_categories)) { $event_speaker_categories = []; }
            $has_speaker_categories = count(array_filter(array_map('trim', $event_speaker_categories))) > 0;
            echo '<div class=\"pa-event-single-speakers' . ($has_speaker_categories ? ' pa-event-single-speakers--categorized' : '') . '\"><h4>Speakers</h4>' . $this->speaker_cards($speaker_ids, $program_id, 'event-page', $post->ID) . '</div>';
        }
"""
new_single = """        $speaker_ids = get_post_meta($post->ID, '_pa_speaker_ids', true);
        if (is_array($speaker_ids) && $speaker_ids) {
            echo $this->single_event_speaker_sections($speaker_ids, $program_id, $post->ID);
        }
"""
if old_single in php:
    php = php.replace(old_single, new_single, 1)

old_single_2 = """        $speaker_ids = get_post_meta($post->ID, '_pa_speaker_ids', true);
        if (is_array($speaker_ids) && $speaker_ids) {
            echo '<div class=\"pa-event-single-speakers\"><h4>Speakers</h4>' . $this->speaker_cards($speaker_ids, $program_id, 'agenda', $post->ID) . '</div>';
        }
"""
if old_single_2 in php:
    php = php.replace(old_single_2, new_single, 1)

section_method = r'''    private function single_event_speaker_sections($speaker_ids, $program_id, $event_id) {
        $speaker_ids = array_values(array_filter(array_map('absint', (array)$speaker_ids)));
        if (!$speaker_ids) { return ''; }

        $event_speaker_categories = get_post_meta(absint($event_id), '_pa_event_speaker_categories', true);
        if (!is_array($event_speaker_categories)) { $event_speaker_categories = []; }

        $category_groups = [];
        $default_ids = [];
        foreach ($speaker_ids as $speaker_id) {
            $speaker = get_post($speaker_id);
            if (!$speaker || $speaker->post_type !== 'pa_speaker') { continue; }
            $category = '';
            foreach ([$speaker_id, (string)$speaker_id] as $key) {
                if (isset($event_speaker_categories[$key])) { $category = trim(sanitize_text_field($event_speaker_categories[$key])); break; }
            }
            if ($category !== '') {
                if (!isset($category_groups[$category])) { $category_groups[$category] = []; }
                $category_groups[$category][] = $speaker_id;
            } else {
                $default_ids[] = $speaker_id;
            }
        }

        if (!$category_groups) {
            return '<div class="pa-event-single-speakers"><h4>Speakers</h4>' . $this->speaker_cards($speaker_ids, $program_id, 'event-page-default', 0) . '</div>';
        }

        ob_start();
        echo '<div class="pa-single-event-speaker-sections' . (!$default_ids ? ' pa-single-event-speaker-sections--only-categorized' : '') . '">';
        echo '<div class="pa-single-event-speaker-section-list pa-single-event-speaker-section-list--categorized">';
        foreach ($category_groups as $category => $ids) {
            echo '<section class="pa-single-event-speaker-section pa-single-event-speaker-section--categorized"><h4 class="pa-single-event-speaker-section-heading">' . esc_html($category) . '</h4>' . $this->speaker_cards($ids, $program_id, 'event-page-category', $event_id) . '</section>';
        }
        echo '</div>';
        if ($default_ids) {
            echo '<section class="pa-single-event-speaker-section pa-single-event-speaker-section--default"><h4 class="pa-single-event-speaker-section-heading">Speakers</h4>' . $this->speaker_cards($default_ids, $program_id, 'event-page-default', 0) . '</section>';
        }
        echo '</div>';
        return ob_get_clean();
    }

'''
if 'private function single_event_speaker_sections(' not in php:
    php = php.replace('    private function single_speaker($post) {\n', section_method + '    private function single_speaker($post) {\n', 1)

old_split_1 = """        if ($categorized_cards && $default_cards) {
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
new_split = """        if ($categorized_cards && $default_cards) {
            echo '<div class=\"pa-speaker-card-column pa-speaker-card-column--categorized\">' . implode('', $categorized_cards) . '</div>';
            echo '<div class=\"pa-speaker-card-column pa-speaker-card-column--default\">' . implode('', $default_cards) . '</div>';
        } else {
            echo implode('', array_merge($categorized_cards, $default_cards));
        }
"""
if old_split_1 in php:
    php = php.replace(old_split_1, new_split, 1)
PHP.write_text(php)

js = JS.read_text()
if 'function speakerCategorySelectHtml' not in js:
    marker = "  function updateSpeakerOrder(){var ids=[];$('.pa-selected-speakers li').each(function(){ids.push($(this).data('id'));});$('.pa-speaker-order').val(ids.join(','));}\n"
    js = js.replace(marker, marker + "  function speakerCategorySelectHtml(id){var html=$('#pa-speaker-category-select-template').html()||''; return html.replace(/__SPEAKER_ID__/g,id);}\n", 1)
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
if '/* Stagecard speaker category stacked admin layout */' not in admin_css:
    admin_css += '\n/* Stagecard speaker category stacked admin layout */\n.pa-program-category-columns{display:block!important;margin:20px 0 26px!important;}\n.pa-program-category-column{box-sizing:border-box!important;width:100%!important;max-width:none!important;margin:0 0 24px!important;}\n.pa-speaker-categories-column{max-width:760px!important;}\n.pa-speaker-category-row{max-width:620px!important;}\n'
ADMIN_CSS.write_text(admin_css)

public_css = PUBLIC_CSS.read_text()
root_css = '''
/* Stagecard root single Event speaker section layout */
.pa-single-event-speaker-sections{display:grid!important;grid-template-columns:minmax(0,1fr) minmax(0,1fr)!important;gap:clamp(28px,6vw,72px)!important;align-items:start!important;margin-top:2.2rem!important;}
.pa-single-event-speaker-sections--only-categorized{grid-template-columns:1fr!important;}
.pa-single-event-speaker-section-list--categorized{display:flex!important;flex-direction:column!important;gap:28px!important;min-width:0!important;}
.pa-single-event-speaker-section{min-width:0!important;}
.pa-single-event-speaker-section--default{border-left:1px solid currentColor!important;padding-left:clamp(22px,4vw,44px)!important;}
.pa-single-event-speaker-section-heading{display:block!important;width:100%!important;margin:0 0 12px!important;font-size:.82rem!important;line-height:1.2!important;font-weight:700!important;text-transform:uppercase!important;letter-spacing:.04em!important;color:inherit!important;}
.pa-single-event-speaker-section .pa-speaker-card-list{display:grid!important;grid-template-columns:repeat(2,minmax(0,max-content))!important;gap:12px!important;align-items:start!important;justify-items:start!important;overflow:visible!important;}
.pa-single-event-speaker-section .pa-speaker-card-unit{padding-top:0!important;align-self:start!important;justify-content:flex-start!important;overflow:visible!important;}
.pa-single-event-speaker-section .pa-speaker-card-category-label{display:none!important;}
@media (max-width:900px){.pa-single-event-speaker-sections{grid-template-columns:1fr!important;}.pa-single-event-speaker-section--default{border-left:0!important;padding-left:0!important;border-top:1px solid currentColor!important;padding-top:22px!important;}.pa-single-event-speaker-section .pa-speaker-card-list{grid-template-columns:1fr!important;}}
'''
if '/* Stagecard root single Event speaker section layout */' not in public_css:
    public_css += '\n' + root_css
agenda_css = '''
/* Stagecard categorized agenda speaker card order */
.pa-event-card .pa-event-card__speakers,.pa-event-card .pa-speaker-card-list,.pa-event-card .pa-speaker-card-column,.pa-event-card .pa-speaker-card-unit{overflow:visible!important;}
.pa-event-card .pa-speaker-card-list-has-categories{align-items:end!important;}
.pa-event-card .pa-speaker-card-column{align-items:end!important;}
.pa-event-card .pa-speaker-card-unit{justify-content:flex-end!important;align-self:end!important;padding-top:14px!important;}
.pa-event-card .pa-speaker-card-category-label{display:block!important;visibility:visible!important;min-height:1em!important;line-height:1.15!important;margin:0 0 5px!important;overflow:visible!important;white-space:nowrap!important;}
.pa-event-card .pa-speaker-card--categorized{border:1px solid var(--pa-agenda-bar-color,var(--pa-agenda-accent-color,currentColor))!important;}
'''
if '/* Stagecard categorized agenda speaker card order */' not in public_css:
    public_css += '\n' + agenda_css
mobile_css = '''
/* Stagecard mobile categorized agenda speaker cards */
@media (max-width:768px){
  .pa-event-card .pa-event-card__body,
  .pa-event-card.pa-event-card--size-full .pa-event-card__body{min-width:0!important;overflow:hidden!important;}
  .pa-event-card .pa-event-card__speakers{width:100%!important;max-width:100%!important;min-width:0!important;overflow:hidden!important;}
  .pa-event-card .pa-speaker-card-list,
  .pa-event-card .pa-speaker-card-list--categorized-split,
  .pa-event-card .pa-speaker-card-column{display:flex!important;flex-direction:column!important;width:100%!important;max-width:100%!important;min-width:0!important;gap:10px!important;align-items:stretch!important;overflow:hidden!important;}
  .pa-event-card .pa-speaker-card-unit{width:100%!important;max-width:100%!important;min-width:0!important;padding-top:0!important;align-self:stretch!important;overflow:hidden!important;}
  .pa-event-card .pa-speaker-card-category-label{white-space:normal!important;overflow:visible!important;margin:0 0 4px!important;}
  .pa-event-card .pa-speaker-card{width:100%!important;max-width:100%!important;min-width:0!important;box-sizing:border-box!important;overflow:hidden!important;}
  .pa-event-card .pa-speaker-card-text,
  .pa-event-card .pa-speaker-card-text h3,
  .pa-event-card .pa-speaker-card-text p,
  .pa-event-card .pa-speaker-card-text a{min-width:0!important;max-width:100%!important;overflow-wrap:anywhere!important;word-break:normal!important;}
}
'''
if '/* Stagecard mobile categorized agenda speaker cards */' not in public_css:
    public_css += '\n' + mobile_css
spacing_css = '''
/* Stagecard event info to speaker card spacing */
.pa-event-card .pa-event-card__speakers{margin-top:6px!important;}
.pa-event-card .pa-event-card__speakers .pa-speaker-card-list{margin-top:0!important;}
.pa-event-card .pa-speaker-card-unit{padding-top:7px!important;}
@media (max-width:768px){
  .pa-event-card .pa-event-card__speakers{margin-top:6px!important;}
  .pa-event-card .pa-speaker-card-unit{padding-top:0!important;}
}
'''
if '/* Stagecard event info to speaker card spacing */' not in public_css:
    public_css += '\n' + spacing_css
consistency_css = '''
/* Stagecard speaker card consistency and compact spacing */
.pa-event-card .pa-event-card__speakers{margin-top:0!important;}
.pa-event-card .pa-event-card__speakers .pa-speaker-card-list{margin-top:0!important;}
.pa-event-card .pa-speaker-card-unit{padding-top:3px!important;gap:3px!important;}
.pa-event-card .pa-speaker-card-category-label{margin:0 0 3px!important;line-height:1.05!important;}
.pa-event-card .pa-speaker-card,
.pa-single-event-speaker-section .pa-speaker-card{font-size:.78rem!important;line-height:1.18!important;}
.pa-event-card .pa-speaker-card-text h3,
.pa-event-card .pa-speaker-card-text h3 a,
.pa-single-event-speaker-section .pa-speaker-card-text h3,
.pa-single-event-speaker-section .pa-speaker-card-text h3 a{font-size:.82rem!important;line-height:1.1!important;margin:0 0 2px!important;}
.pa-event-card .pa-speaker-card-role,
.pa-event-card .pa-speaker-card-company,
.pa-single-event-speaker-section .pa-speaker-card-role,
.pa-single-event-speaker-section .pa-speaker-card-company{font-size:.74rem!important;line-height:1.15!important;margin:0!important;}
.pa-event-card .pa-speaker-card-image,
.pa-single-event-speaker-section .pa-speaker-card-image{width:40px!important;height:40px!important;min-width:40px!important;max-width:40px!important;min-height:40px!important;max-height:40px!important;flex:0 0 40px!important;}
.pa-event-card .pa-speaker-card-thumb,
.pa-event-card .pa-speaker-card-image img,
.pa-single-event-speaker-section .pa-speaker-card-thumb,
.pa-single-event-speaker-section .pa-speaker-card-image img{width:100%!important;height:100%!important;max-width:100%!important;max-height:100%!important;object-fit:cover!important;}
@media (max-width:768px){
  .pa-event-card .pa-event-card__speakers{margin-top:0!important;}
  .pa-event-card .pa-speaker-card-unit{padding-top:0!important;gap:3px!important;}
}
'''
if '/* Stagecard speaker card consistency and compact spacing */' not in public_css:
    public_css += '\n' + consistency_css
PUBLIC_CSS.write_text(public_css)

print('Applied speaker card consistency and compact event-card spacing.')
