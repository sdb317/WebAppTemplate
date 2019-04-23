///////////////////////////////////////////////////////////
// File        : ConfirmModal.js
// Description : 

// Imports : 

import React from "react";
import ReactDOM from "react-dom";
import { Modal, Button } from "react-bootstrap";

let modalStyles = {
    zIndex:"10000",
    top:"50%",
    transform:"translateY(-25%)"
  };

let wrapper = null;

// Class Definition
class ConfirmModal extends React.Component {
// Attributes

// Constructor
  constructor(props) {
    super(props);
    this.state = {show: true};
  }


// Operations
  componentDidMount() {
    this.promise = new Promise((resolve, reject) => {this.resolve = resolve; this.reject = reject;});
  }

  render() {
    const {classes} = this.props;

    return(
      <Modal className={"quickfire-confirm"} style={modalStyles} show={this.state.show}>
        <Modal.Body>
          <div className={"quickfire-confirm-message"}>
            {this.props.message || "Confirm?"}
          </div>
        </Modal.Body>
        <Modal.Footer>
          <Button bsClass={"quickfire-confirm-action-confirm btn btn-success"} onClick={this.onConfirm.bind(this)}>{this.props.confirmLabel || "Confirm"}</Button>
          <Button bsClass={"quickfire-confirm-action-cancel btn btn-default"} onClick={this.onCancel.bind(this)}>{this.props.cancelLabel || "Cancel"}</Button>
        </Modal.Footer>
      </Modal>
    );
  }

  close() {
    ReactDOM.unmountComponentAtNode(wrapper);
    setTimeout(() => {wrapper.remove(); wrapper=null;}, 0);
  }

  onConfirm() {
    this.close();
    this.resolve(true);
  }

  onCancel() {
    this.close();
    this.resolve(false);
  }


}

// Exports
/* eslint-disable react/no-render-return-value */

export function confirmModal(message) {
  wrapper = document.body.appendChild(document.createElement('div'));
  function getContent(content) {
    return <div dangerouslySetInnerHTML={{__html: content.replace(/\n/g, '<br/>')}} />;
  }
  const props = {message: getContent(message)};
  const component = ReactDOM.render(React.createElement(ConfirmModal, props), wrapper);
  return component.promise;
}

