window.addEventListener('load', function(){
    var widget = $('.l-auction-edit .gallery-widget');
    var photo_save_url = widget.attr('data-photo-save-url');
    var files = [];
    var filesQueueLength = 0;
    var progressEl = widget.find('.progress-bar');

    widget.find('.btn').on('click', function(e){
        var input = document.createElement('input');
        input.type = 'file';
        input.multiple = 'multiple';
        input.accept = "image/*";
        input.click();
        input.onchange = function(e) {
            files = e.target.files;
            uploadFiles.call(self, files);
        }
    });

    function uploadFiles() {
        filesQueueLength = files.length;

        for(var i=0; i<files.length; i++) {
            var file = files[i];
            doUploadFile(file);
        }
    }

    function doUploadFile(file) {

        var formData = new FormData();
        formData.append('file', file);

        $.ajax({
            url: photo_save_url,
            dataType: 'text',
            cache: false,
            contentType: false,
            processData: false,
            data: formData,
            type: 'post',
            success: function(resp){
                resp = $.parseJSON(resp);
                console.log(resp);
                if(!resp.result) {
                    alert(resp.msg);
                    return;
                }

                filesQueueLength--;
                var progress;
                if(filesQueueLength == 0) {
                    progress = progressEl.parent().width();
                } else {
                    progress = (files.length-filesQueueLength)*progressEl.parent().width()/files.length;
                }
                progressEl.width(progress);
                if(filesQueueLength === 0) {
                    window.location.reload();
                }
            }
        });
    }

    var script = document.createElement('script');
    script.src = "/static/js/lib/jquery.datetimepicker.full.min.js";
    $('body').append(script);

    $.datetimepicker.setLocale('ru');
    $('#end_date').datetimepicker({
        format: 'Y-m-d H:i',
        scrollInput: false
    });
});