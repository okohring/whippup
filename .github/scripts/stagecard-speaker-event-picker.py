from pathlib import Path
import re

PHP = Path('program-agenda/program-agenda.php')
JS = Path('program-agenda/assets/js/admin.js')
ADMIN_CSS = Path('program-agenda/assets/css/admin.css')
PUBLIC_CSS = Path('program-agenda/assets/css/public.css')

php = PHP.read_text()

# Program form: load speaker categories beside event categories.
old = "        $categories = $id ? get_post_meta($id, '_pa_categories', true) : [];\n        $all_categories_same = $id ? get_post_meta($id, '_pa_categories_all_same', true) : '';\n        if (!is_array($categories)) { $categories = []; }\n"
new = old + "        $speaker_categories = $id ? get_post_meta($id, '_pa_speaker_categories', true) : [];\n        if (!is_array($speaker_categories)) { $speaker_categories = []; }\n"
if "_pa_speaker_categories" not in php.split('public function form_program()', 1)[1].split('private function program_style_copy_control', 1)[0]:
    php = php.replace(old, new, 1)

old = """        echo '<h3>Categories</h3><p class=\"description\">Category colors and icons are intentional design settings. If no color is chosen, black is used.</p>';
        echo '<label class=\"pa-field pa-checkbox-field pa-all-categories-same-field\"><input type=\"checkbox\" name=\"categories_all_same\" value=\"1\" class=\"pa-all-categories-same\" ' . checked($all_categories_same, '1', false) . '> All categories have same settings</label>';
        echo '<div id=\"pa-categories\">';
        if (!$categories) { $categories = [['name'=>'','color'=>'#000000','icon'=>'none']]; }
        foreach ($categories as $i => $cat) { $this->category_row($i, $cat); }
        echo '</div><button type=\"button\" class=\"button pa-add-category\">Add category</button>';
        echo '<template id=\"pa-category-template\">'; $this->category_row('__INDEX__', ['name'=>'','color'=>'#000000','icon'=>'none']); echo '</template>';
"""
new = """        echo '<section class=\"pa-program-category-columns\"><div class=\"pa-program-category-column pa-event-categories-column\"><h3>Event Categories</h3><p class=\"description\">Category colors and icons are intentional design settings. If no color is chosen, black is used.</p>';
        echo '<label class=\"pa-field pa-checkbox-field pa-all-categories-same-field\"><input type=\"checkbox\" name=\"categories_all_same\" value=\"1\" class=\"pa-all-categories-same\" ' . checked($all_categories_same, '1', false) . '> All event categories have same settings</label>';
        echo '<div id=\"pa-categories\">';
        if (!$categories) { $categories = [['name'=>'','color'=>'#000000','icon'=>'none']]; }
        foreach ($categories as $i => $cat) { $this->category_row($i, $cat); }
        echo '</div><button type=\"button\" class=\"button pa-add-category\">Add event category</button>';
        echo '<template id=\"pa-category-template\">'; $this->category_row('__INDEX__', ['name'=>'','color'=>'#000000','icon'=>'none']); echo '</template></div>';
        echo '<div class=\"pa-program-category-column pa-speaker-categories-column\"><h3>Speaker Categories</h3><p class=\"description\">Optional labels such as Moderator, Host, Panelist, or Featured Speaker. These appear above selected speaker cards.</p><div id=\"pa-speaker-categories\">';
        if (!$speaker_categories) { $speaker_categories = [['name'=>'']]; }
        foreach ($speaker_categories as $i => $speaker_category) { $this->speaker_category_row($i, $speaker_category); }
        echo '</div><button type=\"button\" class=\"button pa-add-speaker-category\">Add speaker category</button>';
        echo '<template id=\"pa-speaker-category-template\">'; $this->speaker_category_row('__INDEX__', ['name'=>'']); echo '</template></div></section>';
"""
if 'pa-program-category-columns' not in php:
    php = php.replace(old, new, 1)

old = "        update_post_meta($new_id, '_pa_categories', $cats);\n"
new = old + "        $speaker_categories = [];\n        foreach ((array)($_POST['speaker_categories'] ?? []) as $speaker_category) {\n            $speaker_category_name = sanitize_text_field($speaker_category['name'] ?? '');\n            if ($speaker_category_name !== '' && !in_array($speaker_category_name, array_column($speaker_categories, 'name'), true)) {\n                $speaker_categories[] = ['name' => $speaker_category_name];\n            }\n        }\n        update_post_meta($new_id, '_pa_speaker_categories', $speaker_categories);\n"
if "update_post_meta($new_id, '_pa_speaker_categories'" not in php:
    php = php.replace(old, new, 1)

helpers = r'''    private function speaker_category_row($i, $category) {
        $name = is_array($category) ? ($category['name'] ?? '') : (string)$category;
        echo '<div class="pa-speaker-category-row"><input type="text" name="speaker_categories[' . esc_attr($i) . '][name]" placeholder="Speaker category" value="' . esc_attr($name) . '"><a href="#" class="pa-remove-row pa-remove-speaker-category-link">Remove category</a></div>';
    }

    private function normalize_speaker_categories($categories) {
        $normalized = [];
        foreach ((array)$categories as $category) {
            $name = is_array($category) ? ($category['name'] ?? '') : $category;
            $name = sanitize_text_field($name);
            if ($name !== '' && !in_array($name, $normalized, true)) { $normalized[] = $name; }
        }
        return $normalized;
    }

    private function speaker_categories_for_program($program_id = 0) {
        $program_id = absint($program_id);
        if ($program_id) { return $this->normalize_speaker_categories(get_post_meta($program_id, '_pa_speaker_categories', true)); }
        $categories = [];
        $programs = get_posts(['post_type'=>'pa_program','post_status'=>['publish','draft'],'numberposts'=>-1,'orderby'=>'title','order'=>'ASC']);
        foreach ($programs as $program) {
            foreach ($this->normalize_speaker_categories(get_post_meta($program->ID, '_pa_speaker_categories', true)) as $category) {
                if (!in_array($category, $categories, true)) { $categories[] = $category; }
            }
        }
        return $categories;
    }

    private function speaker_category_options_html($categories, $selected = '') {
        $selected = sanitize_text_field($selected);
        ob_start();
        echo '<option value="">Default speaker</option>';
        foreach ($this->normalize_speaker_categories($categories) as $category) {
            echo '<option value="' . esc_attr($category) . '" ' . selected($selected, $category, false) . '>' . esc_html($category) . '</option>';
        }
        return ob_get_clean();
    }

    private function selected_speaker_admin_row($speaker_id, $event_speaker_categories = [], $speaker_categories = []) {
        $speaker_id = absint($speaker_id);
        $sp = get_post($speaker_id);
        if (!$sp || $sp->post_type !== 'pa_speaker') { return ''; }
        $selected_category = '';
        foreach ([$speaker_id, (string)$speaker_id] as $key) {
            if (isset($event_speaker_categories[$key])) { $selected_category = sanitize_text_field($event_speaker_categories[$key]); break; }
        }
        return '<li data-id="' . esc_attr($speaker_id) . '"><span class="pa-selected-speaker-name">' . esc_html($sp->post_title) . '</span><span class="pa-selected-speaker-category-wrap"><label><span class="screen-reader-text">Speaker category</span><select class="pa-selected-speaker-category" name="speaker_categories[' . esc_attr($speaker_id) . ']">' . $this->speaker_category_options_html($speaker_categories, $selected_category) . '</select></label></span><span class="pa-selected-speaker-actions"><button type="button" class="button-link pa-move-speaker-up" aria-label="Move up" title="Move up"><span aria-hidden="true">▲</span><span class="screen-reader-text">Move up</span></button> <button type="button" class="button-link pa-move-speaker-down" aria-label="Move down" title="Move down"><span aria-hidden="true">▼</span><span class="screen-reader-text">Move down</span></button> <button type="button" class="button-link pa-remove-speaker">Remove</button></span></li>';
    }

'''
if 'private function speaker_category_row(' not in php:
    php = php.replace('    private function sponsor_level_row($i, $level) {\n', helpers + '    private function sponsor_level_row($i, $level) {\n', 1)

old = "        $speaker_ids = $id ? get_post_meta($id, '_pa_speaker_ids', true) : [];\n        if (!is_array($speaker_ids)) { $speaker_ids = []; }\n        $programs = get_posts(['post_type'=>'pa_program','post_status'=>['publish','draft'],'numberposts'=>-1,'orderby'=>'title','order'=>'ASC']);\n"
new = "        $speaker_ids = $id ? get_post_meta($id, '_pa_speaker_ids', true) : [];\n        if (!is_array($speaker_ids)) { $speaker_ids = []; }\n        $event_speaker_categories = $id ? get_post_meta($id, '_pa_event_speaker_categories', true) : [];\n        if (!is_array($event_speaker_categories)) { $event_speaker_categories = []; }\n        $speaker_categories = $this->speaker_categories_for_program($program_id);\n        $programs = get_posts(['post_type'=>'pa_program','post_status'=>['publish','draft'],'numberposts'=>-1,'orderby'=>'title','order'=>'ASC']);\n"
if "_pa_event_speaker_categories" not in php.split('public function form_event()', 1)[1].split('public function form_speaker()', 1)[0]:
    php = php.replace(old, new, 1)

old = """        echo '</div><ul class=\"pa-selected-speakers\" data-empty=\"No speakers selected.\">';
        foreach ($speaker_ids as $sid) { $sp = get_post($sid); if ($sp) { echo '<li data-id="' . esc_attr($sid) . '"><span class="pa-selected-speaker-name">' . esc_html($sp->post_title) . '</span><span class="pa-selected-speaker-actions"><button type="button" class="button-link pa-move-speaker-up" aria-label="Move up" title="Move up"><span aria-hidden="true">▲</span><span class="screen-reader-text">Move up</span></button> <button type="button" class="button-link pa-move-speaker-down" aria-label="Move down" title="Move down"><span aria-hidden="true">▼</span><span class="screen-reader-text">Move down</span></button> <button type="button" class="button-link pa-remove-speaker">Remove</button></span></li>'; } }
        echo '</ul><input type=\"hidden\" name=\"speaker_order\" class=\"pa-speaker-order\" value=\"' . esc_attr(implode(',', array_map('intval', $speaker_ids))) . '\"></section>';
"""
new = """        echo '</div><ul class=\"pa-selected-speakers pa-selected-speakers-with-categories\" data-empty=\"No speakers selected.\">';
        foreach ($speaker_ids as $sid) { echo $this->selected_speaker_admin_row($sid, $event_speaker_categories, $speaker_categories); }
        echo '</ul><template id=\"pa-speaker-category-select-template\"><span class=\"pa-selected-speaker-category-wrap\"><label><span class=\"screen-reader-text\">Speaker category</span><select class=\"pa-selected-speaker-category\" name=\"speaker_categories[__SPEAKER_ID__]\">' . $this->speaker_category_options_html($speaker_categories) . '</select></label></span></template><input type=\"hidden\" name=\"speaker_order\" class=\"pa-speaker-order\" value=\"' . esc_attr(implode(',', array_map('intval', $speaker_ids))) . '\"></section>';
"""
if 'pa-selected-speakers-with-categories' not in php:
    php = php.replace(old, new, 1)

old = "        $order = array_filter(array_map('absint', explode(',', sanitize_text_field($_POST['speaker_order'] ?? ''))));\n        update_post_meta($new_id, '_pa_speaker_ids', $order);\n"
new = old + "        $raw_speaker_categories = (array)($_POST['speaker_categories'] ?? []);\n        $event_speaker_categories = [];\n        foreach ($order as $speaker_id) {\n            $speaker_id = absint($speaker_id);\n            $speaker_category = '';\n            foreach ([$speaker_id, (string)$speaker_id] as $speaker_category_key) {\n                if (isset($raw_speaker_categories[$speaker_category_key])) { $speaker_category = sanitize_text_field($raw_speaker_categories[$speaker_category_key]); break; }\n            }\n            if ($speaker_category !== '') { $event_speaker_categories[(string)$speaker_id] = $speaker_category; }\n        }\n        update_post_meta($new_id, '_pa_event_speaker_categories', $event_speaker_categories);\n"
if "update_post_meta($new_id, '_pa_event_speaker_categories'" not in php:
    php = php.replace(old, new, 1)

php = php.replace("$this->speaker_cards($speaker_ids, $program_id, 'agenda')", "$this->speaker_cards($speaker_ids, $program_id, 'agenda', $event->ID)", 1)
php = php.replace("$this->speaker_cards($speaker_ids, $program_id, 'agenda')", "$this->speaker_cards($speaker_ids, $program_id, 'agenda', $post->ID)", 1)

start = php.find('    private function speaker_cards(')
end = php.find('\n}\n\nnew Program_Agenda_Plugin();', start)
if start != -1 and end != -1:
    old_func = php[start:end]
    if 'pa-speaker-card-category-label' not in old_func:
        new_func = r'''    private function speaker_cards($speaker_ids, $program_id = 0, $context = '', $event_id = 0) {
        $settings = $program_id ? get_post_meta($program_id, '_pa_speaker_card_settings', true) : [];
        if (!is_array($settings)) { $settings = []; }
        $show_thumb = ($settings['show_thumbnail'] ?? '1') !== '0';
        $style = '';
        $card_color = !empty($settings['color']) ? sanitize_hex_color($settings['color']) : '';
        $card_bg = !empty($settings['background']) ? sanitize_hex_color($settings['background']) : '';
        if ($card_bg) { $style .= 'background-color:' . esc_attr($card_bg) . ';'; }
        if ($card_color) { $style .= 'color:' . esc_attr($card_color) . ';--pa-speaker-card-text-color:' . esc_attr($card_color) . ';'; }
        $text_style = $card_color ? 'color:' . esc_attr($card_color) . ' !important;' : '';
        $style .= $this->program_border_style($settings);
        if (!empty($settings['border_color'])) { $style .= 'border-color:' . esc_attr($settings['border_color']) . ';'; }
        $img_class = 'pa-speaker-card-thumb';
        if (($settings['thumbnail_shape'] ?? '') === 'circle') { $img_class .= ' is-circle'; }
        if (($settings['thumbnail_shape'] ?? '') === 'square') { $img_class .= ' is-square'; }
        $event_speaker_categories = $event_id ? get_post_meta(absint($event_id), '_pa_event_speaker_categories', true) : [];
        if (!is_array($event_speaker_categories)) { $event_speaker_categories = []; }
        $default_cards = [];
        $categorized_cards = [];
        foreach ((array)$speaker_ids as $sid) {
            $sid = absint($sid);
            $sp = get_post($sid);
            if (!$sp || $sp->post_type !== 'pa_speaker') { continue; }
            $category = '';
            foreach ([$sid, (string)$sid] as $key) { if (isset($event_speaker_categories[$key])) { $category = sanitize_text_field($event_speaker_categories[$key]); break; } }
            $role = get_post_meta($sp->ID, '_pa_speaker_role_title', true);
            if (!$role) { $role = get_post_meta($sp->ID, '_pa_speaker_credentials', true); }
            $company = get_post_meta($sp->ID, '_pa_speaker_company', true);
            $img = absint(get_post_meta($sp->ID, '_pa_speaker_image_id', true));
            ob_start();
            echo '<div class="pa-speaker-card-unit' . ($category ? ' pa-speaker-card-unit--categorized' : '') . '">';
            if ($category) { echo '<span class="pa-speaker-card-category-label">' . esc_html($category) . '</span>'; }
            echo '<article class="pa-speaker-card' . ($category ? ' pa-speaker-card--categorized' : '') . '" style="' . esc_attr($style) . '">';
            if ($show_thumb) {
                echo '<a class="pa-speaker-card-image" href="' . esc_url(get_permalink($sp)) . '">';
                if ($img) { echo wp_get_attachment_image($img, 'medium', false, ['class'=>$img_class]); }
                else { echo '<span class="' . esc_attr($img_class) . ' pa-speaker-card-placeholder" aria-hidden="true"></span>'; }
                echo '</a>';
            }
            echo '<div class="pa-speaker-card-text"><h3><a style="' . esc_attr($text_style) . '" href="' . esc_url(get_permalink($sp)) . '">' . esc_html($sp->post_title) . '</a></h3>';
            if ($role) { echo '<p class="pa-speaker-card-role" style="' . esc_attr($text_style) . '">' . esc_html($role) . '</p>'; }
            if ($company) { echo '<p class="pa-speaker-card-company" style="' . esc_attr($text_style) . '">' . esc_html($company) . '</p>'; }
            echo '</div></article></div>';
            $card_html = ob_get_clean();
            if ($category) { $categorized_cards[] = $card_html; } else { $default_cards[] = $card_html; }
        }
        $list_classes = 'pa-speaker-card-list ' . ($context === 'agenda' ? 'pa-speaker-card-list-agenda' : '');
        if ($categorized_cards) { $list_classes .= ' pa-speaker-card-list-has-categories'; }
        if ($categorized_cards && $default_cards) { $list_classes .= ' pa-speaker-card-list--categorized-split'; }
        ob_start();
        echo '<div class="' . esc_attr(trim($list_classes)) . '">';
        if ($categorized_cards && $default_cards) {
            echo '<div class="pa-speaker-card-column pa-speaker-card-column--default">' . implode('', $default_cards) . '</div>';
            echo '<div class="pa-speaker-card-column pa-speaker-card-column--categorized">' . implode('', $categorized_cards) . '</div>';
        } else {
            echo implode('', array_merge($default_cards, $categorized_cards));
        }
        echo '</div>';
        return ob_get_clean();
    }'''
        php = php[:start] + new_func + php[end:]
PHP.write_text(php)

js = JS.read_text()
if 'function speakerCategorySelectHtml' not in js:
    marker = "  function updateSpeakerOrder(){var ids=[];$('.pa-selected-speakers li').each(function(){ids.push($(this).data('id'));});$('.pa-speaker-order').val(ids.join(','));}\n"
    js = js.replace(marker, marker + "  function speakerCategorySelectHtml(id){var html=$('#pa-speaker-category-select-template').html()||''; return html.replace(/__SPEAKER_ID__/g,id);}\n", 1)
old = """  $(document).on('change','.pa-speaker-check',function(){
    var id=$(this).val(), name=$(this).closest('label').text().trim(), $list=$('.pa-selected-speakers');
    if(this.checked){ if(!$list.find('li[data-id="'+id+'"]').length){$list.append('<li data-id="'+id+'"><span class="pa-selected-speaker-name">'+name+'</span><span class="pa-selected-speaker-actions"><button type="button" class="button-link pa-move-speaker-up" aria-label="Move up" title="Move up"><span aria-hidden="true">▲</span><span class="screen-reader-text">Move up</span></button> <button type="button" class="button-link pa-move-speaker-down" aria-label="Move down" title="Move down"><span aria-hidden="true">▼</span><span class="screen-reader-text">Move down</span></button> <button type="button" class="button-link pa-remove-speaker">Remove</button></span></li>');} }
    else {$list.find('li[data-id="'+id+'"]').remove();}
    updateSpeakerOrder();
  });
"""
new = """  $(document).on('change','.pa-speaker-check',function(){
    var id=$(this).val(), name=$(this).closest('label').text().trim(), $list=$('.pa-selected-speakers');
    if(this.checked){ if(!$list.find('li[data-id="'+id+'"]').length){$list.append('<li data-id="'+id+'"><span class="pa-selected-speaker-name">'+name+'</span>'+speakerCategorySelectHtml(id)+'<span class="pa-selected-speaker-actions"><button type="button" class="button-link pa-move-speaker-up" aria-label="Move up" title="Move up"><span aria-hidden="true">▲</span><span class="screen-reader-text">Move up</span></button> <button type="button" class="button-link pa-move-speaker-down" aria-label="Move down" title="Move down"><span aria-hidden="true">▼</span><span class="screen-reader-text">Move down</span></button> <button type="button" class="button-link pa-remove-speaker">Remove</button></span></li>');} }
    else {$list.find('li[data-id="'+id+'"]').remove();}
    updateSpeakerOrder();
  });
"""
if 'speakerCategorySelectHtml(id)' not in js:
    js = js.replace(old, new, 1)
if '.pa-add-speaker-category' not in js:
    marker = "  $(document).on('click','.pa-add-category',function(){\n    var $wrap=$('#pa-categories'), tpl=$('#pa-category-template').html(), i=$wrap.children('.pa-category-row').length;\n    var $row=$(tpl.replaceAll('__INDEX__',i));\n    $wrap.append($row);\n    refreshCategoryIcon($row);\n  });\n"
    js = js.replace(marker, marker + "  $(document).on('click','.pa-add-speaker-category',function(e){e.preventDefault();var $wrap=$('#pa-speaker-categories'), tpl=$('#pa-speaker-category-template').html(), i=$wrap.children('.pa-speaker-category-row').length;$wrap.append($(tpl.replaceAll('__INDEX__',i)));});\n  $(document).on('click','.pa-remove-speaker-category-link',function(e){e.preventDefault();$(this).closest('.pa-speaker-category-row').remove();});\n", 1)
JS.write_text(js)

admin_css = ADMIN_CSS.read_text()
if '/* Stagecard speaker categories */' not in admin_css:
    admin_css += '\n\n/* Stagecard speaker categories */\n.pa-program-category-columns{display:grid;grid-template-columns:minmax(0,1.4fr) minmax(280px,.8fr);gap:28px;align-items:start;margin:20px 0 26px;}\n.pa-program-category-column{border:1px solid #dcdcde;border-radius:10px;background:#fff;padding:18px;}\n.pa-program-category-column h3{margin-top:0!important;}\n.pa-speaker-category-row{display:flex;gap:12px;align-items:center;margin:0 0 12px;}\n.pa-speaker-category-row input{flex:1;}\n.pa-selected-speakers-with-categories li{display:grid!important;grid-template-columns:minmax(140px,1fr) minmax(160px,220px) auto!important;gap:12px!important;align-items:center!important;}\n.pa-selected-speaker-category-wrap select{width:100%;}\n@media (max-width:900px){.pa-program-category-columns{grid-template-columns:1fr;}.pa-selected-speakers-with-categories li{grid-template-columns:1fr!important;align-items:start!important;}.pa-selected-speaker-actions{justify-self:start;}}\n'
ADMIN_CSS.write_text(admin_css)

public_css = PUBLIC_CSS.read_text()
if '/* Stagecard categorized speaker cards */' not in public_css:
    public_css += '\n\n/* Stagecard categorized speaker cards */\n.pa-speaker-card-list-has-categories{align-items:flex-start!important;}\n.pa-speaker-card-list--categorized-split{display:grid!important;grid-template-columns:minmax(0,1fr) minmax(0,1fr)!important;gap:14px!important;width:100%!important;}\n.pa-speaker-card-column{display:grid!important;grid-template-columns:repeat(2,minmax(0,max-content))!important;gap:12px!important;align-items:start!important;min-width:0!important;}\n.pa-speaker-card-unit{display:flex!important;flex-direction:column!important;gap:4px!important;align-items:flex-start!important;min-width:0!important;}\n.pa-speaker-card-category-label{display:block!important;margin:0 0 1px!important;font-size:.68rem!important;line-height:1.1!important;font-weight:600!important;letter-spacing:.03em!important;text-transform:uppercase!important;color:var(--pa-agenda-location-color,var(--pa-agenda-title-color,inherit))!important;text-align:left!important;}\n.pa-speaker-card--categorized{border:1px solid var(--pa-agenda-bar-color,var(--pa-agenda-accent-color,currentColor))!important;}\n.pa-speaker-card-list-has-categories:not(.pa-speaker-card-list--categorized-split){gap:14px!important;}\n@media (max-width:900px){.pa-speaker-card-list--categorized-split{grid-template-columns:1fr!important;}.pa-speaker-card-column{grid-template-columns:1fr!important;}}\n'
PUBLIC_CSS.write_text(public_css)

print('Applied speaker event picker and speaker category support.')
