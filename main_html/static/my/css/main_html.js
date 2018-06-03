$(document).ready(function () {
    var options= {
        url: '/deleteRecord/'
        // success: function (data) {
        //     $('#record').html(data);
        // }
        // target:'#record'
    };
    $('#record_form').submit(
        function () {
            $('form').ajaxSubmit(options);
            alert("aaa");
            // return false;
            // alert("aaa")
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
