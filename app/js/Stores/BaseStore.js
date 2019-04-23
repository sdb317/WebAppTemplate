///////////////////////////////////////////////////////////
// File        : BaseStore.js
// Description : 

// GENERATED FROM UML - PLEASE DO NOT ADD/REMOVE ATTRIBUTES OR OPERATIONS

// Imports : 

// Class Definition
export default
class BaseStore {
// Attributes
  itemType;

// Constructor
  constructor(itemType) {
    this.itemType = itemType;
  }


// Operations
  GetItemType() {
    if ((typeof(this.itemType) == undefined) || (!this.itemType.length)) {
      throw("No 'itemType'");
    } else {
      return this.itemType.toLowerCase();
    }
  }

  GetItemDataType() {
    return this.itemType;
  }

  GetItemDataTypeList() {
    return `${this.itemType}s`; // Plural
  }


}

// Exports

