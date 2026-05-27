from pathlib import Path

PHP = Path('program-agenda/program-agenda.php')
PUBLIC_CSS = Path('program-agenda/assets/css/public.css')

php = PHP.read_text()

constructor_marker = "        add_shortcode('program_sponsors', [$this, 'shortcode_program_sponsors']);\n"
constructor_insert = constructor_marker + "        add_shortcode('program_pdf', [$this, 'shortcode_program_pdf']);\n        add_action('template_redirect', [$this, 'maybe_render_program_pdf_page']);\n"
if "shortcode_program_pdf" not in php.split("public function shortcode_program_agenda", 1)[0]:
    if constructor_marker not in php:
        raise SystemExit('Could not find constructor shortcode marker.')
    php = php.replace(constructor_marker, constructor_insert, 1)

page_has_old = "        return has_shortcode($post->post_content, 'program_agenda') || has_shortcode($post->post_content, 'program_sponsors');\n"
page_has_new = "        return has_shortcode($post->post_content, 'program_agenda') || has_shortcode($post->post_content, 'program_sponsors') || has_shortcode($post->post_content, 'program_pdf');\n"
if page_has_old in php:
    php = php.replace(page_has_old, page_has_new, 1)

form_old = "            echo '<div class=\"pa-shortcode-box\"><h3>Sponsor Showcase Shortcode</h3><p>Place this shortcode on the public Sponsors showcase page.</p><input readonly value=\"' . esc_attr('[program_sponsors id=\"' . $this->program_shortcode_id($id) . '\"]') . '\" onclick=\"this.select();\"></div>';\n"
form_new = form_old + "            echo '<div class=\"pa-shortcode-box\"><h3>Program PDF Shortcode</h3><p>Place this shortcode wherever users should download or print the latest Program agenda.</p><input readonly value=\"' . esc_attr('[program_pdf id=\"' . $this->program_shortcode_id($id) . '\"]') . '\" onclick=\"this.select();\"></div>';\n"
if 'Program PDF Shortcode' not in php:
    if form_old not in php:
        raise SystemExit('Could not find sponsor shortcode box marker.')
    php = php.replace(form_old, form_new, 1)

else_old = "            echo '<div class=\"pa-shortcode-box\"><h3>Shortcodes</h3><p>The agenda and sponsor showcase shortcodes will appear here after the program is saved.</p></div>';\n"
else_new = "            echo '<div class=\"pa-shortcode-box\"><h3>Shortcodes</h3><p>The agenda, sponsor showcase, and Program PDF shortcodes will appear here after the program is saved.</p></div>';\n"
if else_old in php:
    php = php.replace(else_old, else_new, 1)

method_marker = "    public function shortcode_program_sponsors($atts) {\n"
method_block = r'''
    public function shortcode_program_pdf($atts) {
        $atts = shortcode_atts(['id'=>'', 'label'=>'Download Program PDF'], $atts, 'program_pdf');
        $program_id = $this->resolve_program_shortcode_id($atts['id']);
        $program = get_post($program_id);
        if (!$program || $program->post_type !== 'pa_program') { return ''; }
        $url = add_query_arg('pa_program_pdf', $program_id, home_url('/'));
        $label = trim(wp_strip_all_tags((string)($atts['label'] ?? '')));
        if ($label === '') { $label = 'Download Program PDF'; }
        return '<p class="pa-program-pdf-download"><a class="pa-program-pdf-link" href="' . esc_url($url) . '" target="_blank" rel="noopener">' . esc_html($label) . '</a></p>';
    }

    public function maybe_render_program_pdf_page() {
        if (empty($_GET['pa_program_pdf'])) { return; }
        $program_id = absint($_GET['pa_program_pdf']);
        $program = get_post($program_id);
        if (!$program || $program->post_type !== 'pa_program') {
            status_header(404);
            wp_die(esc_html__('Program not found.', 'program-agenda'));
        }

        $events = get_posts([
            'post_type' => 'pa_event',
            'post_status' => 'publish',
            'numberposts' => -1,
            'meta_query' => [['key'=>'_pa_program_id','value'=>$program_id,'compare'=>'=']],
        ]);
        usort($events, function($a, $b) {
            $cmp = $this->agenda_event_sort_value($a) <=> $this->agenda_event_sort_value($b);
            if ($cmp !== 0) { return $cmp; }
            return strcasecmp($a->post_title, $b->post_title);
        });

        $program_url = get_post_meta($program_id, '_pa_back_to_link', true);
        if (!$program_url) { $program_url = home_url('/'); }
        $generated = date_i18n(get_option('date_format', 'F j, Y'));
        $logo_url = '';
        $logo_id = function_exists('get_theme_mod') ? absint(get_theme_mod('custom_logo')) : 0;
        if ($logo_id) { $logo_url = wp_get_attachment_image_url($logo_id, 'full'); }
        $site_name = get_bloginfo('name');

        nocache_headers();
        header('Content-Type: text/html; charset=' . get_bloginfo('charset'));
        echo '<!doctype html><html ' . get_language_attributes() . '><head><meta charset="' . esc_attr(get_bloginfo('charset')) . '"><meta name="viewport" content="width=device-width, initial-scale=1"><title>' . esc_html($program->post_title) . ' Program PDF</title>';
        echo '<style>
            :root{color-scheme:light;}
            body{margin:0;background:#f6f7f7;color:#1d2327;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;line-height:1.45;}
            .pa-program-print-page{max-width:900px;margin:0 auto;padding:48px 36px;background:#fff;min-height:100vh;box-sizing:border-box;}
            .pa-program-print-actions{position:sticky;top:0;z-index:2;margin:-48px -36px 32px;padding:14px 36px;background:#f6f7f7;border-bottom:1px solid #dcdcde;text-align:right;}
            .pa-program-print-actions button{appearance:none;border:1px solid #1d2327;background:#1d2327;color:#fff;border-radius:4px;padding:8px 14px;cursor:pointer;}
            .pa-program-print-logo{max-width:220px;max-height:90px;width:auto;height:auto;object-fit:contain;margin:0 0 28px;display:block;}
            .pa-program-print-site-name{margin:0 0 22px;font-size:14px;font-weight:700;text-transform:uppercase;letter-spacing:.08em;color:#646970;}
            .pa-program-print-title{margin:0 0 10px;font-size:34px;line-height:1.08;}
            .pa-program-print-note{margin:0 0 34px;color:#50575e;font-size:14px;border-bottom:1px solid #dcdcde;padding-bottom:22px;}
            .pa-program-print-note a{color:inherit;}
            .pa-program-print-day{margin:34px 0 14px;font-size:20px;line-height:1.2;border-bottom:2px solid #1d2327;padding-bottom:8px;}
            .pa-program-print-event{break-inside:avoid;page-break-inside:avoid;margin:0 0 22px;padding:0 0 22px;border-bottom:1px solid #dcdcde;}
            .pa-program-print-event:last-child{border-bottom:0;}
            .pa-program-print-time{margin:0 0 4px;font-size:13px;font-weight:700;text-transform:uppercase;letter-spacing:.04em;color:#646970;}
            .pa-program-print-event-title{margin:0 0 8px;font-size:18px;line-height:1.2;}
            .pa-program-print-meta{margin:0 0 10px;font-size:13px;color:#50575e;}
            .pa-program-print-description{margin:10px 0 0;font-size:14px;}
            .pa-program-print-description > :first-child{margin-top:0;}
            .pa-program-print-description > :last-child{margin-bottom:0;}
            .pa-program-print-speakers{margin:12px 0 0;}
            .pa-program-print-speakers h3{margin:0 0 6px;font-size:13px;text-transform:uppercase;letter-spacing:.04em;}
            .pa-program-print-speakers ul{margin:0;padding-left:18px;}
            .pa-program-print-speakers li{margin:0 0 5px;}
            .pa-program-print-speaker-detail{color:#50575e;font-size:13px;}
            .pa-program-print-empty{margin:24px 0;color:#646970;}
            @media print{body{background:#fff}.pa-program-print-page{max-width:none;padding:0;background:#fff}.pa-program-print-actions{display:none}.pa-program-print-note{font-size:11px}.pa-program-print-title{font-size:28px}.pa-program-print-day{break-after:avoid;page-break-after:avoid}.pa-program-print-event{break-inside:avoid;page-break-inside:avoid}}
        </style>';
        echo '</head><body><main class="pa-program-print-page">';
        echo '<div class="pa-program-print-actions"><button type="button" onclick="window.print()">Print / Save as PDF</button></div>';
        if ($logo_url) { echo '<img class="pa-program-print-logo" src="' . esc_url($logo_url) . '" alt="' . esc_attr($site_name) . '">'; }
        else { echo '<p class="pa-program-print-site-name">' . esc_html($site_name) . '</p>'; }
        echo '<h1 class="pa-program-print-title">' . esc_html($program->post_title) . '</h1>';
        echo '<p class="pa-program-print-note">Generated on ' . esc_html($generated) . ' and subject to change. Visit <a href="' . esc_url($program_url) . '">' . esc_html($program_url) . '</a> for the latest agenda.</p>';

        if (!$events) {
            echo '<p class="pa-program-print-empty">No events have been added yet.</p>';
        } else {
            $current_day = '';
            foreach ($events as $event) {
                $date = get_post_meta($event->ID, '_pa_event_date', true);
                $day_key = $date ? date_i18n('Y-m-d', strtotime($date)) : 'unscheduled';
                if ($day_key !== $current_day) {
                    $current_day = $day_key;
                    $day_label = $date && strtotime($date) ? date_i18n('F j, Y', strtotime($date)) : 'Unscheduled';
                    echo '<h2 class="pa-program-print-day">' . esc_html($day_label) . '</h2>';
                }
                $start = get_post_meta($event->ID, '_pa_event_time', true);
                $end = get_post_meta($event->ID, '_pa_event_end_time', true);
                $time = trim($start . ($end ? ' – ' . $end : ''));
                $location = get_post_meta($event->ID, '_pa_event_location', true);
                $category = get_post_meta($event->ID, '_pa_event_category', true);
                echo '<article class="pa-program-print-event">';
                if ($time) { echo '<p class="pa-program-print-time">' . esc_html($time) . '</p>'; }
                echo '<h3 class="pa-program-print-event-title">' . esc_html($event->post_title) . '</h3>';
                $meta = array_filter([$category, $location]);
                if ($meta) { echo '<p class="pa-program-print-meta">' . esc_html(implode(' • ', $meta)) . '</p>'; }
                if ($event->post_content) { echo '<div class="pa-program-print-description">' . wp_kses_post(wpautop($event->post_content)) . '</div>'; }
                $speaker_ids = get_post_meta($event->ID, '_pa_speaker_ids', true);
                if (!is_array($speaker_ids)) { $speaker_ids = []; }
                if ($speaker_ids) {
                    echo '<section class="pa-program-print-speakers"><h3>Speakers</h3><ul>';
                    foreach ($speaker_ids as $speaker_id) {
                        $speaker = get_post(absint($speaker_id));
                        if (!$speaker || $speaker->post_type !== 'pa_speaker') { continue; }
                        $credentials = get_post_meta($speaker->ID, '_pa_speaker_credentials', true);
                        $role = get_post_meta($speaker->ID, '_pa_speaker_role_title', true);
                        $company = get_post_meta($speaker->ID, '_pa_speaker_company', true);
                        $name = $speaker->post_title . ($credentials ? ', ' . $credentials : '');
                        $detail = implode(' • ', array_filter([$role, $company]));
                        echo '<li><strong>' . esc_html($name) . '</strong>' . ($detail ? '<br><span class="pa-program-print-speaker-detail">' . esc_html($detail) . '</span>' : '') . '</li>';
                    }
                    echo '</ul></section>';
                }
                echo '</article>';
            }
        }
        echo '</main><script>window.addEventListener("load",function(){setTimeout(function(){window.print();},250);});</script></body></html>';
        exit;
    }

'''
if 'public function shortcode_program_pdf' not in php:
    if method_marker not in php:
        raise SystemExit('Could not find shortcode_program_sponsors marker.')
    php = php.replace(method_marker, method_block + method_marker, 1)

PHP.write_text(php)

css = PUBLIC_CSS.read_text()
css_marker = '/* Stagecard program PDF shortcode */'
css_block = r'''
/* Stagecard program PDF shortcode */
.pa-program-pdf-download{
  margin:1rem 0;
}
.pa-program-pdf-link{
  display:inline-flex!important;
  align-items:center!important;
  justify-content:center!important;
  gap:.4rem!important;
  padding:.65rem 1rem!important;
  border:1px solid currentColor!important;
  border-radius:.35rem!important;
  color:inherit!important;
  text-decoration:none!important;
  line-height:1.2!important;
}
.pa-program-pdf-link:hover,
.pa-program-pdf-link:focus{
  text-decoration:underline!important;
  text-underline-offset:.18em!important;
}
'''
if css_marker not in css:
    css = css.rstrip() + '\n\n' + css_block.strip() + '\n'
PUBLIC_CSS.write_text(css)

print('Applied Program PDF shortcode support.')
