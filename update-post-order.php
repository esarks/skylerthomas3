<?php
/**
 * Update Post Menu Order from WordPress Export
 * Upload this file to your WordPress root directory and visit it in your browser
 * DELETE this file after running!
 */

// Load WordPress
require_once(__DIR__ . "/wp-load.php");

// Check if user is admin
if (!current_user_can("manage_options")) {
    die("You must be logged in as an administrator to run this script.");
}

// Menu order mapping: post_id => menu_order
$post_order_map = array(
    7 => 1,
    1551 => 2,
    2302 => 3,
    329 => 4,
    1031 => 5,
    6017 => 6,
    1516 => 7,
    4061 => 8,
    2146 => 9,
    2148 => 10,
    2150 => 11,
    2190 => 12,
    2193 => 13,
    2198 => 14,
    2279 => 15,
    2281 => 16,
    2296 => 17,
    2300 => 18,
    2317 => 19,
    2318 => 20,
    2319 => 21,
    2321 => 22,
    4060 => 23,
    41 => 24,
    807 => 25,
    629 => 26,
    583 => 27,
    211 => 28,
    670 => 29,
    602 => 30,
    10242 => 31,
    1121 => 32,
    244 => 33,
    766 => 34,
    1333 => 35,
    600 => 36,
    203 => 37,
    34 => 38,
    217 => 39,
    290 => 40,
    2284 => 41,
    1384 => 42,
    355 => 43,
    365 => 44,
    800 => 45,
    241 => 46,
    265 => 47,
    52 => 48,
    1485 => 49,
    271 => 50,
    274 => 51,
    1457 => 52,
    135 => 53,
    281 => 54,
    301 => 55,
    622 => 56,
    946 => 57,
    560 => 58,
    341 => 59,
    326 => 60,
    75 => 61,
    1302 => 62,
    24 => 63,
    67 => 64,
    1377 => 65,
    287 => 66,
    1495 => 67,
    10238 => 68,
    276 => 69,
    781 => 70,
    238 => 71,
    785 => 72,
    937 => 73,
    911 => 74,
    1425 => 75,
    1322 => 76,
    138 => 77,
    1419 => 78
);

echo "<h1>Updating Post Menu Order</h1>";
echo "<pre>";

$updated = 0;
foreach ($post_order_map as $post_id => $menu_order) {
    $post = get_post($post_id);
    if ($post && $post->post_type === "post") {
        $result = wp_update_post(array(
            "ID" => $post_id,
            "menu_order" => $menu_order
        ));
        if ($result && !\is_wp_error($result)) {
            echo "✓ Updated post #$post_id: " . get_the_title($post_id) . " (menu_order = $menu_order)\n";
            $updated++;
        }
    }
}

echo "\n=================================\n";
echo "✓ Updated $updated posts\n";
echo "\nNow go to your WordPress admin and check the APTO post order!\n";
echo "\n⚠️  IMPORTANT: Delete this file (update-post-order.php) from your server now!\n";
echo "</pre>";
?>
