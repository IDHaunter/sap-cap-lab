sap.ui.define([
    "sap/fe/test/JourneyRunner",
	"authorslist/test/integration/pages/AuthorsList.gen",
	"authorslist/test/integration/pages/AuthorsObjectPage.gen"
], function (JourneyRunner, AuthorsListGenerated, AuthorsObjectPageGenerated) {
    'use strict';

    const runner = new JourneyRunner({
        launchUrl: sap.ui.require.toUrl('authorslist') + '/test/flp.html#app-preview',
        pages: {
			onTheAuthorsListGenerated: AuthorsListGenerated,
			onTheAuthorsObjectPageGenerated: AuthorsObjectPageGenerated
        },
        async: true
    });

    return runner;
});

