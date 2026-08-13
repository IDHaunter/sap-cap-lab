sap.ui.define([
    "sap/ui/core/mvc/ControllerExtension"
], function (ControllerExtension) {
    "use strict";

    return ControllerExtension.extend("bookslist.ext.controller.ObjectPageExt", {
        onViewAuthor: function () {
            const oContext = this.base.getView().getBindingContext();
            const authorId = oContext.getProperty("author_ID");

            if (!authorId) {
                sap.m.MessageToast.show("This book has no author assigned yet.");
                return;
            }

            const url = `http://localhost:8081/test/flp.html?sap-ui-xx-viewCache=false#app-preview`;
            window.open(url, "_blank");
        }
    });
});