// This code adds the word type filter to the word frequency
// results.

$(document).ready(function() {
    "use strict";

    var parseDataFromTable = function() {
        var dataSet = [];

        $('#word-frequency-table tbody tr').each(function() {
            var cols = $(this).find('td');
            dataSet.push({
                word: cols.eq(0).text(),
                count: cols.eq(1).text(),
                posTag: cols.eq(2).text()
            });
        });

        return dataSet;
    };

    var getUniqueTags = function(dataSet) {
        var allPosTags = $.map(dataSet, function(data_element) {
            return data_element.posTag;
        });

        var uniqueTagsDict = {},
            uniqueTagsArr = [];

        $.each(allPosTags, function() {
            if (uniqueTagsDict.hasOwnProperty(this)) {
                return true; // continue
            }
            uniqueTagsDict[this] = true;
            uniqueTagsArr.push(this);
        });

        return uniqueTagsArr;
    };

    var createSelectElement = function(uniqueTags) {
        var selectEl = $("#select-pos-tag");
        $.each(uniqueTags, function() {
            var el = "<option value='" + this + "'>" + this + "</option>";
            selectEl.append($(el));
        });
    };

    var filterDataSet = function(dataSet, filterFunc) {
        return $.map(dataSet, function(data_element) {
            if (filterFunc(data_element)) {
                return data_element;
            }
            return null; // remove from dataSet
        });
    };

    var renderTable = function(dataSet) {
        var tbody = $("#word-frequency-table tbody");
        tbody.html("");
        $.each(dataSet, function() {
            var tr = $("<tr/>");
            var td = $("<td/>");

            tr.append(td.clone().text(this.word));
            tr.append(td.clone().text(this.count));
            tr.append(td.clone().text(this.posTag));
            tbody.append(tr);
        });
    };

    var bindSelectChoiceToFilter = function(dataSet) {
        $("#select-pos-tag").on('change', function() {
            var selectedTag = $(this).val();
            var dataToRender = dataSet;

            if (selectedTag !== 'all') {
                var filterFunc = function(data_el) {
                    if (data_el.posTag === selectedTag) {
                        return true;
                    }
                    return false;
                };
                dataToRender = filterDataSet(dataSet, filterFunc);
            }

            renderTable(dataToRender);
        });
    };

    var main = function main() {
        var dataSet = parseDataFromTable();
        var uniqueTags = getUniqueTags(dataSet);
        createSelectElement(uniqueTags);

        bindSelectChoiceToFilter(dataSet);
    };

    main();

});