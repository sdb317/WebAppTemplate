/*global QUnit */
/* eslint-disable no-console */

import React from "react";

import { confirmModal } from "./ConfirmModal";

QUnit.module("ComponentDetails", function (hooks) {
  console.clear();

  hooks.before(function (assert) {
    console.log("QUnit.hooks.before");
    assert.ok(true, "before");
  });

  QUnit.test("display", function (assert) {
    console.log("QUnit." + assert.test.testName);
    // debugger;
    function getContent(content) {
      return <div dangerouslySetInnerHTML={{__html: content}} />;
    }
    confirmModal(getContent("First <br/> Second <br/> Third"))
      .then(() => {
        // debugger;
        console.log("resolved");
      })
      .catch(() => {
        // debugger;
        console.log("rejected");
      });
    assert.ok(true, "passed");
  });

  hooks.after(function (assert) { // Not getting called here for some reason
    console.log("QUnit.hooks.after");
    assert.ok(true, "after");
  });
});

