$(document).ready(function() {
    let offset = initialOffset; // Используем глобальную переменную, определённую в шаблоне
    const limit = 20;

    $('#reset-filters').click(function(e) {
        e.preventDefault();
        window.location.href = employeeListUrl; // Используем глобальную переменную
    });

    $('#load-more').click(function(e) {
        e.preventDefault();
        loadMoreEmployees(offset, $('#filter-form').serialize());
    });

    $('.sortable a').click(function(e) {
        e.preventDefault();
        const currentOrdering = $(this).data('ordering');
        const newOrdering = currentOrdering.startsWith('-') ? currentOrdering.slice(1) : '-' + currentOrdering;
        $('.sortable a').removeClass('active');
        $(this).addClass('active');
        $(this).data('ordering', newOrdering);
        loadSortedEmployees(newOrdering, $('#filter-form').serialize());
    });

    $('#filter-form').submit(function(e) {
        e.preventDefault();
        offset = initialOffset; // Сбрасываем offset
        loadSortedEmployees(getOrdering(), $(this).serialize());
    });

    function loadMoreEmployees(currentOffset, filterData) {
        $.ajax({
            url: loadMoreEmployeesUrl, // Используем глобальную переменную
            type: 'GET',
            data: filterData + '&offset=' + currentOffset + '&ordering=' + getOrdering(),
            success: function(data) {
                $('#employee-rows').append(data.html);
                offset += limit;
            },
            error: function(xhr, status, error) {
                console.error('Ошибка при загрузке:', error);
            }
        });
    }

    function loadSortedEmployees(ordering, filterData = '') {
        $.ajax({
            url: employeeListUrl, // Используем глобальную переменную
            type: 'GET',
            data: filterData + '&ordering=' + ordering,
            success: function(data) {
                const newRows = $(data).find('#employee-rows').html();
                $('#employee-rows').html(newRows);
                offset = initialOffset; // Сбрасываем offset
            },
            error: function(xhr, status, error) {
                console.error('Ошибка при сортировке:', error);
            }
        });
    }

    function getOrdering() {
        return $('.sortable a.active').data('ordering') || 'id';
    }
});
