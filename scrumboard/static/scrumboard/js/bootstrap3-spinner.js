(function ($) {

    $('.spinner .btn:first-of-type').on('click', function() {
        $input = $(this).closest('.spinner').find('input');
        $input.val(parseInt($input.val(), 10) + 1);
    });

    $('.spinner .btn:last-of-type').on('click', function() {
        $input = $(this).closest('.spinner').find('input');
        $input.val(parseInt($input.val(), 10) - 1);
    });

})(jQuery);