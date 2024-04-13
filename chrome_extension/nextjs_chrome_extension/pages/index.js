import React, { useState, useEffect } from 'react';
import Index from '../components/Index';
import New from '../components/New';

export default function Home() {
  const [activePage, setActivePage] = useState('index');

  useEffect(() => {
    setupWebSocketConnection();
    // Other initialization code
  }, []);

  const navigateToPage = (page) => {
    setActivePage(page);
  };

  function setupWebSocketConnection() {
    const connection = new WebSocket('ws://localhost:3000');

    connection.onopen = () => {
      console.log('WebSocket connection established.');
    };

    connection.onmessage = event => {
      const message = JSON.parse(event.data);

      switch (message.type) {
        case 'url':
          chrome.tabs.query({active: true, currentWindow: true}, (tabs) => {
            const currentTab = tabs[0];
            if (currentTab) {
              chrome.tabs.update(currentTab.id, {url: message.data});
            }
          });
          break;
        case 'new-url':
          chrome.tabs.create({url: message.data});
          break;
        // Handle other message types...
      }
    };

    connection.onclose = () => {
      console.log('WebSocket connection closed. Attempting to reconnect...');
      setTimeout(setupWebSocketConnection, 1000);
    };

    connection.onerror = (error) => {
      console.error('WebSocket encountered an error:', error);
      connection.close();
    };
  }

  return (
    <>
      {activePage === 'index' && <Index navigateToPage={navigateToPage} />}
      {activePage === 'new' && <New navigateToPage={navigateToPage} />}
    </>
  );
}