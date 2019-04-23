///////////////////////////////////////////////////////////
// File        : BaseSingletonStore.js
// Description : 

// Imports : 

import { cloneDeep } from "lodash";
import axios from "axios";

import BaseStore from "./BaseStore";

// Class Definition
export default
class BaseSingletonStore extends BaseStore {
// Attributes

// Constructor
  constructor(itemType) {
    super(itemType);
    if (!this.getInstance()) { // Abstract class - derived classes must provide static instance attribute
      this.setInstance(this);
      this.getInstance().promise = axios.get(`/api/v1/${this.GetItemType()}/`); // Will do the request asynchronously so that the UI is still responsive
    }
    return this.getInstance();
  }


// Operations
  async get() {
    let response = await this.getInstance().promise;
    let results = cloneDeep(response.data);
    return results;
  }


}

// Exports


