function addObserverIfDesiredNodeAvailable() {
    let target = document.querySelector('.user-information-button .status-icon');
    if(!target) {
        // The node we need does not exist yet.
        window.setTimeout(addObserverIfDesiredNodeAvailable, 500);
        return;
    }
    let observer = new MutationObserver(function(mutations) {
        mutations.forEach(function(mutation) {
            let presenceStatus = mutation.target.classList[2];
            let xhr = new XMLHttpRequest();
            xhr.open("POST", "http://localhost:5000", true);
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
