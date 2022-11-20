import React, { useState } from "react";
import { NavLink } from 'react-router-dom';
import './style/NavBar.css';
import {ReactComponent as CloseMenu} from '../media/close_menu.svg'
import {ReactComponent as OpenMenu} from '../media/open_menu.svg'


function NavBar() {
        const [navbarOpen, setNavbarOpen] = useState(false)
        const handleToggle = () => {
            setNavbarOpen(!navbarOpen)
        }
        
    return (
            <div className={navbarOpen ? "open menu-bar" : "menu-bar"} >
                <div className="menu-head">
                    <i onClick={handleToggle} >{navbarOpen ? <CloseMenu/> : <OpenMenu/>}</i>
                </div>
                <nav>
                    <p>Hello doctor</p>
                    <NavLink exact to='/' className="option noselect" >Cameras</NavLink>
                    <NavLink exact to='/alerts' className="option noselect" >Alerts</NavLink>
                    <NavLink exact to='/rules' className="option noselect" >Rules</NavLink>
                    <NavLink exact to='/setup' className="option noselect" >Setup</NavLink>
                    <div className="stopper"></div>
                    <NavLink exact to='/settings' className="option noselect" >Settings</NavLink>
                </nav>
            </div>

    );
}

export default NavBar;