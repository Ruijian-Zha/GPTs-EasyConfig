"use client";

import { useState, useEffect, useRef } from "react";
import { Excalidraw, convertToExcalidrawElements } from "@excalidraw/excalidraw";

const ExcalidrawWrapper: React.FC = () => {
  const [elements, setElements] = useState(
    convertToExcalidrawElements([
      {
        type: "rectangle",
        x: 50,
        y: 250,
      },
      {
        type: "ellipse",
        x: 250,
        y: 250,
      },
      {
        type: "diamond",
        x: 380,
        y: 250,
      },
    ])
  );
  const [key, setKey] = useState(0);

  useEffect(() => {
    let countdown = 10;
    console.log(`Countdown: ${countdown}`);

    const interval = setInterval(() => {
      countdown -= 1;
      console.log(`Countdown: ${countdown}`);

      if (countdown === 0) {
        setElements([]);
        setKey(prevKey => prevKey + 1); // Change the key to reload the component
        clearInterval(interval);
      }
    }, 1000); // 1 second

    return () => clearInterval(interval); // Clean up on component unmount
  }, []);

  return (
    <div style={{ width: '50%' }} key={key}>
      <Excalidraw
        initialData={{
          elements,
        //   appState: { zenModeEnabled: true, viewBackgroundColor: "#a5d8ff" },
          appState: { zenModeEnabled: true },
          scrollToContent: true,
        }}
      />
    </div>
  );
};

export default ExcalidrawWrapper;