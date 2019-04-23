///////////////////////////////////////////////////////////
// File        : Persons.js
// Description : 

// Imports : 

import { action, observable, computed } from "mobx";
import { FormStore } from "hbp-quickfire";

import definitions from "../definitions";
import jsonPath from "../jsonpath";
import BaseFormStore from "./BaseFormStore";
import PersonTypes from "./PersonTypes";

let personDetailsConfig = {
  fields: {
    id: {
      defaultValue: 0
    },
    first_name: {
      type: "InputText",
      label: "First Name",
      emptyToNull: false,
      validationRules: "required"
    },
    last_name: {
      type: "InputText",
      label: "Last Name",
      emptyToNull: false,
      validationRules: "required"
    },
    email: {
      type: "InputText",
      label: "Email",
      emptyToNull: false,
      validationRules: "required"
    },
    type: {
      defaultValue: 0,
      type: "Select",
      label: "Type",
      mappingValue: "numeric",
      mappingLabel: "alphanumeric",
    },
  }
};

// Class Definition
export default
class Persons extends BaseFormStore {
// Attributes

// Constructor
  constructor() {
    super("Person");
    this.personTypes = new PersonTypes();
    this.formStore = new FormStore(personDetailsConfig);
    let initialisation = [];
    initialisation.push(this.personTypes.get().then((options) => {this.formStore.getField("/type").updateOptions(options);}));
    this.synchronise = Promise.all(initialisation);
  }


// Operations
  @action
  injectValues(item) {
    item.saved_on = new Date(item.saved_on).toISOString().substr(0, 10);
    super.injectValues(item);
  }

  async validate() {
    let isValid = true;
    const fields = this.formStore.structure.fields;
    isValid = await super.validate();
    return isValid;
  }

  @action
  async save() {
    let item = this.getValues();
    // if (item.id) { // If it already exists...
    //   let URL = `/${this.GetItemType()}/${item.id}/`;
    //   let itemHash = this.itemHash;
    //   await this.getItemQuery(URL, "detail=true"); // ...fetch it again
    //   if (itemHash != this.itemHash) { // ...and check to see if it has changed...
    //     this.selectItem(item.id); // ...and reload
    //     this.status.error = "the item was changed by someone else while you were editing";
    //     setTimeout(() => (this.status.error = null), 10000); // Reset value after 10 seconds
    //     return item.id; // If we don't return an id we will have 'unsaved changes'
    //   }
    // }
    let id = await super.save(item);
    if (id) {
      this.selectItem(id); // Reload to ensure hash is updated
    }
    return id;
  }

  @action
  new() {
    super.new();
    this.formStore.toggleReadMode(false); // No point setting a 'new' one to read-only
  }


}

// Exports

