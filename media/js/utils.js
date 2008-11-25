Array.prototype.each = function(fn) {
    for (var i = 0; i < this.length; i++) {
        fn(this[i]);
    }
};
Array.prototype.map = function(fn) {
    var results = [];
    for (var i = 0; i < this.length; i++) {
        results.push(fn(this[i]));
    }
    return results;
};
Array.prototype.filter = function(test) {
    test = test || function(el) { return el ? true : false; };
    var results = [];
    for (var i = 0; i < this.length; i++)
        if (test(this[i]))
            results.push(this[i]);
    return results;
};
Array.prototype.any = function(test) {
    return this.filter(test).length > 0;
};
Array.prototype.contains = function(el) {
    return this.any(function (other) {
        return el == other;
    });
};

String.prototype.isEmpty = function() {
    return /^\s*$/.test(this);
};
String.prototype.trim = function() {
    return this.replace(/^\s+|\s+$/g, '');
};


if (!console) {
    var console = {
        log: function() {}
    };
}
