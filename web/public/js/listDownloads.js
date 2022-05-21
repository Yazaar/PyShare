(function() {
    function detailClickEvent(e) {
        e.currentTarget.parentElement.classList.toggle('open');
    }

    var detailElements = document.querySelectorAll('.details');
    
    for (var i = 0; i < detailElements.length; i++) {
        detailElements[i].addEventListener('click', detailClickEvent);
    }
})();
