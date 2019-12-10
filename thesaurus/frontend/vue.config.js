module.exports = {
    publicPath: '',
    chainWebpack: config => {
        config.module
        .rule('raw')
        .test(/\.txt$/)
        .use('raw-loader')
        .loader('raw-loader')
        .end()
    },
}