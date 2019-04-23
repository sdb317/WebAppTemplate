///////////////////////////////////////////////////////////
// File        : PersonView.js
// Description : 

// Imports : 

import React from "react";
import { observer, inject } from "mobx-react";
import { Grid, Col, Row } from "react-bootstrap";
import injectStyles from "react-jss";

import { BaseForm, BaseFormStyles } from "./BaseForm";
import DisseminationPlanDetails from "./DisseminationPlanDetails";

let styles = {
};

// Class Definition
export default
@injectStyles(Object.assign(BaseFormStyles, styles))
@inject(stores => ({ store: stores.disseminationPlanStore }))
@observer
class PersonView extends DisseminationPlanDetails {
// Attributes

// Constructor

// Operations
  render() {
  }


}

// Exports

