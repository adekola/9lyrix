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

            var is_remix = $('#remix').value == "Yes";
            var form_data = {
                title: $('#title').val(),
                artist: $('#artist').val(),
                year: $('#year').val(),
                remix: is_remix,
                lyrics: $('#lyrics').val()
            }

            var post_data = JSON.stringify(form_data);

            $.ajax({
                cache: false,
                url: "http://" + window.location.host+"/v1/song/",
                data: post_data,
                dataType: 'html',
                type: 'POST',
                success: function (json) {
                    $('form').fadeOut();
                    $('#ajaxResult').append(json).fadeIn().show();
                    $('#submitSuccess').fadeIn().show();
                },
                fail: function (json) {
                    $('#submitFail').show();
                }
            });
        });

        //set what happens when the Add New button is clicked
        $('#addNew').click(function () {

        });

        $('#clearForm').click(function () {
            $('#artist').value = "";
            $('#year').value = "";
            $('#remix').selectedIndex = 0;
            $('#lyrics').value = "";
            $('#title').value = "";
        });



})(jQuery);

