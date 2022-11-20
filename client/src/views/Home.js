import React, { useEffect } from 'react';
import './style/Home.css';


function Home() {
    
    const cameras = [
        {id: 0, img: "", status: '2'},
        {id: 1, img: "", status: '0'},
        {id: 2, img: "", status: '1'},
        {id: 3, img: "", status: '0'},
        {id: 4, img: "", status: '2'},
    ]
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
                <div className='all-cameras'>{listCameras}</div>
            </div>

    );
}

export default Home;

/*   */