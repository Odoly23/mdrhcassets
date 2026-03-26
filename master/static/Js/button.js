$(function() {
    const sidebar = $('#sidebar');
    const mainContent = $('#mainContent');
    const overlay = $('#sidebarOverlay');
    const toggleBtn = $('#sidebarToggle');

    function toggleSidebar() {
        if ($(window).width() <= 991.98) {
            sidebar.toggleClass('show');
            overlay.toggleClass('active');
        } else {
            sidebar.toggleClass('collapsed');
            mainContent.toggleClass('expanded');
        }
    }

    toggleBtn.on('click', toggleSidebar);

    overlay.on('click', function() {
        sidebar.removeClass('show');
        overlay.removeClass('active');
    });

    $('.custom-file-input').on('change', function() {
        let fileName = $(this).val().split('\\').pop();
        $(this).next('.custom-file-label').html(fileName || 'Choose file');
    });

    $('.nav-link').on('click', function() {
        if ($(window).width() <= 991.98) {
            sidebar.removeClass('show');
            overlay.removeClass('active');
        }
    });
});