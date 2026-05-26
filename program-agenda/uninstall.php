<?php
/**
 * Optional uninstall cleanup for Program Agenda.
 *
 * By default, client content is preserved. Cleanup only runs when the admin
 * explicitly enables the Admin Settings cleanup option. The cleanup only targets this plugin’s Programs, Events, Speakers, and Sponsors; Media Library uploads and normal WordPress content are preserved.
 */

if (!defined('WP_UNINSTALL_PLUGIN')) {
    exit;
}

$delete_data = get_option('pa_delete_data_on_uninstall', '0') === '1';

if (!$delete_data) {
    // Keep Program, Event, Speaker, and Sponsor records by default.
    delete_option('pa_delete_data_on_uninstall');
    return;
}

$post_types = ['pa_program', 'pa_event', 'pa_speaker', 'pa_sponsor'];

foreach ($post_types as $post_type) {
    do {
        $posts = get_posts([
            'post_type' => $post_type,
            'post_status' => ['publish', 'draft', 'pending', 'private', 'future', 'trash'],
            'numberposts' => 100,
            'fields' => 'ids',
            'suppress_filters' => true,
        ]);

        foreach ($posts as $post_id) {
            wp_delete_post((int) $post_id, true);
        }
    } while (!empty($posts));
}

$options = [
    'pa_event_page_settings',
    'pa_speaker_page_settings',
    'pa_delete_data_on_uninstall',
];

foreach ($options as $option) {
    delete_option($option);
}

flush_rewrite_rules(false);
