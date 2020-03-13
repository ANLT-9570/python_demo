


var alzjzx = {
    'get':function (args) {
        args['method'] = 'get';
        this.ajax(args);
    },
    'post':function (args) {
        args['method'] = 'post';
        this.ajax(args);
    },
    'ajax':function (args) {
        args['method'] = 'post';
        this.ajax(args);
    },
}