<?php
/**
 * Plugin Name: Fix Post Navigation (Menu Order)
 * Description: Navigation based on menu_order with correct arrow directions
 * Version: 7.0
 * Author: Claude
 */

// Get adjacent posts based on menu_order
function fpn_get_adjacent_posts() {
    global $post;

    if (!is_singular('post') || !$post) {
        return array('prev' => null, 'next' => null);
    }

    // Get all published posts ordered by menu_order
    $all_posts = get_posts(array(
        'post_type' => 'post',
        'post_status' => 'publish',
        'posts_per_page' => -1,
        'orderby' => 'menu_order',
        'order' => 'ASC',
        'fields' => 'ids'
    ));

    // Find current post position
    $current_position = array_search($post->ID, $all_posts);

    if ($current_position === false) {
        return array('prev' => null, 'next' => null);
    }

    // Get adjacent posts
    $prev_id = isset($all_posts[$current_position - 1]) ? $all_posts[$current_position - 1] : null;
    $next_id = isset($all_posts[$current_position + 1]) ? $all_posts[$current_position + 1] : null;

    return array(
        'prev' => $prev_id ? get_post($prev_id) : null,
        'next' => $next_id ? get_post($next_id) : null
    );
}

// Override the navigation output completely
add_filter('the_post_navigation', 'fpn_custom_navigation', 10, 2);
function fpn_custom_navigation($output, $args) {
    if (!is_singular('post')) {
        return $output;
    }

    $adjacent = fpn_get_adjacent_posts();
    $prev_post = $adjacent['prev'];
    $next_post = $adjacent['next'];

    if (!$prev_post && !$next_post) {
        return '';
    }

    ob_start();
    ?>
    <nav class="navigation post-navigation" role="navigation" aria-label="Posts">
        <h2 class="screen-reader-text">Post navigation</h2>
        <div class="nav-links">
            <?php if ($prev_post): ?>
                <div class="nav-previous">
                    <a href="<?php echo get_permalink($prev_post); ?>" rel="prev">
                        <span class="meta-nav" aria-hidden="true">←</span>
                        <span class="screen-reader-text">Previous post:</span>
                        <span class="post-title"><?php echo get_the_title($prev_post); ?></span>
                    </a>
                </div>
            <?php endif; ?>

            <?php if ($next_post): ?>
                <div class="nav-next">
                    <a href="<?php echo get_permalink($next_post); ?>">
                        <span class="screen-reader-text">Next post:</span>
                        <span class="post-title"><?php echo get_the_title($next_post); ?></span>
                        <span class="meta-nav" aria-hidden="true">→</span>
                    </a>
                </div>
            <?php endif; ?>
        </div>
    </nav>
    <?php
    return ob_get_clean();
}

// Also override via JavaScript as absolute fallback
add_action('wp_footer', 'fpn_js_override');
function fpn_js_override() {
    if (!is_singular('post')) {
        return;
    }

    $adjacent = fpn_get_adjacent_posts();
    $prev_post = $adjacent['prev'];
    $next_post = $adjacent['next'];

    ?>
    <script type="text/javascript">
    (function($) {
        $(document).ready(function() {
            // Find the navigation meta-nav spans
            var $nav = $('.post-navigation');

            if ($nav.length) {
                // Replace "Previous" with left arrow
                $nav.find('.nav-previous .meta-nav').text('←');

                // Replace "Next" with right arrow
                $nav.find('.nav-next .meta-nav').text('→');

                // Update the links to use menu_order navigation
                <?php if ($prev_post): ?>
                $nav.find('.nav-previous a').attr('href', '<?php echo get_permalink($prev_post); ?>');
                $nav.find('.nav-previous .post-title').text('<?php echo esc_js(get_the_title($prev_post)); ?>');
                <?php endif; ?>

                <?php if ($next_post): ?>
                $nav.find('.nav-next a').attr('href', '<?php echo get_permalink($next_post); ?>');
                $nav.find('.nav-next .post-title').text('<?php echo esc_js(get_the_title($next_post)); ?>');
                <?php endif; ?>
            }
        });
    })(jQuery);
    </script>
    <?php
}
