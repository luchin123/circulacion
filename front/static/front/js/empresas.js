(function($) {

    $("#empresas").tablesorter({
        theme : "bootstrap",
        widthFixed: true,
        headerTemplate : '{content} {icon}',
        widgets : ["uitheme", "filter", "print", "stickyHeaders"],
        widgetOptions : {
            filter_reset : ".reset",
            //filter_cssFilter: ['', 'datepicker', '', '', '', '', '']
            filter_functions: {
                0: {
                    'EMPRESA': function(e, n, f, i, $r) { return 'EMPRESA'},
                    'ASOCIACIÓN': function(e, n, f, i, $r) { return 'ASOCIACIÓN'},
                },
            }
        }
      })
      .tablesorterPager({
        container: $(".ts-pager"),
        ajaxUrl : '/empresas/json/?{filterList:filter}&{sortList:column}&page={page}&size={size}',
        customAjaxUrl: function(table, url) {
          $(table).trigger('changingUrl', url);
          return url;
        },
        ajaxObject: {
          dataType: 'json'
        },
        ajaxProcessing: function(data){
          if (data && data.hasOwnProperty('rows')) {
            var r, row, c, d = data.rows,
            // total number of rows (required)
            total = data.total_rows,
            // array of header names (optional)
            headers = data.headers,
            // all rows: array of arrays; each internal array has the table cell data for that row
            rows = [],
            // len should match pager set size (c.size)
            len = d.length;
            // this will depend on how the json is set up - see City0.json
            // rows.data('id')
            for ( r=0; r < len; r++ ) {
              row = []; // new row array
              // cells
              for ( c in d[r] ) {
                if (typeof(c) === "string") {
                  row.push(d[r][c]); // add each table cell data to row array
                }
              }
              rows.push(row); // add new row array to rows array
            }
            // in version 2.10, you can optionally return $(rows) a set of table rows within a jQuery object
            return [ total, rows, headers ];
          }
        },
        updateArrows: true,
        page: 0,
        size: 10,
        fixedHeight: false,
        output: '{startRow} - {endRow} / {filteredRows} ({totalRows})',
        removeRows: false,
        cssGoto  : ".pagenum",
        savePages : false,
      });

})(jQuery)
