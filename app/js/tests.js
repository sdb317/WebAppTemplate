/* Display whole app */
import React from "react";
import ReactDOM from "react-dom";
import App from "./Components/App";
document.getElementById("qunit-dashboard").style.display="none";
ReactDOM.render(<App/>, document.getElementById("react"));

// Component tests
// import Component from './Components/PersonQuery.tests';
// import Component from './Components/WhatsNew.tests';

// Store tests
// import Component from './Stores/Persons.tests';

