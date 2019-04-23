///////////////////////////////////////////////////////////
// File        : WhatsNew.js
// Description : 

import React from "react";
import { Grid, Row, Col, Glyphicon, PanelGroup, Panel } from "react-bootstrap";
import injectStyles from "react-jss";

import { BaseFormStyles } from "./BaseForm";

let styles = {
  panel: {
    "& .glyphicon":{
      marginRight: "20px",
    },
  },
  link: {
    textAlign: "right", 
    margin: "8px 0"
  },
};

// Imports : 

import BaseComponent from "./BaseComponent";

// Class Definition
export default
@injectStyles(Object.assign(BaseFormStyles, styles))
class WhatsNew extends BaseComponent {
// Attributes

// Constructor
  constructor(props) {
    super(props);
  }


// Operations
  render() {
    const { classes } = this.props;
    return (
      <Grid fluid={true} className={classes.container}>
        <Row>
          <Col xs={12} sm={8}>
            <h3>What&apos;s new!</h3>
          </Col>
        </Row>
        <Row>
          <Col xs={12} sm={10} smOffset={1}>
            <PanelGroup accordion defaultActiveKey="1" className={classes.panel} id="PanelGroupWhatsNew">
              <Panel eventKey="1">
                <Panel.Heading>
                  <Panel.Title toggle>This release...</Panel.Title>
                </Panel.Heading>
                <Panel.Body collapsible>
                  <div>
                    <Glyphicon glyph="thumbs-up"/>
                    <span>Demo App</span>
                  </div>
                  <div className={classes.link}>
                    <a href="/">Try it!</a>
                  </div>
                </Panel.Body>
              </Panel>
              <Panel eventKey="2">
                <Panel.Heading>
                  <Panel.Title toggle>Previous releases...</Panel.Title>
                </Panel.Heading>
                <Panel.Body collapsible>
                  <div>
                    <Glyphicon glyph="hand-right"/>
                    <span>Report problems or requests</span>
                  </div>
                  <div className={classes.link}>
                    <a href="mailto:?subject=APP: ">Click &apos;Contact Us&apos;</a>
                  </div>
                </Panel.Body>
              </Panel>
            </PanelGroup>
          </Col>
        </Row>
      </Grid>
    );
  }


}

// Exports

