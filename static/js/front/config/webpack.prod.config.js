const HtmlWebpackPlugin = require('html-webpack-plugin');

module.exports = {
    mode: "production",
    entry: "./src/index.tsx",

    output: {
        path: __dirname + "/../../bundle",
        filename: "[name].bundle.js",
        chunkFilename: "[id].chunk.js",
        clean: true
    },

    module: {
        rules: [
            {
                test: /\.(ts|tsx)$/,
                loader: "ts-loader",
                exclude: /node_modules$/
            }
        ]
    },

    plugins: [
        new HtmlWebpackPlugin({
            publicPath: "/static/js/bundle",
            scriptLoading: "blocking",
            template: __dirname + "/../../../../templates/index.template.html",
            filename: __dirname + "/../../../../templates/index.html",
            inject: false,
            minify: true
        })
    ],

    resolve: {
        extensions: [".js", ".ts", ".tsx"]
    }
}