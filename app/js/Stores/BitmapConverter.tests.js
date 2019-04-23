/*global QUnit, console */
/* eslint-disable no-console */

import BitmapConverter from "./BitmapConverter";

QUnit.module("BitmapConverter", function (hooks) {
  console.clear();
  this.component = new BitmapConverter([{"label": "Unknown","numeric": 0,"alphanumeric": "<Unknown>"},{"label": "SPManagers","numeric": 1,"alphanumeric": "SP Managers"},{"label": "HBP","numeric": 2,"alphanumeric": "HBP"},{"label": "DIR","numeric": 3,"alphanumeric": "DIR"},{"label": "SIB","numeric": 4,"alphanumeric": "SIB"},{"label": "CivilSociety","numeric": 5,"alphanumeric": "Civil Society"},{"label": "Customers","numeric": 6,"alphanumeric": "Customers"},{"label": "GeneralPublic","numeric": 7,"alphanumeric": "General Public"},{"label": "Industry","numeric": 8,"alphanumeric": "Industry"},{"label": "Investors","numeric": 9,"alphanumeric": "Investors"},{"label": "Media","numeric": 10,"alphanumeric": "Media"},{"label": "PolicyMakers","numeric": 11,"alphanumeric": "Policy Makers"},{"label": "ScientificCommunity","numeric": 12,"alphanumeric": "Scientific Community"},{"label": "Other","numeric": 32,"alphanumeric": "Other..."}]);

  hooks.before(function (assert) {
    console.log("hooks.before");
    assert.ok(true, "before");
  });

  QUnit.test("fromBitmap", function (assert) {
    let fromBitmap = JSON.stringify(this.component.fromBitmap((1 << 1) | (1 << 3)));
    let expectedValues = JSON.stringify([{"label": "SPManagers","numeric": 1,"alphanumeric": "SP Managers"},{"label": "DIR","numeric": 3,"alphanumeric": "DIR"}]);
    assert.ok(fromBitmap == expectedValues, "passed");
  });

  QUnit.test("toBitmap", function (assert) {
    let toBitmap = this.component.toBitmap([{"label": "SPManagers","numeric": 1,"alphanumeric": "SP Managers"},{"label": "DIR","numeric": 3,"alphanumeric": "DIR"}]);
    let expectedValues = (1 << 1) | (1 << 3);
    assert.ok(toBitmap == expectedValues, "passed");
  });

  hooks.after(function (assert) { // Not getting called here for some reason
    console.log("hooks.after");
    assert.ok(true, "after");
  });
});

