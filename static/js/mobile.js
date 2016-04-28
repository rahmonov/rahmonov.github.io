(function (root, $) {
    var $button = $('button.nav'),
        $nav = $('.side ul');

    $button.on('click', function () {
        $nav.slideToggle();
    });
}(window, jQuery));