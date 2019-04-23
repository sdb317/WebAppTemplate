/*global QUnit */
/* eslint-disable no-console */

import React from "react";
import ReactDOM from "react-dom";

import { observer } from "mobx-react";

import WhatsNew from "./WhatsNew";

@observer
class Component extends React.Component {
  constructor(props) {
    super(props);
  }

  render() {
    console.log("Component.render");
    return (
      <WhatsNew
        ref={(childComponent) => { this.childComponent = childComponent; }}
      />
    );
  }
}

QUnit.module("WhatsNew", function (hooks) {
  console.clear();
  this.component = ReactDOM.render(<Component />, document.getElementById("react"));

  hooks.before(function (assert) {
    console.log("QUnit.hooks.before");
    assert.ok(true, "before");
  });

  QUnit.test("renderedParent", function (assert) {
    console.log("QUnit." + assert.test.testName);
    assert.ok(typeof this.component.props == "object", "passed");
  });

  QUnit.test("rendered", function (assert) {
    console.log("QUnit." + assert.test.testName);
    assert.ok(typeof this.component.childComponent.props == "object", "passed");
  });

  // hooks.after(function (assert) { // Not getting called here for some reason
  //   console.log("QUnit.hooks.after");
  //   ReactDOM.unmountComponentAtNode(document.getElementById("react"));
  //   assert.ok(true, "after");
  // });
});

