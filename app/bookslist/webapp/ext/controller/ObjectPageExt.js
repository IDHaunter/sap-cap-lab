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

            const url = "http://localhost:8081/test/flp.html?sap-ui-xx-viewCache=false#app-preview";
            window.open(url, "_blank");
        }
    };
});