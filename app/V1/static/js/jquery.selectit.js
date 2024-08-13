/*
// jquery.selectit plugin v1.0
// Tag Editor Field using jQuery
// Copyright (c) 2011-2024 Chris Pietschmann
// https://github.com/crpietschmann/jquery.selectit
// MIT License
*/
(function ($) {
    var keyCodes = {
        space: 32,
        enter: 13,
        comma: 188,
        backspace: 8,
        control: 17,
        isMatch: function () {
            var which = arguments[0];
            for (var i = 1; i < arguments.length; i++) {
                if (arguments[i] === which) {
                    return true;
                }
            }
            return false;
        }
    };
    var defaultOptions = {
        fieldname: null,
        values: null,
        animation: true
    };
    function parseValues(options) {
        var tags = splitString(this.val());
        for (var i in tags) {
            var tag = tags[i];
            if (tag.length > 0) {
                addValue.call(this.parent(), tag, options);
            }
        }
        this.val('');
    }
    function addValue(tag, options) {
        var hiddeninput = $('<input/>').attr('type', 'hidden').val(tag);
        if (options.fieldname) {
            hiddeninput.attr('name', options.fieldname);
        }
        var xSVG = '<svg class="svg-icon iconClearSm pe-none" width="14" height="14" viewBox="0 0 14 14"><path d="M12 3.41L10.59 2 7 5.59 3.41 2 2 3.41 5.59 7 2 10.59 3.41 12 7 8.41 10.59 12 12 10.59 8.41 7z"></path></svg>';
        var newElem = $('<span/>').addClass('selectit-option').html(tag).append(hiddeninput).append(
            $('<button/>').addClass('selectit-remove').attr('alt', 'remove').html(xSVG).click(function () {
                if (options.animation){
                    $(this).parent().fadeOut(function() {
                        $(this).remove();
                    });
                } else {
                    $(this).parent().remove();
                }
            })
        );
        this.before(newElem);
        if (options.animation) {
            newElem.hide().fadeIn();
        }
    }
    function splitString(str) {
        var arr = str.split(',');
        var finishedArray = [];
        for (var i = 0; i < arr.length; i++) {
            var temp = arr[i].split(' ');
            for (var x = 0; x < temp.length; x++) {
                finishedArray.push(temp[x]);
            }
        }
        return finishedArray;
    }

    $.fn.selectit = function (opts) {
        if (!opts || (opts && typeof opts !== 'string')) {
            var options = $.extend({}, defaultOptions, opts);
            var that = this;
            this.data('selectit-options', options);
            this.addClass("selectit").each(function () {
                // add input box
                var input = $('<input/>').
                    attr({ type: 'text' }).
                    addClass('selectit-input').
                    keyup(function (e) {
                        var elem = $(this);
                        if (keyCodes.isMatch(e.which, keyCodes.comma, keyCodes.control, keyCodes.enter, keyCodes.space)) {
                            parseValues.call(elem, that.data('selectit-options'));
                        }
                    }).
                    focus(function () {
                        $(that).addClass('focus');
                    }).
                    blur(function () {
                        parseValues.call($(this), that.data('selectit-options'));
                        $(that).removeClass('focus');
                    }).
                    keydown(function (e) {
                        var elem = $(this);
                        if (keyCodes.isMatch(e.which, keyCodes.backspace)) {
                            if (elem.val().length === 0) {
                                // remove the far right tag
                                var lastoption = elem.parent().parent().find('.selectit-option:last');
                                elem.val(lastoption.find('input').val());
                                lastoption.remove();
                                return false;
                            }
                        }
                    });
                $('<span/>').addClass('selectit-new').append(input).appendTo(this);
                $(that).click(function (e) {
                    if (e.target === this) {
                        input.focus();
                    }
                });
            });
            if (options.values) {
                this.selectit('add', options.values);
            }
        } else {
            var method = opts.toLowerCase();
            var value = arguments[1];
            // run methods on the selectit box
            // possible: add, remove, clear
            if (method === 'values') {
                var values = [];
                $(this).find('.selectit-option input[type=hidden]').each(function () {
                    values.push($(this).val());
                });
                return values;
            } else if (method === 'clear') {
                $(this).find('.selectit-option').remove();
            } else if (method === 'add') {
                if (typeof value === 'string') {
                    value = [value];
                }
                for (var vi = 0; vi < value.length; vi++) {
                    addValue.call($(this).find('.selectit-new'), value[vi], $(this).data('selectit-options'));
                }
            }
        }
        return this;
    };
})(jQuery);