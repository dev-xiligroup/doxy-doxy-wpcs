<?php
/**
 * This file implements example wpcs.
 *
 * @author     Imichel
 *
 * @link       <URI>
 *
 * @package    WordPress
 * @subpackage 2021
 * @since      2021-04
 */

/**
 * Thanks to support of 20tauri himself.
 */

/**
 * Set the scripts.
 *
 * @param    <type> $script_list The script list.
 *
 * @return   <type> The scripts.
 */
function settings_scripts( $script_list ) {
	return $script_list;
}

/**
 * Searches for any matches launch.
 *
 * @param    <type> $script_list The script list.
 */
function find_any_launch( $script_list ) {
	do_action( 'toto' );
}

/**
 * Set the content width in pixels, based on the theme's design and stylesheet.
 *
 * Priority 0 to make it available to lower priority callbacks.
 *
 * @global int $content_width
 */
function twentyseventeen_content_width() {

	$content_width = $GLOBALS['content_width'];

	// Get layout.
	$page_layout = get_theme_mod( 'page_layout' );

	// Check if layout is one column.
	if ( 'one-column' === $page_layout ) {
		if ( twentyseventeen_is_frontpage() ) {
			$content_width = 644;
		} elseif ( is_page() ) {
			$content_width = 740;
		}
	}

	// Check if is single post and there is no sidebar.
	if ( is_single() && ! is_active_sidebar( 'sidebar-1' ) ) {
		$content_width = 740;
	}

	/**
	 * Filter Twenty Seventeen content width of the theme.
	 *
	 * @since Twenty Seventeen 1.0
	 *
	 * @param int $content_width Content width in pixels.
	 */
	$GLOBALS['content_width'] = apply_filters( 'twentyseventeen_content_width', $content_width );
}
add_action( 'template_redirect', 'twentyseventeen_content_width', 0 );
