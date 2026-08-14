sap.ui.define([
    "sap/m/MessageToast"
], function (MessageToast) {
    "use strict";

    return {
        onViewAuthor: function (oContext) {
            const authorId = oContext.getProperty("author_ID");

            if (!authorId) {
                MessageToast.show("This book has no author assigned yet.");
                return;
            }

            const isLocal = window.location.hostname === "localhost";

            const url = isLocal
                ? "http://localhost:8081/test/flp.html?sap-ui-xx-viewCache=false#app-preview"
                : "../../authorslist/index.html";

            window.open(url, "_blank");
        }
    };
});