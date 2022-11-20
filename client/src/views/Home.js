import React, { useEffect } from 'react';
import './style/Home.css';


function Home() {
    
    useEffect(() => {
        const ws = new WebSocket(
          "wss://localhost:8001"
        );
    
        ws.onopen = () => {
          console.log("Connection Established!");
          ws.send("vid");
        };
        ws.onmessage = (event) => {
          const response = JSON.parse(event.data);
          console.log(response);

          //ws.close();
        };
        ws.onclose = () => {
          console.log("Connection Closed!");
          //initWebsocket();
        };
    
        ws.onerror = () => {
          console.log("WS Error");
        };
    
        return () => {
          ws.close();
        };
      }, []);

    const listCameras = cameras.map((camera) =>
        <div className='cam-container'>
            <img src={"data:image/png;base64, "{camera.img}}></img>
        </div>
    );
    return (
            <div className='home'>
                <h1>Cameras</h1>
                <div className='stopper'></div>
                <ul>{listCameras}</ul>
            </div>

    );
}

export default Home;