///////////////////////////////////////////////////////////
// File        : PersonList.js
// Description : 

// Imports : 

import React from "react";
import { observer } from "mobx-react";
import { Grid, Row, Col, Table } from "react-bootstrap";
import { Link } from "react-router-dom";
import { GenericList } from "hbp-quickfire";
import injectStyles from "react-jss";

const styles = {
  title: {
    fontWeight: "bold",
  },
  doi: {
    color: "gray",
    textDecoration: "none !important",
    display: "inline"
  },
  date: {
    textDecoration: "none !important",
    display: "inline"
  }
};

const ItemTitle = injectStyles(styles)(({ classes, item }) => (
  <div>
    <Link to={`/person/${item.id}/`}>
      <div className={classes.title}>{item.last_name + ", " + item.first_name}</div>
    </Link>
  </div>
));

let listStyles = {
  container:{
    "& h3":{
      marginBottom: "20px"
    }
  }
};

// Class Definition
export default
@injectStyles(listStyles)
@observer
class PersonList extends React.Component {
// Attributes

// Constructor
  constructor(props) {
    super(props);
  }


// Operations
  render() {
    const {classes} = this.props;
    return (
      <Grid fluid={true} className={classes.container}>
        <Row>
          <Col xs={12}>
            <h3>{this.props.heading}</h3>
          </Col>
        </Row>
        <Row>
          <Col xs={12}>
            <GenericList
              items={this.props.store.items}
              itemTitle={ItemTitle}
              expanded={false}
            />
          </Col>
        </Row>
      </Grid>
    );
  }


}

// Exports

