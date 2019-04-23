/* global QUnit */
/* eslint-disable no-console */

import React from "react";
import ReactDOM from "react-dom";

import { Provider, observer } from "mobx-react";
import { Router, Route } from "react-router-dom";

import PersonStore from "../Stores/Persons";
import PersonQuery from "./PersonQuery";

import { createBrowserHistory } from "history";

const history = createBrowserHistory();

const stores = {
  personStore: new PersonStore()
};
for (const key in stores) {
  let store = stores[key];
  if (store.registerHistory && typeof store.registerHistory === "function") {
    store.registerHistory(history); // Make the history available in each store
  }
}

@observer
class Component extends React.Component {
  constructor(props) {
    super(props);
  }

  render() {
    console.log("Component.render");
    return (
      <Provider {...stores}>
        <Router history={history}>
          {/*
          <PersonQuery
            ref={(childComponent) => { this.childComponent = childComponent; }}
          />
          */}
          <Route path="*" component={PersonQuery} />
        </Router>
      </Provider>
    );
  }
}

QUnit.module("PersonQuery", function (hooks) {
  console.clear();
  this.component = ReactDOM.render(<Component />, document.getElementById("react"));

  hooks.before(function (assert) {
    console.log("QUnit.hooks.before");
    assert.ok(true, "before");
  });

  // QUnit.test("renderedParent", function (assert) {
  //   console.log("QUnit." + assert.test.testName);
  //   assert.ok(typeof this.component.props == "object", "passed");
  // });

  // QUnit.test("rendered", function (assert) {
  //   console.log("QUnit." + assert.test.testName);
  //   assert.ok(typeof this.component.childComponent.props == "object", "passed");
  // });

  // hooks.after(function (assert) { // Not getting called here for some reason
  //   console.log("QUnit.hooks.after");
  //   ReactDOM.unmountComponentAtNode(document.getElementById("react"));
  //   assert.ok(true, "after");
  // });
});

