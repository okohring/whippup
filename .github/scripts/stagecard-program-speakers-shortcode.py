from pathlib import Path
import re

PHP = Path('program-agenda/program-agenda.php')
PUBLIC_CSS = Path('program-agenda/assets/css/public.css')

php = PHP.read_text()

if "add_shortcode('program_speakers'" not in php:
    php = php.replace(
        "        add_shortcode('program_sponsors', [$this, 'shortcode_program_sponsors']);\n",
        "        add_shortcode('program_sponsors', [$this, 'shortcode_program_sponsors']);\n        add_shortcode('program_speakers', [$this, 'shortcode_program_speakers']);\n",
        1,
    )

php = php.replace(
    "return has_shortcode($post->post_content, 'program_agenda') || has_shortcode($post->post_content, 'program_sponsors') || has_shortcode($post->post_content, 'program_pdf');",
    "return has_shortcode($post->post_content, 'program_agenda') || has_shortcode($post->post_content, 'program_sponsors') || has_shortcode($post->post_content, 'program_speakers') || has_shortcode($post->post_content, 'program_pdf');",
)

if 'Speaker Directory Shortcode' not in php:
    php = php.replace(
        "            echo '<div class=\"pa-shortcode-box\"><h3>Sponsor Showcase Shortcode</h3><p>Place this shortcode on the public Sponsors showcase page.</p><input readonly value=\"' . esc_attr('[program_sponsors id=\"' . $this->program_shortcode_id($id) . '\"]') . '\" onclick=\"this.select();\"></div>';\n",
        "            echo '<div class=\"pa-shortcode-box\"><h3>Sponsor Showcase Shortcode</h3><p>Place this shortcode on the public Sponsors showcase page.</p><input readonly value=\"' . esc_attr('[program_sponsors id=\"' . $this->program_shortcode_id($id) . '\"]') . '\" onclick=\"this.select();\"></div>';\n            echo '<div class=\"pa-shortcode-box\"><h3>Speaker Directory Shortcode</h3><p>Place this shortcode on a public Speakers page to show everyone speaking at this Program.</p><input readonly value=\"' . esc_attr('[program_speakers id=\"' . $this->program_shortcode_id($id) . '\"]') . '\" onclick=\"this.select();\"></div>';\n",
        1,
    )
    php = php.replace(
        "<p>The agenda, sponsor showcase, and Program PDF shortcodes will appear here after the program is saved.</p>",
        "<p>The agenda, sponsor showcase, speaker directory, and Program PDF shortcodes will appear here after the program is saved.</p>",
    )

method = r'''    public function shortcode_program_speakers($atts) {
        $atts = shortcode_atts(['id'=>''], $atts, 'program_speakers');
        $program_id = $this->resolve_program_shortcode_id($atts['id']);
        $program = get_post($program_id);
        if (!$program || $program->post_type !== 'pa_program') { return ''; }

        $events = get_posts([
            'post_type'=>'pa_event',
            'post_status'=>'publish',
            'numberposts'=>-1,
            'meta_key'=>'_pa_event_date',
            'orderby'=>'meta_value',
            'order'=>'ASC',
            'meta_query'=>[['key'=>'_pa_program_id','value'=>$program_id,'compare'=>'=']],
        ]);

        $speaker_ids = [];
        foreach ($events as $event) {
            $ids = get_post_meta($event->ID, '_pa_speaker_ids', true);
            if (!is_array($ids)) { continue; }
            foreach ($ids as $speaker_id) {
                $speaker_id = absint($speaker_id);
                if ($speaker_id && get_post_type($speaker_id) === 'pa_speaker' && !in_array($speaker_id, $speaker_ids, true)) {
                    $speaker_ids[] = $speaker_id;
                }
            }
        }

        if (!$speaker_ids) { return '<p class="pa-program-speakers-empty">No speakers have been added yet.</p>'; }

        $speakers = get_posts([
            'post_type'=>'pa_speaker',
            'post_status'=>'publish',
            'numberposts'=>-1,
            'post__in'=>$speaker_ids,
            'orderby'=>'title',
            'order'=>'ASC',
        ]);

        ob_start();
        echo '<section class="pa-program-speakers" aria-label="Program speakers">';
        echo '<div class="pa-program-speaker-grid">';
        foreach ($speakers as $speaker) {
            $image_id = absint(get_post_meta($speaker->ID, '_pa_speaker_image_id', true));
            $role = get_post_meta($speaker->ID, '_pa_speaker_role_title', true);
            $company = get_post_meta($speaker->ID, '_pa_speaker_company', true);
            $permalink = get_permalink($speaker);
            echo '<article class="pa-program-speaker-card">';
            echo '<a class="pa-program-speaker-image-link" href="' . esc_url($permalink) . '" aria-label="' . esc_attr($speaker->post_title) . '">';
            if ($image_id) {
                echo wp_get_attachment_image($image_id, 'medium', false, ['class'=>'pa-program-speaker-image', 'alt'=>esc_attr($speaker->post_title)]);
            } else {
                echo '<span class="pa-program-speaker-image pa-program-speaker-placeholder" aria-hidden="true"></span>';
            }
            echo '</a>';
            echo '<h3 class="pa-program-speaker-name"><a href="' . esc_url($permalink) . '">' . esc_html($speaker->post_title) . '</a></h3>';
            if ($role) { echo '<p class="pa-program-speaker-role">' . esc_html($role) . '</p>'; }
            if ($company) { echo '<p class="pa-program-speaker-company">' . esc_html($company) . '</p>'; }
            echo '</article>';
        }
        echo '</div></section>';
        return ob_get_clean();
    }

'''
if 'public function shortcode_program_speakers(' not in php:
    php = php.replace('    public function shortcode_program_pdf($atts) {\n', method + '    public function shortcode_program_pdf($atts) {\n', 1)

PHP.write_text(php)

css = PUBLIC_CSS.read_text()
css = re.sub(r'\n?/\* Stagecard program speakers shortcode \*/.*?(?=\n/\* Stagecard |\Z)', '\n', css, flags=re.S)
block = '''
/* Stagecard program speakers shortcode */
.pa-program-speakers{
  width:100%!important;
  box-sizing:border-box!important;
}
.pa-program-speaker-grid{
  display:grid!important;
  grid-template-columns:repeat(auto-fit,minmax(190px,1fr))!important;
  gap:36px 44px!important;
  align-items:start!important;
  justify-items:center!important;
}
.pa-program-speaker-card{
  box-sizing:border-box!important;
  width:100%!important;
  max-width:240px!important;
  text-align:center!important;
  font-family:Montserrat, Arial, Helvetica, sans-serif!important;
}
.pa-program-speaker-image-link{
  display:inline-flex!important;
  width:150px!important;
  height:150px!important;
  border-radius:50%!important;
  overflow:hidden!important;
  align-items:center!important;
  justify-content:center!important;
  margin:0 auto 16px!important;
  text-decoration:none!important;
}
.pa-program-speaker-image{
  display:block!important;
  width:150px!important;
  height:150px!important;
  max-width:150px!important;
  max-height:150px!important;
  border-radius:50%!important;
  object-fit:cover!important;
  object-position:center center!important;
}
.pa-program-speaker-placeholder{
  background:rgba(0,0,0,.08)!important;
}
.pa-program-speaker-name{
  margin:0 0 7px!important;
  font-size:.92rem!important;
  line-height:1.2!important;
  font-weight:600!important;
  text-transform:uppercase!important;
  letter-spacing:.04em!important;
}
.pa-program-speaker-name a{
  color:inherit!important;
  text-decoration:none!important;
}
.pa-program-speaker-name a:hover,
.pa-program-speaker-name a:focus-visible{
  text-decoration:underline!important;
}
.pa-program-speaker-role,
.pa-program-speaker-company{
  margin:0 0 5px!important;
  font-size:.82rem!important;
  line-height:1.35!important;
  font-weight:400!important;
}
.pa-program-speakers-empty{
  margin:0!important;
}
@media (max-width:640px){
  .pa-program-speaker-grid{
    grid-template-columns:repeat(auto-fit,minmax(150px,1fr))!important;
    gap:30px 24px!important;
  }
  .pa-program-speaker-card{
    max-width:200px!important;
  }
}
'''
css = css.rstrip() + '\n\n' + block.strip() + '\n'
PUBLIC_CSS.write_text(css)

print('Added program_speakers shortcode, Program form shortcode box, and public speaker grid styles.')
