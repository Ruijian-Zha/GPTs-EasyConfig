(function() {
    const iframe = document.createElement('iframe');
    iframe.style.height = '100px'; // Adjust size as needed
    iframe.style.width = '300px'; // Adjust size as needed
    iframe.style.position = 'fixed';
    iframe.style.top = '0';
    iframe.style.right = '0';
    iframe.style.zIndex = '1000'; // Ensure it's above other content
    iframe.src = chrome.runtime.getURL('index.html');
    document.body.appendChild(iframe);
  })();