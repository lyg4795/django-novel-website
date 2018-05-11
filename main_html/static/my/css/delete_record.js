$(document).ready(function () {
    $('#delete').click(
    function () {
        $.get('/deleteRecord',function (data) {
            $('#record').html(data);
        });
    }
    );
});

