import React from "react";
import ReactDOM from "react-dom";
import { Confirm } from "hbp-quickfire";

export default (message, callback) => {
  const container = document.createElement("div");
  document.body.appendChild(container);

  const withCleanup = answer => {
    ReactDOM.unmountComponentAtNode(container);
    document.body.removeChild(container);
    callback(answer);
  };

  ReactDOM.render(
    <Confirm
      show={true}
      message={message}
      confirmLabel={"OK"}
      cancelLabel={"Cancel"}
      onCancel={() => withCleanup(false)}
      onConfirm={() => withCleanup(true)}
    />,
    container
  );
};