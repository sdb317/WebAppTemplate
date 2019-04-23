/*global QUnit, console */
/* eslint-disable no-console */

import BaseFormStore from "./BaseFormStore";

QUnit.module("BaseFormStore", function (hooks) {
    console.clear();
    this.component = new BaseFormStore();

    hooks.before(function (assert) {
        console.log("hooks.before");
        assert.ok(true, "before");
    });

    QUnit.test("constructor", function (assert) {
        console.log("rendered");
        assert.ok(typeof (this.component.items) != "undefined", "passed");
    });

    hooks.after(function (assert) { // Not getting called here for some reason
        console.log("hooks.after");
        assert.ok(true, "after");
    });
});

