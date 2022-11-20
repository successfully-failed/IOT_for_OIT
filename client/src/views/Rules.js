import './style/Rules.css';
import React, { useState } from 'react';

const detectionList = {
    1: 'Stomachache',
    2: 'No drip',
    3: 'Stand up'
};

const actionList = {
    1: 'Notificate',
    2: 'Flash lights',
    3: 'Start alarm'
};


var allRules = [];
allRules.push(<RuleContainer></RuleContainer>);

// function returnDetectionList() {
//     const list = [];
//     for (let i = 1; i <= 3; i++) {
//         list.push(detectionList[i]);
//     }
//     return (<option>{list}</option>)
// }

function RulesPage() {
    return (
        <div className='rules-page'>
            <header>
            <h1>Set your rules</h1>
            <h1>Active rules: X</h1>
            
            </header>
            <MainRulesContainer>
            </MainRulesContainer>
        </div>
    )
}
let rerenderglob, setRerendererglob;
function MainRulesContainer() {
    const [rerender, setRerender] = useState(false);
    rerenderglob = rerender;
    setRerendererglob = setRerender;

    return (
        <main>
            {allRules}
        </main>
    )
}

// let json = require('./../../../../log/rules.json');
// console.log(json);

function RuleContainer() {
    function saveRule(e) {
      e.preventDefault();
      //let camera = document.querySelector("#detection");
      let detection = document.querySelector("#detection").value;
      let action = document.querySelector("#action").value;
      console.log(detection);
      console.log(action);

        

      const readyRuleContainer = (
        <div className="ready-rule-container">
            <p></p>
            <p>IF</p>
            <p>{detection}</p>
            <p>THEN</p>
            <p>{action}</p>
        </div>
      )
      allRules.push(readyRuleContainer);
      console.log(allRules);
      setRerendererglob(!rerenderglob);
    }

    function deleteRule() {
    }
    return (
        <form onSubmit={saveRule} onReset={deleteRule}>
            <div className='rule-container'>
                <CameraSelector />
                <p>IF</p>
                <DetectionSelector />
                <p>THEN</p>
                <ActionSelector />
                <SaveButton />
                <DeleteButton />
            </div>
        </form>
    )
}

function CameraSelector() {
    return (
        <div className='camera-selector'>
            <select>
                
            </select>
        </div>
    )
}

function DetectionSelector() {
    return (
        <div className='detection-selector'>
            <select id="detection">
                <option>{detectionList[1]}</option>
                <option>{detectionList[2]}</option>
                <option>{detectionList[3]}</option>

            </select>
            
        </div>
    );
}

function ActionSelector() {
    return (
        <div className='action-selector'>
            <select id="action">
                <option>{actionList[1]}</option>
                <option>{actionList[2]}</option>
                <option>{actionList[3]}</option>
            </select>
        </div>
    )
}

function SaveButton() {
    return (
        <button type="submit">SAVE</button>
    );
}

function DeleteButton() {
    return (
        <button type="reset">DELETE</button>
    );
}

export default RulesPage;