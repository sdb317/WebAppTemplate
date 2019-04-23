import React from "react";
import { Alert } from "react-bootstrap";

export
class ErrorStatus extends React.Component {
  render() {
    return (
      <Alert bsStyle="danger">
        {`Error ${this.props.operation} ${String.fromCodePoint(0x1f641)}`}
        <br/>
        {`For assistance: `}<a href={'mailto:support@whoever.org?subject=APP: Error ' + this.props.operation}><strong>Contact Us...</strong></a>
      </Alert>
    );
  }
}

export
class SuccessStatus extends React.Component {
  render() {
    return (
      <Alert bsStyle="success">
        {`Success ${this.props.operation} ${String.fromCodePoint(0x1f642)}`}
      </Alert>
    );
  }
}
