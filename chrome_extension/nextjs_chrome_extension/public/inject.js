console.log("Message from inject.js")

// Fetch the HTML content of index.html
// fetch(chrome.runtime.getURL('index.html'))
//   .then(response => response.text())
//   .then(data => {
//     // Create a container for the side panel
//     const sidePanel = document.createElement('div');
//     sidePanel.innerHTML = data;
//     // Apply some basic styles to position the side panel
//     Object.assign(sidePanel.style, {
//       position: 'fixed',
//       right: '0',
//       top: '0',
//       width: '300px', // Adjust the width of the side panel as needed
//       height: '100%',
//       backgroundColor: 'white',
//       zIndex: '1000', // Ensure it's on top of other elements
//       overflow: 'auto'
//     });
//     document.body.appendChild(sidePanel);
//   })
//   .catch(err => console.error(err));