sap.ui.define([
    "sap/ui/core/mvc/Controller",
    "sap/ui/model/json/JSONModel"
], function (Controller, JSONModel) {
    "use strict";

    return Controller.extend("sap.cap.catalog.controller.Books", {

        onInit: function () {

            const oData = {
                title: "Grokking Algorithms",
                author: "Aditya Bhargava",
                stock: 10
            };

            const oModel = new JSONModel(oData);

            this.getView().setModel(oModel);
        }

    });
});