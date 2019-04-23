///////////////////////////////////////////////////////////
// File        : BaseComponent.js
// Description : 

// GENERATED FROM UML - PLEASE DO NOT ADD/REMOVE ATTRIBUTES OR OPERATIONS

// Imports : 

import React from "react";
import { observer } from "mobx-react";

// Class Definition
export default
@observer
class BaseComponent extends React.Component {
// Attributes
  state = {unsavedChanges: false};

// Constructor
  constructor(props) {
    super(props);
    // console.log("constructor");
  }


// Operations
  componentWillMount() {
    // console.log("componentWillMount");
  }

  render() {
    console.log("render");
    return null;
  }

  componentDidMount() {
    // console.log("componentDidMount");
  }

  componentWillReceiveProps(nextProps) {
    // console.log("componentWillReceiveProps");
  }

  componentWillUpdate(nextProps,nextState) {
    // console.log("componentWillUpdate");
  }

  componentDidUpdate(prevProps,prevState) {
    // console.log("componentDidUpdate");
  }

  componentWillUnmount() {
    // console.log("componentWillUnmount");
  }

  componentDidCatch(error,info) {
    // console.log("componentDidCatch");
  }


}

// Exports

