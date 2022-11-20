import React, { useState } from "react";
import { Link, NavLink } from 'react-router-dom';
import OutsideClickHandler from 'react-outside-click-handler';
import './style/NavBar.css';


function Menu() {
        const [navbarOpen, setNavbarOpen] = useState(false)
        const handleToggle = () => {
            setNavbarOpen(!navbarOpen)
        }
        
    return (
        <OutsideClickHandler onOutsideClick={() => {setNavbarOpen(false)}}>
            <div className={navbarOpen ? "open menu-bar" : "menu-bar"} >
                <div className="first-menu-line">
                    <Link to='/' ><Logo className={"logo"}/></Link>
                    <i onClick={handleToggle} >{navbarOpen ? <CloseMenu/> : <OpenMenu/>}</i>
                </div>
                <nav>
                    <NavLink exact to='/' className="option noselect" >Home</NavLink>
                    <NavLink exact to='/about' className="option noselect" >About</NavLink>
                    <NavLink exact to='/contact' className="option noselect" >Contact</NavLink>
                    <NavLink exact to='/login' className="option noselect" >Login</NavLink>
                </nav>
            </div>
            
        </OutsideClickHandler>

    );
}

export default Menu;