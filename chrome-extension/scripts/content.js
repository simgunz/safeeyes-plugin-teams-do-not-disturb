function addObserverIfDesiredNodeAvailable() {
    let target = document.querySelector('.me-control-avatar-badge');
    if(!target) {
        // The node we need does not exist yet.
        window.setTimeout(addObserverIfDesiredNodeAvailable, 500);
        return;
    }
    let observer = new MutationObserver(function(mutations) {
        mutations.forEach(function(mutation) {
            let presenceStatus = mutation.target.ariaLabel;
            let xhr = new XMLHttpRequest();
            xhr.open("POST", "http://localhost:6776", true);
            xhr.setRequestHeader('Content-Type', 'application/json');
            xhr.send(JSON.stringify({
                status: presenceStatus,
            }));
        });
    });
    let config = { attributes: true };
    observer.observe(target, config);
}

addObserverIfDesiredNodeAvailable();
