///////////////////////////////////////////////////////////
// File        : PersonDetails.js
// Description : 

// Imports : 

import React from "react";
import { observer, inject } from "mobx-react";
import { Grid, Col, Row } from "react-bootstrap";
import { Form, Field } from "hbp-quickfire";
import injectStyles from "react-jss";

import { BaseForm, BaseFormStyles } from "./BaseForm";
// import ConfirmField from "./ConfirmField";

// Class Definition
export default
@injectStyles(BaseFormStyles)
@inject(stores => ({ store: stores.personStore }))
@observer
class PersonDetails extends BaseForm {
// Attributes

// Constructor
  constructor(props) {
    super(props);
    this.formStore = this.props.store.formStore;
  }


// Operations
  render() {
    const { classes, store } = this.props;
    return (
      <Grid fluid={true} className={classes.container} onChange={this.handleFormChange}>
        <Row>
          <Col xs={12}>
            <h3>Person Entry</h3>
          </Col>
        </Row>
        <Form store={store.formStore}>
          <style type="text/css">{this.styleOverrides}</style>
          <Row>
            <Col xs={12} title="">
              <Field name="first_name" />
            </Col>
          </Row>
          <Row>
            <Col xs={12} title="">
              <Field name="last_name" />
            </Col>
          </Row>
          <Row>
            <Col xs={12} title="">
              <Field name="email" />
            </Col>
          </Row>
          <Row>
            <Col xs={12} title="">
              <Field name="type" />
            </Col>
          </Row>
        </Form>
        {super.renderSaveNewDelete()}
      </Grid>
    );
  }


}

// Exports

