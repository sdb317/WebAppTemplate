///////////////////////////////////////////////////////////
// File        : PersonTypes.js
// Description : 

// Imports : 

import BaseSingletonStore from "./BaseSingletonStore";

// Class Definition
export default
class PersonTypes extends BaseSingletonStore {
// Attributes

// Constructor
  constructor() {
    super("options/person/type");
  }


// Operations
  setInstance(value) {
    PersonTypes.instance = value;
  }

  getInstance() {
    return PersonTypes.instance;
  }


}

// Exports

