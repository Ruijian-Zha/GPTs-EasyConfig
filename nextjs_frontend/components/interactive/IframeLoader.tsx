import React, { useState, useEffect } from "react";
// @ts-ignore
const IframeLoader = ({ shouldDisplay }) => {
  const [iframeSrc, setIframeSrc] = useState("");

  useEffect(() => {
    const fetchIframeSrc = async () => {
      const response = await fetch("/api/getUrl?id=0");
      const data = await response.json();
      if (response.ok) {
        setIframeSrc(data.url);
      } else {
        console.error("Failed to fetch the iframe URL:", data.error);
      }
    };

    fetchIframeSrc();
    const intervalId = setInterval(fetchIframeSrc, 5000); // Changed to 5 seconds

    return () => clearInterval(intervalId);
  }, []);

  if (!shouldDisplay || !iframeSrc) {
    return null;
  }

  return (
    <iframe
      src={iframeSrc}
      style={{ width: "50%", height: "80vh", marginLeft: "10%" }}
      allowFullScreen
      loading="lazy"
      referrerPolicy="no-referrer-when-downgrade"
    ></iframe>
  );
};

export default IframeLoader;
