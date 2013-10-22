/**
 * Created with PyCharm.
 * User: adekola
 * Date: 10/7/13
 * Time: 3:15 PM
 * To change this template use File | Settings | File Templates.
 */

(function($){
     //now set the actions for when the respective buttons are clicked
        $('#submitForm').click(function (event) {
            //retrieve the field values
            event.preventDefault();

            var form_data = $('form').serialize();
            $.ajax({
                cache: false,
                url: "http://" + window.location.host+"/addLyrics",
                data: form_data,
                dataType: 'html',
                type: 'POST',
                success: function (json) {
                    $('form').fadeOut();
                    $('#ajaxResult').append(json).fadeIn().show();
                    $('#submitSuccess').removeAttr("hidden").fadeIn();
                },
                fail: function (json) {
                    $('#ajaxFail').show();
                }
            });
        });

        //set what happens when the Add New button is clicked
        $('#addNew').click(function () {
            $.get("http://" + window.location.host);
        });

        $('#clearForm').click(function () {
            $('#artist').clearData();
            $('#year').clearData();
            $('#remix').selectedIndex = 0;
            $('#lyrics').clearData();
            $('#title').clearData();
        });
})(jQuery);

