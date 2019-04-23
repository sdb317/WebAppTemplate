/* global QUnit, console */
/* eslint-disable no-console */

import Persons from "./Persons";

QUnit.module("Person", function (hooks) {
  console.clear();
  this.component = new Persons();

  hooks.before(function (assert) {
    console.log("hooks.before");
    assert.ok(true, "before");
  });

  QUnit.test("constructor", function (assert) {
    console.log(assert.test.testName);
    assert.ok(typeof this.component.items != "undefined", "passed");
  });

  // QUnit.test("getItem", function (assert) {
  //   console.log(assert.test.testName);
  //   var done = assert.async();
  //   this.component.getItem(27,"",(item) => {
  //     console.log(item.name);
  //     assert.ok(typeof item.name != "undefined", "passed");
  //     done();
  //   });
  // });

  // QUnit.test("save", function (assert) {
  //   console.log(assert.test.testName);
  //   var done = assert.async();
  //   this.component.save().then(
  //     function() {
  //       assert.ok(this.component.getValues().id > 0, "passed");
  //       done();
  //     }.bind(this)
  //   );
  // });

  hooks.after(function (assert) { // Not getting called here for some reason
    console.log("hooks.after");
    assert.ok(true, "after");
  });
});

