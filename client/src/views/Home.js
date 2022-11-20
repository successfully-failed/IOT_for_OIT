import React, { useEffect } from 'react';
import './style/Home.css';


function Home() {
    
    useEffect(() => {
        const ws = new WebSocket(
          "ws://localhost:8001"
        );
    
        ws.onopen = () => {
          console.log("Connection Established!");
          ws.send(JSON.stringify({""}));
        };
        ws.onmessage = (event) => {
          const response = JSON.parse(event.data);
          console.log("RESPONSE: ", response);

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
    
    const cameras = [0,1,2,3]
    const listCameras = cameras.map((camera) =>
        <div className='cam-container'>
            <img src="data:image/png;base64, iVBORw0KGgoAAAANSUhEUgAAAAUA
    AAAFCAYAAACNbyblAAAAHElEQVQI12P4//8/w38GIAXDIBKE0DHxgljNBAAO
        9TXL0Y4OHwAAAABJRU5ErkJggg==" alt="Red dot" ></img>
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