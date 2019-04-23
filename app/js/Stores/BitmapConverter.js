///////////////////////////////////////////////////////////
// File        : BitmapConverter.js
// Description : 

// Imports : 

// Class Definition
export default
class BitmapConverter {
// Attributes

// Constructor
  constructor(options) {
    this.options = options;
  }


// Operations
  fromBitmap(bitmap) {
    let values = [];
    Array.from(this.options, (v) => {if ((bitmap & (1 << v.numeric)) != 0) {values.push(v);}});
    return values;
  }

  toBitmap(values) {
    let bitmap = 0;
    Array.from(values, (v) => bitmap |= (1 << v.numeric));
    return bitmap;
  }


}

// Exports

