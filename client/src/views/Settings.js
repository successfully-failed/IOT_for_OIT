import React, { useEffect } from 'react';
import './style/Settings.css';

export default SettingsPage;

function SettingsPage() {
    
    useEffect(() => {
        let switchStatus = false;
        const statusEl = document.querySelector("#status");
        const switcher = document.querySelector("#switch");
        const infoParagraph = document.querySelector("#paragraph");
        switcher.addEventListener('click', () => {
            switchStatus ? switcher.classList.remove("deactivated-switcher") : switcher.classList.add("deactivated-switcher");
            switchStatus ? statusEl.classList.remove("deactivated-status") : statusEl.classList.add("deactivated-status") ;
            switchStatus ? infoParagraph.classList.remove("no-display") : infoParagraph.classList.add("no-display");
            switcher.innerHTML = switchStatus ? 'Deactivate AI' : 'Activate AI';
            switchStatus = !switchStatus;
        });
    })

    return (
    <div id="SettingsPage">
        <h1>Settings Page</h1>
        <div id="prompt-container">
            <h2 id="status"></h2>
            <button id="switch">Deactivate AI</button>
            <p id="paragraph">Warning! Process of deactivating will disable AI and its dependencies.</p>
        </div>
    </div>
    )
}