import React, { useEffect, useState } from 'react';
import './style/Home.css';


function Home() {
    const [cameras, setCameras] = useState([]);
    const fetch_cam = () => {
        useEffect(() => {
                fetch('/cameras')
                .then(response => response.json())
                .then(json => setCameras(json))
        }, []);
    }
    
    const listCameras = cameras.map((camera) =>
        <div className='cam-container'>
            <div className={
                (camera.status==='0') ? ('cam-view green') :
                (camera.status==='1') ? ('cam-view orange') :
                (camera.status==='2') ? ('cam-view red') : alert('Given bad data!')}>
                    <img src={camera.img} alt='camera view'></img></div>
            <p>{camera.id}</p>
        </div>
    );

    return (
            <div className='home'>
                <h1>Cameras</h1>
                <div className='stopper'></div>
                <div className='all-cameras'>{listCameras} {(cameras.length === 0) ? "No camera!" : null}</div>
                {fetch_cam}
            </div>

    );
}

export default Home;

/*   */