function generateTree(obj, root=false) {
    var sect = document.createElement('div');
    sect.classList.add('directory');
    if (root) {
        sect.classList.add('open');
    }
    var files = document.createElement('div');
    files.classList.add('files');
    var details = document.createElement('div');
    details.classList.add('details');
    details.title = 'Open / Close';
    details.addEventListener('click', function(){
        details.parentElement.classList.toggle('open');
    });
    var arrowIcon = document.createElement('div');
    arrowIcon.classList.add('arrowIcon');
    details.appendChild(arrowIcon);
    var dirname = document.createElement('p');
    dirname.classList.add('dirname');
    dirname.innerText = obj.name;
    details.appendChild(dirname);
    sect.appendChild(details);
    for (var i = 0; i < obj.files.length; i++) {
        if (obj.files[i].files !== undefined) {
            // directory
            files.appendChild(generateTree(obj.files[i]));
        } else {
            // file
            var data = obj.files[i];
            var file = document.createElement('div');
            file.classList.add('file');
            var downloadUrl = document.createElement('a');
            downloadUrl.innerText = data.name + ' (download)';
            downloadUrl.href = '/download/' + data.path;
            file.appendChild(downloadUrl);
            files.appendChild(file);
        }
    }
    sect.appendChild(files);
    return sect
}

function launch() {
    if (!window.fileTree) {
        return;
    }
    var downloadsTree = document.querySelector('#downloadsTree');
    if (downloadsTree === null) {
        return;
    }
    var tree = generateTree(fileTree, root=true);
    downloadsTree.appendChild(tree);
}

launch();