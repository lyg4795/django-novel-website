$(document).ready(function () {
    $('#delete').click(
        function () {
            $.get('/deleteRecord',function (data) {
                $('#record').html(data);
            });
        }
        // alert("aaa")
    );
    $('#update').click(
        function () {
            $.get('/update_novel',function (data) {
                $('#record').html(data)
            })
        }
    );
});

