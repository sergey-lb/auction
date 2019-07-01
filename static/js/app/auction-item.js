window.addEventListener('load', function(){
    $('.tree .respond').on('click', function(e){
        var formContainer = $(this).closest('.comment').find('.ondemand');
        if(formContainer.hasClass('d-none')) {
            formContainer.removeClass('d-none');
        } else {
            formContainer.addClass('d-none');
        }
        return false;
    });
});