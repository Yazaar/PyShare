(function(){
    var uploading = false;
    var progressbar = document.querySelector('.innerProgressbar');
    var progressbarDetails = document.querySelector('.progressbarDetails');
    var fileselect = document.querySelector('.virtualUploadForm input#fileupload');
    document.querySelector('.virtualUploadForm button#uploadBtn').addEventListener('click', function(){
        var uploadThis = fileselect.files[0];
        if (uploadThis === undefined || uploading === true) {
            return;
        }
        uploading = true;
        var xml = new XMLHttpRequest();
        var form = new FormData();
        form.append('file', uploadThis);
        var sizename;
        var dividor;

        xml.upload.onloadstart = function(e){
            var total = e.total || e.totalSize;
            console.log(total);
            if (isNaN(total)) {
                sizename = 'B';
                dividor = 1;
            } else if (total > 1000000000) {
                sizename = 'GB';
                dividor = 1000000000;
            } else if (total > 1000000) {
                sizename = 'MB';
                dividor = 1000000;
            } else if (total > 1000) {
                sizename = 'KB';
                dividor = 1000;
            } else {
                sizename = 'B';
                dividor = 1;
            }
        }

        xml.upload.onprogress = function(e){
            var completed = e.loaded || e.position;
            var total = e.total || e.totalSize;
            if (isNaN(completed) || isNaN(total)) {
                return;
            }
            var percentage = Math.round(completed / total * 1000) / 10;
            progressbar.style.width = percentage + '%';
            progressbarDetails.innerText = (Math.round(completed/dividor*100)/100) + '/' + (Math.round(total/dividor*100)/100) + sizename + '(' + percentage + '%)';
        };
        
        xml.upload.onload = function(e){
            var total = e.total || e.totalSize;
            if (isNaN(total)) {
                progressbarDetails.innerText = 'File uploaded!';
            } else {
                progressbarDetails.innerText = 'File uploaded! (' + (Math.round(total/dividor*100)/100) + sizename + ')';
            }
            uploading = false;
        };



        xml.open('POST', '/upload');
        xml.send(form);
    });
})();