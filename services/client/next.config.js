module.exports  = () => {

    webpack: (config, { isServer }) => {
        return config
    }

    serverRuntimeConfig: {
        mySecret: "secret"
    }

    const env =  {
        API_URL: process.env.REACT_APP_SERVICE_URL,
        API_SERVER_URL: process.env.REACT_APP_SERVER_SERVICE_URL
    }

    // next.config.js object
    return {
        env,
    }
}