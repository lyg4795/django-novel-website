$(document).ready(function () {
    var options= {
        url: '/deleteRecord/',
        type:'post',
        success: function (data) {
            $('#record').html(data);
        },
        target:'#record'
    };
    $('#record_form').submit(

        function () {
            var check={'bookname':[]};
            $('input:checkbox').each(function() {
                if ($(this).prop('checked')) {
                    check.bookname.push($(this).val());
                }
            });
            $('form').ajaxSubmit({
                url: '/deleteRecord/',
                type:'post',
                target:'#record',
                data:check,
                success: function (data) {
                    $('#record').html(data);
                }
            });
        }
    );
    $('#update').click(
        function () {
            $.get('/update_novel',function (data) {
                $('#record').html(data)
            })
        }
    );
}
);
function sures()
{
return(confirm('确定继续？'));
}
