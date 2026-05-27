from pathlib import Path

PHP = Path('program-agenda/program-agenda.php')
JS = Path('program-agenda/assets/js/admin.js')
CSS = Path('program-agenda/assets/css/admin.css')

php = PHP.read_text()
helper_marker = "    private function sponsor_program_titles($sponsor_id) {\n        $titles = [];\n        foreach ($this->sponsor_program_ids($sponsor_id) as $program_id) {\n            $title = get_the_title($program_id);\n            if ($title) { $titles[] = $title; }\n        }\n        return $titles;\n    }\n"
helper_insert = helper_marker + r'''

    private function speaker_event_ids($speaker_id) {
        $speaker_id = absint($speaker_id);
        if (!$speaker_id) { return []; }
        $events = get_posts([
            'post_type' => 'pa_event',
            'post_status' => ['publish','draft'],
            'numberposts' => -1,
            'meta_key' => '_pa_event_date',
            'orderby' => 'meta_value',
            'order' => 'ASC',
        ]);
        $ids = [];
        foreach ($events as $event) {
            $speaker_ids = get_post_meta($event->ID, '_pa_speaker_ids', true);
            if (!is_array($speaker_ids)) { $speaker_ids = []; }
            if (in_array($speaker_id, array_map('absint', $speaker_ids), true)) { $ids[] = absint($event->ID); }
        }
        return $ids;
    }

    private function speaker_event_picker_label($event_id) {
        $event = get_post($event_id);
        if (!$event || $event->post_type !== 'pa_event') { return ''; }
        $parts = [$event->post_title];
        $when = $this->format_event_when($event_id);
        if ($when) { $parts[] = $when; }
        $program_id = absint(get_post_meta($event_id, '_pa_program_id', true));
        $program_title = $program_id ? get_the_title($program_id) : '';
        if ($program_title) { $parts[] = $program_title; }
        return implode(' — ', array_filter($parts));
    }

    private function sync_speaker_events($speaker_id, $selected_event_ids) {
        $speaker_id = absint($speaker_id);
        if (!$speaker_id) { return; }
        $selected_event_ids = array_values(array_filter(array_unique(array_map('absint', (array)$selected_event_ids))));
        $selected_event_ids = array_values(array_filter($selected_event_ids, static function($event_id) { return get_post_type($event_id) === 'pa_event'; }));
        $selected_lookup = array_fill_keys($selected_event_ids, true);

        $events = get_posts([
            'post_type' => 'pa_event',
            'post_status' => ['publish','draft'],
            'numberposts' => -1,
            'orderby' => 'date',
            'order' => 'DESC',
        ]);
        foreach ($events as $event) {
            $event_id = absint($event->ID);
            $speaker_ids = get_post_meta($event_id, '_pa_speaker_ids', true);
            if (!is_array($speaker_ids)) { $speaker_ids = []; }
            $speaker_ids = array_values(array_filter(array_unique(array_map('absint', $speaker_ids))));
            $currently_attached = in_array($speaker_id, $speaker_ids, true);
            $should_attach = isset($selected_lookup[$event_id]);

            if ($should_attach && !$currently_attached) {
                $speaker_ids[] = $speaker_id;
                update_post_meta($event_id, '_pa_speaker_ids', $speaker_ids);
            } elseif (!$should_attach && $currently_attached) {
                $speaker_ids = array_values(array_filter($speaker_ids, static function($id) use ($speaker_id) { return absint($id) !== $speaker_id; }));
                update_post_meta($event_id, '_pa_speaker_ids', $speaker_ids);
            }
        }
    }
'''
if 'private function speaker_event_ids(' not in php:
    if helper_marker not in php:
        raise SystemExit('Could not find sponsor_program_titles marker.')
    php = php.replace(helper_marker, helper_insert, 1)

form_marker = "        echo '<div class=\"pa-inline-fields pa-two-fields\"><label class=\"pa-field\">LinkedIn<input type=\"url\" name=\"linkedin\" value=\"' . esc_attr($id ? get_post_meta($id, '_pa_speaker_linkedin', true) : '') . '\"></label>';\n        echo '<label class=\"pa-field\">Website<input type=\"url\" name=\"website\" value=\"' . esc_attr($id ? get_post_meta($id, '_pa_speaker_website', true) : '') . '\"></label></div>';\n"
event_picker = form_marker + r'''        $selected_event_ids = $id ? $this->speaker_event_ids($id) : [];
        $events_for_speaker = get_posts(['post_type'=>'pa_event','post_status'=>['publish','draft'],'numberposts'=>-1,'meta_key'=>'_pa_event_date','orderby'=>'meta_value','order'=>'ASC']);
        echo '<section class="pa-field pa-speaker-event-picker-field"><h3 class="pa-field-heading">Events</h3><p class="description">Searchable and multi-selectable. Selected events are automatically sorted by event date.</p><div class="pa-speaker-event-toolbar"><input type="search" class="pa-speaker-event-search" placeholder="Search events by title, program, date, category, or location"><button type="button" class="button pa-select-all-speaker-events">Select all visible</button></div><div class="pa-speaker-event-picker">';
        foreach ($events_for_speaker as $event_for_speaker) {
            $event_program_id = absint(get_post_meta($event_for_speaker->ID, '_pa_program_id', true));
            $event_program_title = $event_program_id ? get_the_title($event_program_id) : '';
            $event_when = $this->format_event_when($event_for_speaker->ID);
            $event_category = get_post_meta($event_for_speaker->ID, '_pa_event_category', true);
            $event_location = get_post_meta($event_for_speaker->ID, '_pa_event_location', true);
            $event_label = $this->speaker_event_picker_label($event_for_speaker->ID);
            $event_search_terms = strtolower(trim($event_for_speaker->post_title . ' ' . $event_program_title . ' ' . $event_when . ' ' . $event_category . ' ' . $event_location));
            echo '<label data-name="' . esc_attr($event_search_terms) . '"><input type="checkbox" class="pa-speaker-event-check" name="speaker_event_ids[]" value="' . esc_attr($event_for_speaker->ID) . '" ' . checked(in_array(absint($event_for_speaker->ID), array_map('intval', $selected_event_ids), true), true, false) . '> ' . esc_html($event_label) . '</label>';
        }
        echo '</div><ul class="pa-selected-speaker-events" data-empty="No events selected.">';
        foreach ($selected_event_ids as $selected_event_id) {
            $selected_event_label = $this->speaker_event_picker_label($selected_event_id);
            if ($selected_event_label) { echo '<li data-id="' . esc_attr($selected_event_id) . '"><span class="pa-selected-speaker-event-name">' . esc_html($selected_event_label) . '</span><button type="button" class="button-link pa-remove-speaker-event">Remove</button></li>'; }
        }
        echo '</ul></section>';
'''
if 'pa-speaker-event-picker-field' not in php:
    if form_marker not in php:
        raise SystemExit('Could not find speaker website field marker.')
    php = php.replace(form_marker, event_picker, 1)

save_marker = "        update_post_meta($new_id, '_pa_speaker_style_program_id', absint($_POST['speaker_style_program_id'] ?? 0));\n        wp_safe_redirect(admin_url('admin.php?page=program-edit-speaker&id=' . $new_id . '&saved=1')); exit;\n"
save_replace = "        update_post_meta($new_id, '_pa_speaker_style_program_id', absint($_POST['speaker_style_program_id'] ?? 0));\n        $selected_event_ids = array_values(array_filter(array_unique(array_map('absint', (array)($_POST['speaker_event_ids'] ?? [])))));\n        $this->sync_speaker_events($new_id, $selected_event_ids);\n        wp_safe_redirect(admin_url('admin.php?page=program-edit-speaker&id=' . $new_id . '&saved=1')); exit;\n"
if 'sync_speaker_events($new_id' not in php:
    if save_marker not in php:
        raise SystemExit('Could not find save_speaker marker.')
    php = php.replace(save_marker, save_replace, 1)
PHP.write_text(php)

js = JS.read_text()
js_marker = "  $(document).on('click','.pa-move-speaker-down',function(e){e.preventDefault();var $li=$(this).closest('li'),$next=$li.next('li'); if($next.length){$li.insertAfter($next); updateSpeakerOrder();}});\n"
js_insert = js_marker + r'''

  $(document).on('input','.pa-speaker-event-search',function(){
    var q=String($(this).val()||'').toLowerCase();
    $('.pa-speaker-event-picker label').each(function(){
      var terms=String($(this).data('name')||'').toLowerCase();
      $(this).toggle(terms.indexOf(q)!==-1);
    });
  });
  $(document).on('change','.pa-speaker-event-check',function(){
    var id=$(this).val(), name=$(this).closest('label').text().trim(), $list=$('.pa-selected-speaker-events');
    if(this.checked){
      if(!$list.find('li[data-id="'+id+'"]').length){
        $list.append('<li data-id="'+id+'"><span class="pa-selected-speaker-event-name">'+name+'</span><button type="button" class="button-link pa-remove-speaker-event">Remove</button></li>');
      }
    } else {
      $list.find('li[data-id="'+id+'"]').remove();
    }
  });
  $(document).on('click','.pa-remove-speaker-event',function(e){
    e.preventDefault();
    var id=$(this).closest('li').data('id');
    $('.pa-speaker-event-check[value="'+id+'"]').prop('checked',false);
    $(this).closest('li').remove();
  });
  $(document).on('click','.pa-select-all-speaker-events',function(e){
    e.preventDefault();
    $('.pa-speaker-event-picker label:visible .pa-speaker-event-check').each(function(){
      if(!this.checked){ $(this).prop('checked',true).trigger('change'); }
    });
  });
'''
if 'pa-speaker-event-search' not in js:
    if js_marker not in js:
        raise SystemExit('Could not find speaker JS marker.')
    js = js.replace(js_marker, js_insert, 1)
JS.write_text(js)

css = CSS.read_text()
css_marker = '/* Stagecard speaker event picker */'
css_block = r'''
/* Stagecard speaker event picker */
.pa-speaker-event-picker-field{
  border:1px solid #dcdcde;
  border-radius:10px;
  padding:16px;
  background:#fff;
}
.pa-speaker-event-picker-field .pa-field-heading{
  margin:0 0 6px!important;
  font-size:16px;
  line-height:1.3;
}
.pa-speaker-event-picker-field > .description{
  margin:0 0 12px!important;
  color:#646970;
  font-size:13px;
  line-height:1.45;
}
.pa-speaker-event-toolbar{
  display:flex;
  gap:12px;
  align-items:center;
  margin:10px 0;
}
.pa-speaker-event-toolbar input[type=search]{
  flex:1;
  min-height:36px;
}
.pa-speaker-event-picker{
  border:1px solid #dcdcde;
  border-radius:8px;
  padding:10px;
  max-height:190px;
  overflow:auto;
  background:#fbfbfc;
  margin:10px 0;
}
.pa-speaker-event-picker label{
  display:block;
  margin:6px 0!important;
  font-weight:400!important;
  line-height:1.35;
}
.pa-selected-speaker-events{
  border:1px dashed #c3c4c7;
  border-radius:8px;
  padding:10px;
  min-height:40px;
  background:#fbfbfc;
  margin:10px 0 0!important;
}
.pa-selected-speaker-events:empty::before{
  content:attr(data-empty);
  color:#646970;
  font-style:italic;
}
.pa-selected-speaker-events li{
  display:flex;
  justify-content:space-between;
  align-items:center;
  gap:12px;
  background:#fff;
  border:1px solid #dcdcde;
  border-radius:6px;
  padding:8px 10px;
  margin:0 0 8px;
}
.pa-selected-speaker-events li:last-child{margin-bottom:0;}
.pa-selected-speaker-event-name{min-width:0;overflow-wrap:anywhere;}
@media (max-width:782px){
  .pa-selected-speaker-events li{align-items:flex-start;flex-direction:column;}
  .pa-speaker-event-toolbar{align-items:stretch;flex-direction:column;}
  .pa-speaker-event-toolbar .button{width:fit-content;}
}
'''
if css_marker not in css:
    css = css.rstrip() + '\n\n' + css_block.strip() + '\n'
CSS.write_text(css)

print('Applied speaker event picker support.')
