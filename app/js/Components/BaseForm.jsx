///////////////////////////////////////////////////////////
// File        : BaseForm.js
// Description : 

// GENERATED FROM UML - PLEASE DO NOT ADD/REMOVE ATTRIBUTES OR OPERATIONS

// Imports : 

import React from "react";
import { Button, Row, Col, Alert } from "react-bootstrap";
import { action } from "mobx";
import { Confirm } from "hbp-quickfire";
import { Prompt } from "react-router-dom";
import { Link } from "react-router-dom";
import { ErrorStatus, SuccessStatus } from "../StatusMessage";

import { areYouSure, leaveWithoutSaving } from "../Strings";

// Class Definition
export
class BaseForm extends React.Component {
// Attributes
  state = {confirm: false, unsavedChanges: false};
  styleOverrides = "";

// Constructor
  constructor(props) {
    super(props);
    /*
    'handlePageLeave' is called when user leaves or reloads page
    bind creates a new function reference. Therefore we need store the bound reference so we can pass the same reference to add- and later removeEventListener 
    */
    this.handlePageLeave = this._handlePageLeave.bind(this);
    this.styleOverrides += ".quickfire-tree-node {overflow: hidden; white-space: nowrap; text-overflow: ellipsis;} "; // Truncate long values in TreeSelect
    this.styleOverrides += ".quickfire-field .alert-danger {display: none;} "; // No validation pop-down's
    this.styleOverrides += ".quickfire-field .form-control-feedback {display: none;} "; // No glyphicons in inputs
    this.styleOverrides += ".quickfire-field .control-label {color: white;} "; // Don't change the label colour on validation
    this.styleOverrides += ".data-grid-container .data-grid .cell {text-align: left; vertical-align: top; color: black; font-family: sans-serif;} "; // Specific styles for DataSheet cells...
    this.styleOverrides += ".data-grid-container .data-grid.clip .cell {overflow-x: auto; word-wrap: break-word; white-space: normal;} "; // ...and clip them where necessary
  }


// Operations
  openFormFieldURL(fieldName) {
    const { store } = this.props;
    const url = store.formStore.getField(fieldName).value;
    openURLInNewTab(url);
  }

  componentWillMount() {    
  }

  render() {     
    return(<div>Not yet implemented!</div>);
  }

  renderEdit() {
    const { classes, store } = this.props;
    return(
      <Row className={classes.operationRow}>
        <Col xs={12} sm={6} md={2} style={{float: "right"}}>
          <Button
            className={classes.formButton}
            bsStyle="success"
            type="submit"
            onClick={() => store.formStore.toggleReadMode(false)}
            title={"Edit this item"}
          >
            Edit
          </Button>
        </Col>
      </Row>
    );
  }

  renderSaveNewDelete() {
    const { classes, store } = this.props;
    const { id } = this.props.match.params;
    const isNew = id == "new" ? true : false;
    return(
      <Row className={classes.operationRow}>
        <Col xs={12} sm={6}>
          {store.status.error && <ErrorStatus operation={store.status.error}/>}
          {store.status.success && <SuccessStatus operation={store.status.success}/>}
        </Col>
        <Col xs={12} sm={6} md={2}>
          <Button
            className={classes.formButton}
            bsStyle="success"
            type="submit"
            onClick={this.save.bind(this)}
            title={"Save the changes to the item"}
            disabled={!this.state.unsavedChanges} // only enabled if changes where made
          >
            Save
          </Button>
        </Col>
        <Col xs={12} sm={6} md={2} >
          <Button
            className={classes.formButton}              
            onClick={this.new.bind(this, false)}
            title={"Discard the changes and create a new item"}
          >
            New
          </Button>
        </Col>
        <Col xs={12} sm={6} md={2} >
          <Button
            className={classes.formButton}
            bsStyle="danger"
            onClick={this.delete.bind(this, false)}
            title={"Delete the item"}
            disabled={isNew} // when new item isn't saved yet, button is disabled
          >
            Delete...
          </Button>
        </Col>
        <div>
          <Confirm
            show={this.state.confirm}
            message={areYouSure}
            confirmLabel={"OK"}
            cancelLabel={"Cancel"}
            onConfirm={this.delete.bind(this, true)}
            onCancel={this.delete.bind(this, false)}
          />
          {/* This prevents react router from navigating to a different page when there are unsaved changes */}
          <Prompt
            when={this.state.unsavedChanges}
            message={leaveWithoutSaving}
          />
        </div>
      </Row>
    );
  }

  componentDidMount() {
    const { id } = this.props.match.params;
    this.get(id);
    window.addEventListener("beforeunload", this.handlePageLeave);
  }

  componentWillReceiveProps(nextProps) {
    const { id:prev_id } = this.props.match.params;
    const { id:next_id } = nextProps.match.params;
    const { search:prev_search } = this.props.location || {};
    const { search:next_search } = nextProps.location || {};
    if (next_id !== prev_id || next_search !== prev_search) {
      this.get(next_id);
      if (next_id !== "new") {
        this.setState({unsavedChanges: false});
      }
    }
  }

  componentWillUpdate(nextProps,nextState) {    
  }

  componentDidUpdate(prevProps,prevState) {
  }

  componentWillUnmount() {
    window.removeEventListener("beforeunload", this.handlePageLeave);
  }

  componentDidCatch(error,info) {
  }

  @action
  updateStatus = (status,timeout=0) => {
    this.status = {
      ...this.blankStatus,
      ...status
    };
    if (timeout) {
      setTimeout(() => this.status = { ...this.blankStatus }, timeout);
    }
  }

  highlight(fieldsToHighlight,fieldName) {
    if (fieldsToHighlight.split("+").findIndex(function (element) {return element==fieldName;}) != -1) {
      return {backgroundColor:"red", borderRadius:"8px"};
    }
    return {};
  }

  handleFormChange = () => {
    this.setState({unsavedChanges: true});
  }

  _handlePageLeave(e) { // handlePageLeave is called when user leaves or reloads page. Note this doesn't handle navigation within the website, this is handled by react router Prompt
    if (this.state.unsavedChanges) {
      e.returnValue = leaveWithoutSaving;
      return e.returnValue;
    }
  }

  get(id) {
    this.props.store.selectItem(id);
  }

  save(validate=true) {
    if (validate) {
      this.props.store.validate().
        then(response => {
          if (!response) {
            return;
          }
          this.setState({unsavedChanges: false});
          // if save was unsuccessful reset unsavedChanges so save button stays enabled
          this.props.store.save(undefined, validate).
            then(response => {
              if (!response) {
                this.setState({unsavedChanges: true});
              }
            })
            .catch(error => {
              this.setState({unsavedChanges: true});
            });
        })
        .catch(error => {
          this.setState({unsavedChanges: true});
        });
    }
    else {
      this.setState({unsavedChanges: false});
      // if save was unsuccessful reset unsavedChanges so save button stays enabled
      this.props.store.save(undefined, validate).
        then(response => {
          if (!response) {
            this.setState({unsavedChanges: true});
          }
        })
        .catch(error => {
          this.setState({unsavedChanges: true});
        });
    }
  }

  new() {
    /*
    'New' also acts as a reset button.
    To change the form values we usually trigger a url change and then react to a change of the publication id using react router
    We can't solely rely on that mechanism here because and have to do a manual reset in case we're already on the /new page
    since navigating to new won't change the url and trigger a re-initialization
    */
   if (this.state.unsavedChanges) {
      let response = confirm(leaveWithoutSaving);
      if (response === true) {
        // user confirmed
        this.setState({unsavedChanges: false}, () => {
          // after setState is done
          if (this.props.match.params.id !== "new") {
            // if not on new page. Navigate there (this also triggers the form to update its values)
            this.props.store.history.push(`/${this.props.store.GetItemType()}/new/`);
          } else {
            // if already on /new, navigating to new won't do a reset => manually reset it
            this.props.store.new();
            // reset the url (in case query params were set)
            this.props.store.history.push(`/${this.props.store.GetItemType()}/new/`);
          }
        });
      }
    } else {
      this.props.store.history.push(`/${this.props.store.GetItemType()}/new/`);
    }
  }

  delete(confirmed) {
    if (!confirmed) {
      this.setState({confirm: !this.state.confirm}); // This will either prompt for confirmation or close the modal
    } else {
      this.setState({confirm: false});
      this.setState({unsavedChanges: false});
      this.props.store.delete();
    }
  }


}

// Exports

export let BaseFormStyles = {
  container:{
    padding:"20px"
  },
  formButton:{
    display:"block",
    width:"100%",
    marginTop:"20px",
    marginBottom:"20px"
  }
};
