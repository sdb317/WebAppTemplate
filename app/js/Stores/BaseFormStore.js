///////////////////////////////////////////////////////////
// File        : BaseFormStore.js
// Description : 

// GENERATED FROM UML - PLEASE DO NOT ADD/REMOVE ATTRIBUTES OR OPERATIONS

// Imports : 

import { observable, action } from "mobx";
import axios from "axios";
axios.defaults.xsrfCookieName = "csrftoken";
axios.defaults.xsrfHeaderName = "X-CSRFToken";
const axiosConfig = {
  headers: {
    "Content-Type": "application/json; charset=utf-8"
  }
};

import BaseStore from "./BaseStore";
import { confirmModal } from "../Components/ConfirmModal";

// Class Definition
export default
class BaseFormStore extends BaseStore {
// Attributes
  synchronise = false;
  @observable status = {error: null, success: null};;
  @observable highlights = '';
  @observable items = [];
  itemHash = 0;

// Constructor
  constructor(itemType) {
    super(itemType);
  }


// Operations
  registerHistory(history) {
    this.history = history;
  }

  navigateToItem(target,params) {
    if (this.history) {
      let URL = `/${this.GetItemType()}`;
      URL += (typeof target === "string" && target.length ? "/" + target : ""); // 'target' could be a specific id or 'new'
      URL += (typeof params === "string" && params.length ? "?" + params : ""); // 'params' could be search criteria
      this.history.push(URL); // The 'onHistoryChange' callback should call getItem(s)
    }
  }

  apiError(error) {
    this.status.error = null;
    // window.location.reload(true);
  }

  getPersonalItems() {
    this.getItems(`saved_by=${window.APP.user}`);
  }

  @action
  getItems(params,details=false) {
    let URL = `/${this.GetItemType()}/` + (typeof params === "string" && params.length ? "?" + params : ""); // Just summary values for list
    URL = "/api/v1" + URL + (typeof params === "string" && params.length ? "&" : "?") + `detail=${details ? "true" : "false"}`;
    console.log(`GET: ${URL}`);
    axios.get(URL) // Will do the request asynchronously so that the UI is still responsive
      .then((response) => {
        this.items = response.data[this.GetItemDataTypeList()];
      })
      .catch((error) => {
        console.error("Error in BaseFormStore.getItems: " + error);
        this.apiError(error);
      });
  }

  async getItemQuery(URL,params,delegate) { // Use with 'await' for individual items matching the criteria
    try {
      URL = "/api/v1" + URL + (typeof params === "string" && params.length ? "?" + params : "" );
      console.log(`GET: ${URL}`);
      let response = await axios.get(URL); // Will do the request asynchronously so that the UI is still responsive
      if (response.data[this.GetItemDataTypeList()].length == 1) {
        let item = response.data[this.GetItemDataTypeList()][0];
        this.itemHash = this.calculateHash(JSON.stringify(item));
        return item;
      } else {
        return; // Should only return one or 'undefined'
      }
    }
    catch(error) {
      console.error("Error in BaseFormStore.getItemQuery: " + error);
      // this.apiError(error);
    }
  }

  getItem(id,params,delegate) {
    let URL = `/${this.GetItemType()}/${id}/`;
    this.getItemQuery(URL, "detail=true" + (typeof params === "string" && params.length ? "&" + params : ""), delegate) // Full details for form
      .then(delegate || (item => this.injectValues(item))); // If no delegate, inject the values into the form
  }

  getItemAudit(id,params,delegate) {
    this.getItem(id, "audit=true" + (typeof params === "string" && params.length ? "&" + params : ""), delegate);
  }

  calculateHash(item) {
    return item.split("").reduce(function (a, b) { a = ((a << 5) - a) + b.charCodeAt(0); return a & a; }, 0);
  }

  selectItem(id) {
    if (!id || id === "new") {
      this.new();
    } else {
      this.getItem(id); // Get full details
      let matches = document.URL.match(/\/\d+\/\?highlight=([\w+]*)/); // Set highlights for an existing item
      if ( matches != null) {
        this.highlights = matches[1];
      }
    }
  }

  @action
  injectValues(item,merge=true) { // This can be overriden in derived classes
    if (this.synchronise) {
      this.synchronise = this.synchronise.then(() => {this.formStore.injectValues(item, merge);});
    } else {
      this.formStore.injectValues(item, merge);
    }
  }

  getValues() {
    return this.formStore.getValues();
  }

  async validate() {
    const isValid = await this.formStore.validate();
    let proceed = isValid;
    if (!isValid) {
      let errors = [];
      const fields = this.formStore.structure.fields;
      for (const fieldKey in fields) {
        if (fields[fieldKey].validationErrors) {
          errors.push(...fields[fieldKey].validationErrors);
          if (this.highlights.length) {
            this.highlights += '+';
          }
          this.highlights += fieldKey;
        }
      }
      let message = "Are you sure?\nThe form has the following errors:\n" + errors.map(error => `- ${error}`).join("\n");
      proceed = await confirmModal(message);
    }
    return proceed;
  }

  @action
  save(values) {
    this.highlights = "";
    if (typeof values === "undefined") {
      values = this.getValues();
    }
    let URL = `/api/v1/${this.GetItemType()}/`;
    let axiosMethod = "";
    if (values.id) { // Is it a create or an update?
      axiosMethod = "put";
      URL = URL + values.id + "/";
    } else {
      axiosMethod = "post";
    }
    console.log(`${axiosMethod.toUpperCase()}: ${URL}`);
    return new Promise((resolve, reject) => {
      axios[axiosMethod](URL, JSON.stringify(values), axiosConfig) // Functions are objects too!
        .then(response => {
          let id = response.data["Success"];
          if (id) {
            this.formStore.injectValues({"id": id}, true);
            this.navigateToItem(id.toString());
          }
          this.getItems();
          resolve(id);
          this.status.success = "saving";
          setTimeout(() => (this.status.success = null), 2000); // Reset value after 2 seconds
        })
        .catch(error => {
          reject(error);
          this.status.error = "saving";
          setTimeout(() => (this.status.error = null), 10000); // Reset value after 10 seconds but don't reload here or form item will be lost
          console.error("Error in BaseFormStore.save: " + error);
        });
    });
  }

  @action
  new() {
    this.highlights = "";
    this.formStore.reset();
    this.queryParams = "";
    this.status = {
      error: null,
      success: null
    };
  }

  @action
  delete() {
    this.highlights = "";
    let values = this.getValues();
    if (values.id) {
      let payload = {};
      payload[this.GetItemDataType()] = {}; // Create an object for the item type...
      payload[this.GetItemDataType()].id = values.id; // ...and add the id
      let URL = `/api/v1/${this.GetItemType()}/${payload[this.GetItemDataType()].id}/`;
      console.log(`DELETE: ${URL}`);
      axios.delete(URL, JSON.stringify(payload), axiosConfig)
        .then(() => {
          this.new();
          this.getItems();
          this.navigateToItem("new");
          this.status.success = "deleting";
          setTimeout(() => (this.status.success = null), 2000); // Reset value after 2 seconds
        })
        .catch(error => {
          this.status.error = "deleting";
          setTimeout(() => (this.apiError(error)), 10000); // Reset value after 10 seconds
          console.error("Error in BaseFormStore.delete: " + error);
        });
    }
  }


}

// Exports

