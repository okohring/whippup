from pathlib import Path
import re

php_path = Path('program-agenda/program-agenda.php')
css_path = Path('program-agenda/assets/css/public.css')

php = php_path.read_text()

# Website link should be h6 on sponsor pages.
php = php.replace(
    '<h5 class="pa-speaker-company pa-sponsor-website"><a href="\' . esc_url($website) . \'" target="_blank" rel="noopener">Visit sponsor website</a></h5>',
    '<h6 class="pa-speaker-company pa-sponsor-website"><a href="\' . esc_url($website) . \'" target="_blank" rel="noopener">Visit sponsor website</a></h6>'
)

# Add a square/wide logo plate class based on attachment dimensions.
old_logo = """        if ($logo_id) {
            echo '<div class=\"pa-sponsor-hero-logo\"><a href=\"' . esc_url(get_permalink($post)) . '\" aria-label=\"' . esc_attr($post->post_title) . '\">' . wp_get_attachment_image($logo_id, 'full', false, ['class'=>'pa-sponsor-hero-logo-img', 'alt'=>esc_attr($post->post_title)]) . '</a></div>';
        }"""
new_logo = """        if ($logo_id) {
            $logo_meta = wp_get_attachment_metadata($logo_id);
            $logo_width = is_array($logo_meta) ? absint($logo_meta['width'] ?? 0) : 0;
            $logo_height = is_array($logo_meta) ? absint($logo_meta['height'] ?? 0) : 0;
            $logo_shape_class = ($logo_width && $logo_height && abs($logo_width - $logo_height) <= 12) ? ' pa-sponsor-hero-logo-square' : ' pa-sponsor-hero-logo-wide';
            echo '<div class=\"pa-sponsor-hero-logo' . esc_attr($logo_shape_class) . '\"><a href=\"' . esc_url(get_permalink($post)) . '\" aria-label=\"' . esc_attr($post->post_title) . '\">' . wp_get_attachment_image($logo_id, 'full', false, ['class'=>'pa-sponsor-hero-logo-img', 'alt'=>esc_attr($post->post_title)]) . '</a></div>';
        }"""
if old_logo in php:
    php = php.replace(old_logo, new_logo)

# Remove hover-animation UI/usage if any old copies remain.
php = php.replace("        $hover_animation = in_array(($s['hover_animation'] ?? 'default'), ['default','slant'], true) ? ($s['hover_animation'] ?? 'default') : 'default';\n", "")
php = php.replace('Display options, tabs, date format, and hover behavior', 'Display options, tabs, date format, and card size')
php = re.sub(r"\n\s*echo '<label class=\"pa-field\">Hover animation <select class=\"pa-agenda-live-field\" name=\"agenda\[hover_animation\]\">.*?</label>';", "", php)
php = re.sub(r"\n\s*'hover_animation' => in_array\(sanitize_key\(\$agenda_in\['hover_animation'\] \?\? 'default'\), \['default','slant'\], true\) \? sanitize_key\(\$agenda_in\['hover_animation'\] \?\? 'default'\) : 'default',", "", php)
php = php.replace("        $hover_animation = in_array(($agenda['hover_animation'] ?? 'default'), ['default','slant'], true) ? ($agenda['hover_animation'] ?? 'default') : 'default';\n", "")
php = php.replace("            'pa-event-card--hover-' . $hover_animation,\n", "")
php = php.replace(' pa-event-card--hover-default', '')
php = php.replace(' pa-event-card--hover-slant', '')

php_path.write_text(php)

css = css_path.read_text()
marker = '/* v1.15.158: final hover lock and sponsor typography/logo sizing */'
lines = [
    '',
    '/* v1.15.158: final hover lock and sponsor typography/logo sizing */',
    '.pa-event-card,.pa-agenda-item{transition:transform .16s ease,box-shadow .16s ease!important;transform-origin:center center!important;}',
    '.pa-event-card:hover,.pa-event-card:focus-within,.pa-agenda-item:hover,.pa-agenda-item:focus-within{transform:scale(1.015)!important;}',
    '.pa-event-card__datebar,.pa-agenda-category-bar{transition:none!important;transform:none!important;position:relative!important;overflow:hidden!important;}',
    '.pa-event-card__datebar::before,.pa-event-card__datebar::after,.pa-agenda-category-bar::before,.pa-agenda-category-bar::after{content:none!important;display:none!important;transform:none!important;transition:none!important;}',
    '.pa-schedule .pa-agenda-category-bar,.pa-single .pa-agenda-category-bar,.pa-schedule .pa-agenda-item:hover .pa-agenda-category-bar,.pa-schedule .pa-agenda-item:focus-within .pa-agenda-category-bar,.pa-single .pa-agenda-item:hover .pa-agenda-category-bar,.pa-single .pa-agenda-item:focus-within .pa-agenda-category-bar{width:68px!important;min-width:68px!important;max-width:68px!important;flex:0 0 68px!important;flex-basis:68px!important;}',
    '.pa-event-card:hover .pa-event-card__datebar,.pa-event-card:focus-within .pa-event-card__datebar{transform:none!important;}',
    '.pa-event-card--hover-default,.pa-event-card--hover-slant{transform:none!important;}',
    '.pa-single-sponsor .pa-sponsor-page-label{margin:0 0 .35rem!important;padding:0!important;font-size:inherit!important;line-height:1.2!important;font-weight:700!important;text-transform:none!important;letter-spacing:normal!important;}',
    '.pa-single-sponsor .pa-sponsor-name{margin:0 0 .25rem!important;padding:0!important;line-height:1.12!important;text-transform:none!important;letter-spacing:normal!important;}',
    '.pa-single-sponsor .pa-sponsor-website{margin:.12rem 0!important;padding:0!important;font-size:.875rem!important;line-height:1.25!important;font-weight:inherit!important;text-transform:none!important;letter-spacing:normal!important;}',
    '.pa-single-sponsor .pa-sponsor-website a{color:inherit!important;text-decoration:underline!important;text-underline-offset:.18em!important;}',
    '.pa-sponsor-hero-logo{background:#fff!important;border-radius:0!important;padding:30px!important;display:flex!important;align-items:center!important;justify-content:center!important;overflow:hidden!important;line-height:0!important;}',
    '.pa-sponsor-hero-logo-wide{width:250px!important;height:150px!important;flex:0 0 250px!important;}',
    '.pa-sponsor-hero-logo-square{width:150px!important;height:150px!important;flex:0 0 150px!important;}',
    '.pa-sponsor-hero-logo a{display:flex!important;align-items:center!important;justify-content:center!important;width:100%!important;height:100%!important;}',
    '.pa-sponsor-hero-logo-img{display:block!important;max-width:100%!important;max-height:100%!important;width:auto!important;height:auto!important;object-fit:contain!important;border-radius:0!important;margin:0!important;}',
    '@media(max-width:700px){.pa-event-card:hover,.pa-event-card:focus-within,.pa-agenda-item:hover,.pa-agenda-item:focus-within{transform:none!important;}.pa-schedule .pa-agenda-category-bar,.pa-single .pa-agenda-category-bar,.pa-schedule .pa-agenda-item:hover .pa-agenda-category-bar,.pa-schedule .pa-agenda-item:focus-within .pa-agenda-category-bar,.pa-single .pa-agenda-item:hover .pa-agenda-category-bar,.pa-single .pa-agenda-item:focus-within .pa-agenda-category-bar{width:100%!important;min-width:0!important;max-width:none!important;flex-basis:auto!important;}}',
    '',
]
if marker not in css:
    css_path.write_text(css.rstrip() + '\n'.join(lines))
