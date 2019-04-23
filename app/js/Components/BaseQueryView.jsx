///////////////////////////////////////////////////////////
// File        : BaseQueryView.js
// Description : 

import queryString from "query-string";
import { debounce } from "lodash";

import BaseComponent from "./BaseComponent";

// Imports : 

// Class Definition
export default
class BaseQueryView extends BaseComponent {
// Attributes

// Constructor
  constructor(props,formStore) {
    super(props);
    this.formStore = formStore;
    this.re = new RegExp(`/${this.props.store.GetItemType()}(?!/)`, "");
    const timeout = 0.5;
    this.unlisten = this.props.history.listen(debounce((...args) => {
      this.onHistoryChange(...args);
    }, timeout*1000)); // Set up the re-query callback
    this.queryDetails=false;
  }


// Operations
  componentWillMount() {
    setTimeout(() => {this.onHistoryChange(this.props.location);}, 0); // ...and trigger the first query
  }

  render() {
  }

  componentDidMount() {
  }

  componentWillReceiveProps(nextProps) {
  }

  componentWillUpdate(nextProps,nextState) {
  }

  componentDidUpdate(prevProps,prevState) {
  }

  componentWillUnmount() {
    this.unlisten();
  }

  componentDidCatch(error,info) {
  }

  onChange() {
    this.props.store.navigateToItem(undefined, this.serialise(this.formStore.getValues()));
  }

  onHistoryChange(location,action) {
    if (this.re.test(location.pathname + location.search)) {
      let values = this.deserialise(location.search);
      this.formStore.injectValues(values); // Initialise the form from the query params...
      this.props.store.getItems(location.search.replace(/^\?/, ""), this.queryDetails); // ...and perform the query
    }
  }

  serialise(obj) {
    let str = [];
    for (let p in obj) {
      if (obj.hasOwnProperty(p)) {
        if ((obj[p] != null) && (typeof obj[p] != "object") && (obj[p] != "<Unknown>")) {
          str.push(encodeURIComponent(p) + "=" + encodeURIComponent(obj[p]));
        }
      }
    }
    if (str.length) {
      return str.join("&");
    } else {
      return "";
    }
  }

  deserialise(str) {
    let obj = queryString.parse(str);
    return obj;
  }


}

// Exports

