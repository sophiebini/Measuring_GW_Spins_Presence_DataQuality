$(document).ready(function() {
    // Function to get URL parameters
    function getUrlParameter(name, url) {
        name = name.replace(/[\[\]]/g, "\$&");
        var regex = new RegExp("[?&]" + name + "(=([^&#]*)|&|#|$)"),
            results = regex.exec(url);
        return results ? decodeURIComponent(results[2].replace(/\+/g, " ")) : null;
    }

    // Function to try fetching from the primary path, then fallback if necessary
    function fetchWithFallback(primaryPath, fallbackPath) {
        return fetch(primaryPath)
            .then(response => {
                if (!response.ok) {
                    // If the primary path fails, try the fallback path
                    return fetch(fallbackPath);
                }
                return response;
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Page not found');
                }
                return response.text();
            });
    }

    function loadMainFromHtml(primaryPath, fallbackPath) {
        fetchWithFallback(primaryPath, fallbackPath)
            .then(htmlContent => {
                $("#main").html(htmlContent);
            })
            .catch(error => {
                console.error('Error loading main content:', error);
                $("#main").html('<p>Page not found</p>');
            });
    }

    // Function to load content into the main div
    function loadContentIntoMain(content, contentType) {
        $("#main").html(content);
        console.log(`${contentType} loaded`);
    }

    // Function for the initial page setup
    function setupInitialPage() {
        // Set up initial state based on the URL
        var queryParams = new URLSearchParams(window.location.search);
        var initialModel = queryParams.get('model') || 'summary';

        var fallbackPath = `./html/${initialModel}_page.html`;
        var primaryPath = `./1_main/html/${initialModel}_page.html`;

        // Check for 'img' parameter in the URL
        var initialImage = getUrlParameter('img', window.location.href);
        if (initialImage) {
            // If 'img' parameter is present, load the image into the main div
            loadContentIntoMain(`<img src="${initialImage}" alt="Loaded Image">`, 'Image');
        } else {
            // Otherwise, load the initial page with fallback
            loadMainFromHtml(primaryPath, fallbackPath);
        }
    }

    // Call the setupInitialPage function
    setupInitialPage();

    $(".menuitem").click(function() {
        var itemId = this.id;

        var fallbackPath = `./html/${itemId}_page.html`;
        var primaryPath = `./1_main/html/${itemId}_page.html`;

        // Update or add the 'model' parameter
        var queryParams = new URLSearchParams(window.location.search);
        queryParams.set('model', itemId);
        // Clear any previously loaded image
        queryParams.delete('img');

        // Create a new URL with the updated parameters
        var newUrl = `${window.location.pathname}?${queryParams.toString()}`;
        window.history.pushState({ model: itemId }, '', newUrl);

        // Load the content into the main div with fallback
        loadMainFromHtml(primaryPath, fallbackPath);

        window.parent.postMessage({ action: 'modelChanged', model: itemId, url: newUrl }, '*');
        console.log("model changed ", itemId);
    });

    // Add click event listener to the common ancestor (main div)
    $("#main").on('click', '.clickableImage', function(event) {
        console.log("you clicked a clickableImage");
        var imageUrl = this.src;

        // Load the image into the main div
        loadContentIntoMain(`<img src="${imageUrl}" alt="Loaded Image">`, 'Image');

        // Update or add the 'img' parameter
        var queryParams = new URLSearchParams(window.location.search);
        queryParams.delete('img');
        queryParams.set('img', imageUrl);

        // Create a new URL with the updated parameters
        var newUrl = `${window.location.pathname}?${queryParams.toString()}`;
        window.history.pushState({ "img": imageUrl }, '', newUrl);

        window.parent.postMessage({ action: 'urlUpdate', url: newUrl }, '*');
    });

});

// Toggle function
function toggle(showHideDiv, switchTextDiv) {
    var ele = document.getElementById(showHideDiv);
    var text = document.getElementById(switchTextDiv);
    if(ele.style.display === "block") {
        ele.style.display = "none";
        text.innerHTML = "show";
    }
    else {
        ele.style.display = "block";
        text.innerHTML = "hide";
    }
}

// function to load text file into element
function loadTextFileIntoElement(filePath, elementId) {
    fetch(filePath)
        .then(response => response.text())
        .then(data => {
            // Update the content of the specified element with the loaded text
            document.getElementById(elementId).innerText = data;
        })
        .catch(error => console.error('Error:', error));
}

