///////////////////////////////////////////////////////////
// File        : PersonQuery.js
// Description : 

// Imports : 

import React from "react";
import { observer, inject } from "mobx-react";
import { Row, Grid, Col } from "react-bootstrap";
import { Form, FormStore, Field } from "hbp-quickfire";
import injectStyles from "react-jss";

import BaseQueryView from "./BaseQueryView";
import PersonList from "./PersonList";

let styles = {
  container:{
  },
  form:{
    paddingTop:"20px"
  }
};

let personQueryConfig = {
  fields: {
    first_name: {
      label: "First Name",
      type: "InputText"
    },
    last_name: {
      label: "Last Name",
      type: "InputText"
    }
  }
};

// Class Definition
export default
@injectStyles(styles)
@inject(stores => ({ store: stores.personStore }))
@observer
class PersonQuery extends BaseQueryView {
// Attributes

// Constructor
  constructor(props) {
    super(props, new FormStore(personQueryConfig));
  }


// Operations
  render() {
    // super.render();
    const {classes} = this.props;
    return (
      <Grid fluid={true} className={classes.container}>
        <Row>
          <Col xs={12} md={3} mdPush={8} className={classes.form}>
            <Form store={this.formStore}>
              <Row>
                <Col title="Any part of the person's first name">
                  <Field name="first_name" onChange={this.onChange.bind(this)} />
                </Col>
              </Row>
              <Row>
                <Col title="Any part of the person's last name">
                  <Field name="last_name" onChange={this.onChange.bind(this)} />
                </Col>
              </Row>
            </Form>
          </Col>
          <Col xs={12} md={8} mdPull={3}>
            <h3>Results: <span className="badge">{this.props.store.items.length}</span></h3>
            <PersonList store={this.props.store} />
          </Col>
        </Row>
      </Grid>
    );
  }


}

// Exports

